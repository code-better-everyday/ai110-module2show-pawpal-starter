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
        """Mark this task as completed."""
        self.completed = True

    def __str__(self) -> str:
        """Return a readable one-line summary of the task."""
        status = "[x]" if self.completed else "[ ]"
        return (
            f"{status} {self.scheduled_time} | {self.name} "
            f"({self.duration_minutes} min) [{self.priority}] [{self.frequency}]"
        )


@dataclass
class Pet:
    name: str
    species: str
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def task_count(self) -> int:
        """Return the number of tasks for this pet."""
        return len(self.tasks)


@dataclass
class Owner:
    name: str
    pets: list = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list:
        """Return a flat list of (pet_name, task) tuples across all pets."""
        result = []
        for pet in self.pets:
            for task in pet.tasks:
                result.append((pet.name, task))
        return result


class Scheduler:
    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    def get_schedule(self) -> list:
        """Return all (pet_name, task) tuples from the owner."""
        return self.owner.get_all_tasks()

    def sort_by_time(self) -> list:
        """Return tasks sorted chronologically by scheduled_time."""
        return sorted(self.get_schedule(), key=lambda x: x[1].scheduled_time)

    def filter_by_status(self, completed: bool) -> list:
        """Return tasks filtered by completion status."""
        return [(pet, task) for pet, task in self.get_schedule()
                if task.completed == completed]

    def filter_by_pet(self, pet_name: str) -> list:
        """Return tasks belonging to a specific pet."""
        return [(pet, task) for pet, task in self.get_schedule()
                if pet.lower() == pet_name.lower()]

    def detect_conflicts(self) -> list:
        """Return warning strings for tasks sharing the same scheduled_time and due_date."""
        seen = {}
        warnings = []
        for pet, task in self.get_schedule():
            key = (task.scheduled_time, task.due_date)
            if key in seen:
                warnings.append(
                    f"Conflict at {task.scheduled_time} on {task.due_date}: "
                    f"'{seen[key]}' and '{task.name}'"
                )
            else:
                seen[key] = task.name
        return warnings

    def handle_recurrence(self, task: Task, pet: Pet) -> None:
        """When a recurring task is completed, create the next occurrence."""
        pass
