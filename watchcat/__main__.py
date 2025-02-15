import argparse
import subprocess
import time
from pathlib import Path


class WatchCat:
    def __init__(self, watch_delay: int, source_dir: str, execution_command: str):
        self._watch_delay = watch_delay
        self._source_dir = source_dir
        self._execution_command = execution_command
        self._max_folder_level = max_folder_level
        self._dir_state: dict[str, float] = {}

    def _get_all_file_paths(self, directory: str | Path = None, max_folder_level: int = 0) -> list[Path]:
        all_paths = Path(directory if directory else self._source_dir).glob("*")

        if max_folder_level == 0:
            return [path for path in all_paths if path.is_file()]

        elif max_folder_level > 0:
            subfolder_paths = []
            for path in all_paths:
                if path.is_file():
                    subfolder_paths.append(path)
                elif path.is_dir():
                    subfolder_paths.extend(self._get_all_file_paths(path, max_folder_level - 1))
            return subfolder_paths

        elif max_folder_level < 0:
            raise ValueError("max_folder_level must be greater than 0")

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
