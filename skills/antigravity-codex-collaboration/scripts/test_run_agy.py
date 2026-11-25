"""Process-boundary regressions; no model calls or credentials."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SPEC = importlib.util.spec_from_file_location("run_agy", Path(__file__).with_name("run_agy.py"))
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)
CID = "00000000-0000-4000-8000-000000000001"
RESULT = {"status": "SUCCESS", "conversation_id": CID, "response": "PASS"}


class LifecycleTests(unittest.TestCase):
    def run_child(self, source, *, conversation=None, timeout=3):
        with tempfile.TemporaryDirectory(prefix="agy-lifecycle-") as folder:
            out = Path(folder) / "run"
            record = runner.supervise(
                [sys.executable, "-u", "-c", source], Path(folder), out,
                timeout_seconds=timeout, exit_grace_seconds=0.15,
                expected_conversation=conversation,
            )
            self.assertFalse(record["active_process"])
            self.assertIsNotNone(record["process_exit_code"])
            self.assertEqual(json.loads((out / "process.json").read_text()), record)
            return record, (out / "stdout.json").read_bytes()

    def test_successful_result_then_hang_is_retained_and_reaped(self):
        # This reproduces the observed CLI boundary, not a second real model run.
        source = f"import json,time; print(json.dumps({RESULT!r}),flush=True); time.sleep(30)"
        record, raw = self.run_child(source)
        self.assertEqual(record["status"], "RESULT_RECEIVED_PROCESS_TERMINATED")
        self.assertEqual(record["runner_exit_code"], 2)
        self.assertEqual(record["cleanup_reason"], "final_result_exit_grace")
        self.assertEqual(json.loads(raw), RESULT)

    def test_natural_exit_is_success(self):
        record, _ = self.run_child(f"import json; print(json.dumps({RESULT!r}))")
        self.assertEqual(record["status"], "COMPLETED")
        self.assertEqual(record["process_exit_code"], 0)
        self.assertIsNone(record["cleanup_reason"])

    def test_partial_json_is_not_a_final_result(self):
        source = 'import time; print(\'{"status":"SUCCESS"\',flush=True); time.sleep(30)'
        record, _ = self.run_child(source, timeout=0.5)
        self.assertEqual(record["status"], "TIMED_OUT")
        self.assertFalse(record["result_valid"])

    def test_wrong_conversation_is_not_accepted(self):
        record, _ = self.run_child(
            f"import json; print(json.dumps({RESULT!r}))", conversation="other-session"
        )
        self.assertEqual(record["status"], "INVALID_RESULT")

    def test_success_json_does_not_hide_nonzero_process_exit(self):
        source = f"import json,sys; print(json.dumps({RESULT!r})); sys.exit(7)"
        record, _ = self.run_child(source)
        self.assertEqual(record["status"], "PROCESS_ERROR")
        self.assertEqual(record["process_exit_code"], 7)
        self.assertTrue(record["result_valid"])

    def test_model_error_is_not_success(self):
        result = {**RESULT, "status": "ERROR", "response": "request failed"}
        record, _ = self.run_child(f"import json; print(json.dumps({result!r}))")
        self.assertEqual(record["status"], "MODEL_ERROR")

    def test_denied_empty_success_is_terminal_but_not_accepted(self):
        result = {**RESULT, "response": "", "denied_actions": [{"action": "command", "display_name": "Bash"}]}
        source = f"import json,time; print(json.dumps({result!r}),flush=True); time.sleep(30)"
        record, raw = self.run_child(source)
        self.assertEqual(record["status"], "PERMISSION_DENIED")
        self.assertEqual(record["cleanup_reason"], "final_result_exit_grace")
        self.assertFalse(record["result_valid"])
        self.assertTrue(record["terminal_json_received"])
        self.assertEqual(json.loads(raw), result)

    def test_empty_success_without_denial_is_not_accepted(self):
        result = {**RESULT, "response": ""}
        record, _ = self.run_child(f"import json; print(json.dumps({result!r}))")
        self.assertEqual(record["status"], "INVALID_RESULT")

    def test_slow_fragmented_output_gets_time_to_finish(self):
        data = json.dumps(RESULT)
        split = len(data) // 2
        source = (
            f"import sys,time; sys.stdout.write({data[:split]!r}); sys.stdout.flush(); "
            f"time.sleep(0.4); sys.stdout.write({data[split:]!r}); sys.stdout.flush()"
        )
        record, _ = self.run_child(source)
        self.assertEqual(record["status"], "COMPLETED")

    def test_cleanup_does_not_stop_an_unrelated_process(self):
        unrelated = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"])
        try:
            self.run_child(
                f"import json,time; print(json.dumps({RESULT!r}),flush=True); time.sleep(30)"
            )
            self.assertIsNone(unrelated.poll())
        finally:
            unrelated.terminate()
            unrelated.wait(timeout=5)

    def test_existing_output_is_preserved(self):
        with tempfile.TemporaryDirectory(prefix="agy-lifecycle-") as folder:
            out = Path(folder) / "existing"
            out.mkdir()
            marker = out / "stdout.json"
            marker.write_text("original evidence")
            with self.assertRaises(FileExistsError):
                runner.supervise([sys.executable, "-c", "pass"], Path(folder), out,
                                 timeout_seconds=1, exit_grace_seconds=0.15)
            self.assertEqual(marker.read_text(), "original evidence")


if __name__ == "__main__":
    unittest.main()
