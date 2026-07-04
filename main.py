"""
main.py
-------
CLI demo script for PawPal+. Used to verify that the backend logic
in pawpal_system.py works correctly before connecting it to the UI.

Run with:  python main.py
"""

from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import date

# --- Create the owner (one per session) ---
owner = Owner(name="Jordan")

# --- Create two pets ---
mochi = Pet(name="Mochi", species="dog")
luna = Pet(name="Luna", species="cat")

# --- Add tasks to Mochi ---
# Each task has: name, scheduled_time (HH:MM), duration_minutes, priority, frequency
mochi.add_task(Task("Morning walk",    "07:30", 30, "high",   "daily"))
mochi.add_task(Task("Evening walk",    "18:00", 30, "high",   "daily"))
mochi.add_task(Task("Flea medication", "09:00", 5,  "medium", "weekly"))

# --- Add tasks to Luna ---
luna.add_task(Task("Feeding",          "08:00", 10, "high",   "daily"))
luna.add_task(Task("Grooming",         "11:00", 20, "medium", "weekly"))

# --- Register pets with the owner ---
owner.add_pet(mochi)
owner.add_pet(luna)

# --- Create the Scheduler and generate today's schedule ---
scheduler = Scheduler(owner)

print(f"\n{'='*45}")
print(f"  Today's Schedule for {owner.name}")
print(f"  Date: {date.today()}")
print(f"{'='*45}")

# Print all tasks sorted by scheduled time (earliest first)
for pet_name, task in scheduler.sort_by_time():
    print(f"  [{pet_name}]  {task}")

# --- Check for scheduling conflicts ---
# Conflicts occur when two tasks share the same time slot on the same date
conflicts = scheduler.detect_conflicts()
if conflicts:
    print(f"\nConflicts detected:")
    for warning in conflicts:
        print(f"  {warning}")
else:
    print(f"\nNo scheduling conflicts.")

print(f"{'='*45}\n")
