from __future__ import annotations
import time
from abc import ABC, abstractmethod
from enum import Enum
from importlib import util as _importutil
from pathlib import Path
from pydantic import BaseModel

from .util import TimeDelta, DateTime


class TaskStatus(Enum):
    NEEDED = 1
    """Task is required to be completed."""

    READY = 2
    """Task is available to be completed but is not required."""

    WAITING = 3
    """Task is not yet available to be completed, but it will be in the future."""

    DONE = 4
    """Task is done, and there are no upcoming iterations."""


class Task(ABC):
    """
    Interface for a thing that needs to be done on some schedule, optionally under
    certain conditions.

    Example Use Cases:
    - Take a pill every 8 hours (condition would be: last pill taken > 8 hours ago)
    - Take Pill XYZ:
        - no sooner than every 6 hours
        - AND no sooner than 4 hours after Pill ABC
    - Clean drain 2x per day, no sooner than 6 hours apart
    - Do XYZ 1x per day, no sooner than 12 hours after Pill ABC

    Ultimately, these tasks will should be easily displayed in some view, so we want a
    few methods that allow us to:
    - determine if the task is due
    - how long until the next task *needs* to be done or *can* be done (depending on
      whether the task is required or optional)
    - the task's current status (e.g.: required, optional, pending, done, etc...)
    """

    entries: list[TaskCompletionEntry]

    def import_from_file(self, filepath: str | Path, fail_silently: bool = False) -> list[Task]
        """
        Imports and returns a list of Tasks from a file. If the file cannot be imported,
        an ImportError is raised unless fail_silently is True, in which case False is
        returned.

        Args:
            filepath (str | Path): The path to the file to import.
            fail_silently (bool): Determines whether to return None or raise an
                ImportError if the file cannot be imported.
        
        Returns:
            list[Task]: The list of Tasks imported from the file.
        """
        spec = _importutil.spec_from_file_location(
            name=self.name,
            location=self.filepath,
            submodule_search_locations=self._submodule_paths,
        )
        self._module = _importutil.module_from_spec(spec)
        try:
            spec.loader.exec_module(self._module)
        except Exception as e:
            if fail_silently:
                ## print(f"Failed to load plugin: {self.name=} {self.filepath=}")
                ## print(e)
                return False
            else:
                raise PluginLoadError(
                    f"Error loading plugin '{self.name}': {e}: {e.args}"
                )

    @abstractmethod
    def next_iteration(self) -> DateTime:
        pass

    def is_due(self) -> bool:
        return self.next_iteration() <= DateTime()

    def time_until_due(self) -> TimeDelta:
        """
        Returns the time until the task is due. If the task is already due, this should
        return a negative timedelta.
        """
        return self.next_iteration() - DateTime()

    @abstractmethod
    def status(self) -> TaskStatus:
        pass


class TaskCompletionEntry(BaseModel):
    """
    Represents a single instance of a task being completed. This could be as simple as
    a timestamp, or could include more information like the user who completed the task,
    the location where the task was completed, etc...
    """

    task: Task
    author: str
    timestamp: int
    notes: str
    # ... other fields as needed
