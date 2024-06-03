import argparse
import importlib
from . import core
from pathlib import Path
from .tasks import Task


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-H", "--host", default="localhost", help="host to listen on")
    parser.add_argument(
        "-P", "--port", type=int, default=8080, help="port to listen on"
    )
    parser.add_argument(
        "-D",
        "--task-directory",
        type=Path,
        default="tasks",
        help="task models directory",
    )
    parser.add_argument(
        "-T", "--task-file", type=list[Path], help="single task model file to load"
    )
    parser.add_argument(
        "-C", "--config", default="config.json", help="path to configuration file"
    )
    args = parser.parse_args()

    # Load the task models and configuration, then run the server
    for task_file in args.task_file:
        Task.load(task_file)

    core.run(
        host=args.host,
        port=args.port,
        task_directory=args.task_directory,
        task_file=args.task_file,
        config=args.config,
    )
