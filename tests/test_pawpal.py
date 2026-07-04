from pawpal_system import Task, Pet, Owner, Scheduler
from datetime import date


def test_task_mark_complete():
    """Calling mark_complete() should set completed to True."""
    task = Task("Morning walk", "07:30", 30, "high", "daily")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_pet_task_count_increases_on_add():
    """Adding a task to a Pet should increase its task count by 1."""
    pet = Pet("Mochi", "dog")
    assert pet.task_count() == 0
    pet.add_task(Task("Feeding", "08:00", 10, "high", "daily"))
    assert pet.task_count() == 1
    pet.add_task(Task("Grooming", "11:00", 20, "medium", "weekly"))
    assert pet.task_count() == 2
