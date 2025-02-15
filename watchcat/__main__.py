import subprocess
import time
from datetime import datetime
from hashlib import sha256
from pathlib import Path
import argparse


class WatchCat:
    def __init__(self, watch_delay: int, source_dir: str, execution_command: str):
        self._watch_delay = watch_delay
        self._source_dir = source_dir
        self._execution_command = execution_command
        self._dir_state: dict[str, float] = {}

    def _get_all_file_paths(self) -> list[Path]:
        all_paths = Path(self._source_dir).glob("*")
        return [path for path in all_paths if path.is_file()]

    def _is_dir_change(self) -> bool:
        file_paths = self._get_all_file_paths()
        for file_path in file_paths:
            absolute_path = str(file_path.absolute())
            if absolute_path not in self._dir_state:
                return True
            if self._dir_state[absolute_path] != file_path.stat().st_mtime:
                return True
        return False

    def _init_dir_state(self):
        file_paths = self._get_all_file_paths()
        for file_path in file_paths:
            self._dir_state[str(file_path.absolute())] = file_path.stat().st_mtime

    def watcher(self) -> None:
        self._init_dir_state()
        process = subprocess.Popen(self._execution_command, shell=True)
        while True:
            if self._is_dir_change() is True:
                process.terminate()
                process = subprocess.Popen(self._execution_command, shell=True)
            time.sleep(self._watch_delay)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Watch cat - meow meow meow")
    parser.add_argument("--exec_command", help="Path for execution file")
    parser.add_argument("--source", help="Source for watching")
    parser.add_argument("--watch_delay", help="Delay for re-watch files", default=10)

    args = parser.parse_args()
    watch_cat = WatchCat(watch_delay=args.watch_delay, source_dir=args.source, execution_command=args.exec_command)
    watch_cat.watcher()