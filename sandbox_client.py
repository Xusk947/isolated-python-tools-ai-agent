import json
import os
import socket
import sys


SOCKET_PATH = os.environ.get("SANDBOX_SOCKET", "/tmp/sandbox.sock")


def main():
    raw = sys.stdin.readline()
    if not raw:
        return
    try:
        req = json.loads(raw)
    except Exception as e:
        sys.stdout.write(json.dumps({"error": f"invalid json: {e}"}) + "\n")
        return

    code = req.get("code", "")
    if not isinstance(code, str):
        code = str(code)

    payload = json.dumps({"code": code}, ensure_ascii=False).encode("utf-8") + b"\n"
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.settimeout(30)
            s.connect(SOCKET_PATH)
            s.sendall(payload)
            s.shutdown(socket.SHUT_WR)
            data = b""
            while chunk := s.recv(4096):
                data += chunk
    except Exception as e:
        sys.stdout.write(json.dumps({"error": f"socket error: {e}"}) + "\n")
        return

    sys.stdout.write(data.decode("utf-8", errors="replace").strip() + "\n")


if __name__ == "__main__":
    main()
