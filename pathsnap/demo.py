"""Run the API and interface together for the student-test demo."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data", nargs="?", type=Path, default=Path("Student folder"),
                        help="extracted folder containing student_test")
    args = parser.parse_args()
    student_test = (args.data / "student_test").resolve()
    if not student_test.is_dir():
        parser.error(f"Extract Student folder.zip or provide the extracted folder: {student_test}")
    settings = dict(os.environ, PATHSNAP_MODE="demo", PATHSNAP_TRIPS=str(student_test),
                    PATHSNAP_REFERENCES=str(student_test), PATHSNAP_MODEL=str(ROOT / "artifacts/model.joblib"))
    handler = partial(SimpleHTTPRequestHandler, directory=str(ROOT / "ui"))
    with ThreadingHTTPServer(("127.0.0.1", 8080), handler) as server:
        api = subprocess.Popen([sys.executable, "-m", "uvicorn", "pathsnap.api:app",
                                "--host", "127.0.0.1", "--port", "8000"], cwd=ROOT, env=settings)
        try:
            print("PathSnap UI: http://localhost:8080", flush=True)
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            api.terminate()
            api.wait(timeout=10)


if __name__ == "__main__":
    main()
