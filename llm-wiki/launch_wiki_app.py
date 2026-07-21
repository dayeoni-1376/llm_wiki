#!/usr/bin/env python3
import os
import signal
import subprocess
import sys
import time
import urllib.request
import webbrowser
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from typing import Optional

APP_ROOT = Path(__file__).resolve().parent
MAINTAINER = APP_ROOT / "llm_wiki_maintainer.py"
VENV_PYTHON = APP_ROOT / ".venv" / "bin" / "python"
SERVER_URL = "http://127.0.0.1:8501"


def find_python() -> Path:
    if VENV_PYTHON.exists():
        return VENV_PYTHON
    return Path(sys.executable)


class WikiAppWindow:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("LLM Wiki Assistant")
        self.root.geometry("420x180")
        self.root.resizable(False, False)

        self.server_process: Optional[subprocess.Popen] = None
        self.is_shutting_down = False

        style = ttk.Style(self.root)
        style.theme_use("clam")

        label = ttk.Label(
            self.root,
            text="LLM Wiki를 열고 질문할 준비가 됩니다.",
            font=("Helvetica", 13),
            wraplength=380,
        )
        label.pack(pady=(18, 8))

        self.status_var = tk.StringVar(value="초기화 중...")
        status = ttk.Label(self.root, textvariable=self.status_var, foreground="#1f5fbf")
        status.pack(pady=(0, 12))

        buttons = ttk.Frame(self.root)
        buttons.pack()
        ttk.Button(buttons, text="브라우저 열기", command=self.open_browser).pack(side=tk.LEFT, padx=6)
        ttk.Button(buttons, text="종료", command=self.shutdown).pack(side=tk.LEFT, padx=6)

        self.root.protocol("WM_DELETE_WINDOW", self.shutdown)

    def start_server(self) -> None:
        python_exe = str(find_python())
        cmd = [
            python_exe,
            "-m",
            "streamlit",
            "run",
            str(MAINTAINER),
            "--server.headless",
            "true",
            "--server.address",
            "127.0.0.1",
            "--server.port",
            "8501",
        ]
        log_path = APP_ROOT / "streamlit_app.log"
        with log_path.open("a", encoding="utf-8") as log_file:
            self.server_process = subprocess.Popen(
                cmd,
                cwd=str(APP_ROOT),
                stdout=log_file,
                stderr=subprocess.STDOUT,
                start_new_session=True,
            )

        self.wait_for_server()
        self.status_var.set("열림: http://127.0.0.1:8501")
        self.open_browser()

    def wait_for_server(self) -> None:
        deadline = time.time() + 40
        while time.time() < deadline:
            try:
                with urllib.request.urlopen(SERVER_URL, timeout=1.0) as response:
                    if response.status < 500:
                        return
            except Exception:
                time.sleep(0.5)
        raise RuntimeError("Streamlit 서버가 시작되지 않았습니다.")

    def open_browser(self) -> None:
        webbrowser.open(SERVER_URL)

    def shutdown(self) -> None:
        if self.is_shutting_down:
            return
        self.is_shutting_down = True
        self.status_var.set("종료 중...")
        self.stop_server()
        self.root.destroy()

    def stop_server(self) -> None:
        if self.server_process is None:
            return
        try:
            os.killpg(self.server_process.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        except PermissionError:
            try:
                self.server_process.terminate()
            except Exception:
                pass
        try:
            self.server_process.wait(timeout=8)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(self.server_process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            self.server_process.wait(timeout=3)

    def run(self) -> None:
        self.start_server()
        self.root.mainloop()


if __name__ == "__main__":
    try:
        app = WikiAppWindow()
        app.run()
    except KeyboardInterrupt:
        pass
    except Exception as exc:
        print(f"Failed to launch: {exc}", file=sys.stderr)
        sys.exit(1)
