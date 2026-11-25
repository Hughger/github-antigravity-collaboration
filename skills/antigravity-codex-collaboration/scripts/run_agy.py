"""Supervise an explicitly authorized, read-only local Antigravity CLI turn.

The JSON result and process termination are separate facts. No retries, global
configuration changes, process-name kills, or shell-built command lines.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time
import uuid


def read_result(path, expected_conversation=None):
    """Read a terminal JSON envelope, including empty/denied failed turns."""
    try:
        result = json.loads(path.read_bytes().decode("utf-8-sig"))
        if not isinstance(result, dict):
            return None
        conversation = result.get("conversation_id")
        uuid.UUID(conversation)
        if expected_conversation and conversation != expected_conversation:
            return None
        if not isinstance(result.get("status"), str) or not result["status"]:
            return None
        if not isinstance(result.get("response"), str):
            return None
        return result
    except (OSError, UnicodeError, ValueError, TypeError, AttributeError):
        return None


def supervise(command, workspace, output_dir, *, timeout_seconds=600,
              exit_grace_seconds=5, expected_conversation=None):
    """Retain output and reap only the child held by this Popen handle."""
    if timeout_seconds <= 0 or exit_grace_seconds <= 0:
        raise ValueError("Timeout and exit grace must be positive")
    workspace = Path(workspace).resolve(strict=True)
    output_dir = Path(output_dir).resolve()
    output_dir.relative_to(workspace)
    output_dir.mkdir(parents=True, exist_ok=False)
    stdout_path = output_dir / "stdout.json"
    stderr_path = output_dir / "stderr.log"
    record = {
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "workspace": str(workspace), "executable": command[0],
        "pid": None, "process_exit_code": None, "active_process": False,
        "cleanup_reason": None, "result_valid": False,
        "timeout_seconds": timeout_seconds, "exit_grace_seconds": exit_grace_seconds,
        "expected_conversation": expected_conversation,
    }
    started = time.monotonic()
    result_seen = None
    last_result = None
    proc = None
    interrupted = False
    error = None
    # Direct files avoid a pipe-reader or inherited pipe keeping this wrapper alive.
    with stdout_path.open("xb", buffering=0) as out, stderr_path.open("xb", buffering=0) as err:
        try:
            proc = subprocess.Popen(
                command, cwd=workspace, stdin=subprocess.DEVNULL, stdout=out, stderr=err,
                shell=False, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
            record["pid"] = proc.pid
            (output_dir / "process.json").write_text(
                json.dumps({**record, "status": "RUNNING", "active_process": True}, indent=2),
                encoding="utf-8",
            )
            while proc.poll() is None:
                now = time.monotonic()
                result = read_result(stdout_path, expected_conversation)
                if result is not None:
                    if result != last_result:
                        result_seen = now
                    if now - result_seen >= exit_grace_seconds:
                        record["cleanup_reason"] = "final_result_exit_grace"
                        break
                else:
                    result_seen = None
                last_result = result
                if now - started >= timeout_seconds:
                    record["cleanup_reason"] = "turn_deadline"
                    break
                time.sleep(0.05)
        except KeyboardInterrupt:
            interrupted = True
            record["cleanup_reason"] = "interrupted"
        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"
            record["cleanup_reason"] = "runner_error"
        finally:
            if proc is not None:
                if proc.poll() is None:
                    try:
                        # On Windows terminate/kill use this child's retained OS handle.
                        proc.terminate()
                        proc.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        try:
                            proc.kill()
                            proc.wait(timeout=5)
                        except (OSError, subprocess.TimeoutExpired) as exc:
                            error = f"cleanup failed: {exc}"
                    except OSError as exc:
                        if proc.poll() is None:
                            error = f"cleanup failed: {exc}"
                record["process_exit_code"] = proc.poll()
                record["active_process"] = proc.poll() is None

    result = read_result(stdout_path, expected_conversation)
    denied_actions = result.get("denied_actions", []) if result else []
    record.update({
        "terminal_json_received": result is not None,
        "result_valid": bool(result and result["response"].strip() and not denied_actions),
        "denied_actions": denied_actions,
        "result_status": result.get("status") if result else None,
        "conversation_id": result.get("conversation_id") if result else None,
        "stdout_sha256": hashlib.sha256(stdout_path.read_bytes()).hexdigest(),
        "duration_seconds": round(time.monotonic() - started, 3),
        "error": error,
    })
    if record["active_process"]:
        status, code = "CLEANUP_FAILED", 4
    elif interrupted:
        status, code = "CANCELLED", 130
    elif error:
        status, code = "RUNNER_ERROR", 4
    elif denied_actions:
        status, code = "PERMISSION_DENIED", 3
    elif record["cleanup_reason"] == "turn_deadline":
        status, code = "TIMED_OUT", 124
    elif result is None:
        status, code = "INVALID_RESULT", 3
    elif result["status"] != "SUCCESS":
        status, code = "MODEL_ERROR", 3
    elif not record["result_valid"]:
        status, code = "INVALID_RESULT", 3
    elif record["cleanup_reason"] == "final_result_exit_grace":
        status, code = "RESULT_RECEIVED_PROCESS_TERMINATED", 2
    elif record["process_exit_code"] != 0:
        status, code = "PROCESS_ERROR", 3
    else:
        status, code = "COMPLETED", 0
    record.update(status=status, runner_exit_code=code)
    (output_dir / "process.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agy", type=Path, required=True)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--conversation")
    parser.add_argument("--timeout-seconds", type=float, default=600)
    parser.add_argument("--exit-grace-seconds", type=float, default=5)
    args = parser.parse_args()
    if args.conversation:
        uuid.UUID(args.conversation)
    prompt = sys.stdin.read().strip()
    if not prompt:
        parser.error("Pass the authorized prompt through UTF-8 standard input")
    command = [str(args.agy.resolve(strict=True)), "--mode", "plan", "--sandbox",
               "--output-format", "json", "--print-timeout", f"{args.timeout_seconds:g}s"]
    if args.conversation:
        command += ["--conversation", args.conversation]
    command += ["--print", prompt]
    record = supervise(command, args.workspace, args.output_dir,
                       timeout_seconds=args.timeout_seconds,
                       exit_grace_seconds=args.exit_grace_seconds,
                       expected_conversation=args.conversation)
    print(json.dumps(record, ensure_ascii=False), flush=True)
    return record["runner_exit_code"]


if __name__ == "__main__":
    sys.exit(main())
