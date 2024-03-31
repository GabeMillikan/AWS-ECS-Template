"""
This script is used to start the DEVELOPMENT server (i.e. on localhost).
"""

import subprocess
import sys


def run_command(cmd: str | list[str]) -> subprocess.Popen:
    print(f"=> {cmd}")
    return subprocess.Popen(
        cmd,
        shell=True,
        stdin=sys.stdin,
        stdout=sys.stdout,
        stderr=sys.stderr,
    )


def start_backend() -> subprocess.Popen:
    return run_command("uvicorn server:app --host 0.0.0.0 --port 8000")


start_backend().wait()
# this is where you'd start the database & frontend
