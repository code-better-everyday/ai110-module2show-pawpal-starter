from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import date

# --- Setup ---
owner = Owner(name="Jordan")

mochi = Pet(name="Mochi", species="dog")
luna = Pet(name="Luna", species="cat")

# Tasks for Mochi
mochi.add_task(Task("Morning walk",    "07:30", 30, "high",   "daily"))
mochi.add_task(Task("Evening walk",    "18:00", 30, "high",   "daily"))
mochi.add_task(Task("Flea medication", "09:00", 5,  "medium", "weekly"))

# Tasks for Luna
luna.add_task(Task("Feeding",          "08:00", 10, "high",   "daily"))
luna.add_task(Task("Grooming",         "11:00", 20, "medium", "weekly"))

owner.add_pet(mochi)
owner.add_pet(luna)

# --- Schedule ---
scheduler = Scheduler(owner)

print(f"\n{'='*45}")
print(f"  Today's Schedule for {owner.name}")
print(f"  Date: {date.today()}")
print(f"{'='*45}")

for pet_name, task in scheduler.sort_by_time():
    print(f"  [{pet_name}]  {task}")

# --- Conflict check ---
conflicts = scheduler.detect_conflicts()
if conflicts:
    print(f"\n⚠ Conflicts detected:")
    for warning in conflicts:
        print(f"  {warning}")
else:
    print(f"\nNo scheduling conflicts.")

print(f"{'='*45}\n")
