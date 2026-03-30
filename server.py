import io
import json
import os
import signal
import socketserver
import sys
import time
import traceback
from contextlib import redirect_stderr, redirect_stdout

import artifact_hooks


WORKDIR = os.environ.get("SANDBOX_WORKDIR", "/workspace")
SOCKET_PATH = os.environ.get("SANDBOX_SOCKET", "/tmp/sandbox.sock")
TIMEOUT_SECONDS = int(os.environ.get("SANDBOX_TIMEOUT_SECONDS", "15"))


def _snapshot_files() -> dict[str, tuple[int, int]]:
    out: dict[str, tuple[int, int, int, int, int]] = {}
    for root, _, files in os.walk(WORKDIR):
        for f in files:
            p = os.path.join(root, f)
            try:
                st = os.stat(p)
            except FileNotFoundError:
                continue
            if not os.path.isfile(p):
                continue
            mtime_ns = int(getattr(st, "st_mtime_ns", int(st.st_mtime * 1_000_000_000)))
            ctime_ns = int(getattr(st, "st_ctime_ns", int(st.st_ctime * 1_000_000_000)))
            dev = int(getattr(st, "st_dev", 0))
            ino = int(getattr(st, "st_ino", 0))
            out[p] = (int(st.st_size), mtime_ns, ctime_ns, dev, ino)
    return out


def _workdir_has_entries() -> bool:
    try:
        with os.scandir(WORKDIR) as it:
            for _ in it:
                return True
    except FileNotFoundError:
        return False
    return False


def _changed_files(before: dict[str, tuple[int, int, int, int, int]], after: dict[str, tuple[int, int, int, int, int]]) -> list[str]:
    changed: list[str] = []
    for p, meta in after.items():
        if before.get(p) != meta:
            changed.append(p)
    changed.sort()
    return changed[:50]


class _Timeout(Exception):
    pass


def _timeout_handler(_signum, _frame):
    raise _Timeout("execution timed out")


class Handler(socketserver.StreamRequestHandler):
    def handle(self):
        line = self.rfile.readline()
        if not line:
            return
        try:
            req = json.loads(line.decode("utf-8"))
        except Exception as e:
            self.wfile.write((json.dumps({"error": f"invalid json: {e}"}) + "\n").encode("utf-8"))
            return

        code = req.get("code", "")
        if not isinstance(code, str) or not code.strip():
            self.wfile.write((json.dumps({"error": "code cannot be empty"}) + "\n").encode("utf-8"))
            return

        artifact_hooks.ensure_auto_artifact_hooks(WORKDIR)
        before = _snapshot_files() if _workdir_has_entries() else {}
        out = io.StringIO()
        err = io.StringIO()
        error_text = ""

        old = signal.getsignal(signal.SIGALRM)
        signal.signal(signal.SIGALRM, _timeout_handler)
        signal.setitimer(signal.ITIMER_REAL, TIMEOUT_SECONDS)

        try:
            with redirect_stdout(out), redirect_stderr(err):
                exec(code, {"__name__": "__main__", "__builtins__": __builtins__})
        except _Timeout as e:
            error_text = str(e)
        except Exception:
            error_text = traceback.format_exc()
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, old)

        after = _snapshot_files() if _workdir_has_entries() else {}
        resp = {
            "stdout": out.getvalue(),
            "stderr": err.getvalue(),
            "error": error_text,
            "changed_files": _changed_files(before, after),
        }
        self.wfile.write((json.dumps(resp, ensure_ascii=False) + "\n").encode("utf-8"))


def main():
    os.makedirs(WORKDIR, exist_ok=True)
    os.chdir(WORKDIR)
    try:
        os.unlink(SOCKET_PATH)
    except FileNotFoundError:
        pass

    start = time.time()
    with socketserver.UnixStreamServer(SOCKET_PATH, Handler) as srv:
        os.chmod(SOCKET_PATH, 0o777)
        sys.stdout.write(f"ready in {int((time.time()-start)*1000)}ms\n")
        sys.stdout.flush()
        srv.serve_forever()


if __name__ == "__main__":
    main()
