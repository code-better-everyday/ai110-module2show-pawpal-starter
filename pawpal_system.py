from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date


@dataclass
class Task:
    name: str
    scheduled_time: str          # "HH:MM" format
    duration_minutes: int
    priority: str                # "low", "medium", "high"
    frequency: str               # "once", "daily", "weekly"
    completed: bool = False
    due_date: date = field(default_factory=date.today)

    def mark_complete(self) -> None:
        pass

    def __str__(self) -> str:
        pass


@dataclass
class Pet:
    name: str
    species: str
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def task_count(self) -> int:
        pass


@dataclass
class Owner:
    name: str
    pets: list = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass

    def get_all_tasks(self) -> list:
        pass


class Scheduler:
    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    def get_schedule(self) -> list:
        pass

    def sort_by_time(self) -> list:
        pass

    def filter_by_status(self, completed: bool) -> list:
        pass

    def filter_by_pet(self, pet_name: str) -> list:
        pass

    def detect_conflicts(self) -> list:
        pass

    def handle_recurrence(self, task: Task, pet: Pet) -> None:
        pass
