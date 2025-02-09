import subprocess
import time
from hashlib import sha256
from pathlib import Path
import argparse


DELAY = 1


def get_all_file_paths(source: str) -> list[Path]:
    all_files = Path(source).glob("*")
    return list(all_files)


def get_hash_from_files(file_paths: list[Path]) -> str:
    result = []
    for file_path in file_paths:
        if file_path.is_file():
            with file_path.open() as file:
                content = file.read()
                result.append(sha256(content.encode("utf-8")).hexdigest())
    return sha256("".join(result).encode("utf-8")).hexdigest()


def watcher(source: str, execution_command: str) -> None:
    if source is None or execution_command is None:
        raise ValueError("Please specify source and execution command")
    process = subprocess.Popen(execution_command, shell=True)
    old_hash = None
    while True:
        if (new_hash := get_hash_from_files(get_all_file_paths(source))) != old_hash:
            old_hash = new_hash
            process.terminate()
            process = subprocess.Popen(execution_command, shell=True)
        time.sleep(DELAY)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="йоу")
    parser.add_argument("--exec_command", help="Path for execution file")
    parser.add_argument("--source", help="Source for watching")

    args = parser.parse_args()
    watcher(args.source, args.exec_command)
