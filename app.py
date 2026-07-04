"""
app.py
------
Streamlit UI for PawPal+. Connects the frontend inputs to the
backend logic defined in pawpal_system.py.

Run with:  streamlit run app.py
"""

import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to **PawPal+** — your pet care planning assistant.
Enter your info below, add tasks for your pet, and generate today's schedule.
"""
)

st.divider()

# ── Owner & Pet Setup ──────────────────────────────────────────────────────────
st.subheader("Owner & Pet Info")

owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

# Initialise the Owner in session_state so it persists across button clicks.
# Re-create it only when the owner or pet name changes.
if (
    "owner" not in st.session_state
    or st.session_state.owner.name != owner_name
    or st.session_state.pet_name != pet_name
    or st.session_state.species != species
):
    pet = Pet(name=pet_name, species=species)
    owner = Owner(name=owner_name)
    owner.add_pet(pet)
    st.session_state.owner = owner
    st.session_state.pet_name = pet_name
    st.session_state.species = species

# Convenience references to the live objects stored in session_state
owner = st.session_state.owner
pet = owner.pets[0]  # single pet per session (Phase 3 scope)

st.divider()

# ── Add Tasks ─────────────────────────────────────────────────────────────────
st.subheader("Add a Task")

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task name", value="Morning walk")
with col2:
    scheduled_time = st.text_input("Time (HH:MM)", value="08:00")
with col3:
    duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
with col4:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

frequency = st.selectbox("Frequency", ["daily", "weekly", "once"])

if st.button("Add task"):
    # Create a real Task object and add it to the pet — not a plain dict
    new_task = Task(
        name=task_title,
        scheduled_time=scheduled_time,
        duration_minutes=int(duration),
        priority=priority,
        frequency=frequency,
    )
    pet.add_task(new_task)
    st.success(f"Added '{task_title}' to {pet.name}'s schedule.")

# Show current task list as a table
if pet.task_count() > 0:
    st.markdown(f"**{pet.name}'s tasks ({pet.task_count()} total):**")
    task_rows = [
        {
            "Time": t.scheduled_time,
            "Task": t.name,
            "Duration (min)": t.duration_minutes,
            "Priority": t.priority,
            "Frequency": t.frequency,
            "Done": "[x]" if t.completed else "[ ]",
        }
        for t in pet.tasks
    ]
    st.table(task_rows)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# ── Generate Schedule ──────────────────────────────────────────────────────────
st.subheader("Today's Schedule")

if st.button("Generate schedule"):
    if pet.task_count() == 0:
        st.warning("No tasks added yet. Add at least one task first.")
    else:
        scheduler = Scheduler(owner)

        # Display tasks sorted by scheduled time
        sorted_tasks = scheduler.sort_by_time()
        st.markdown(f"**Schedule for {owner.name} — sorted by time:**")
        schedule_rows = [
            {
                "Time": task.scheduled_time,
                "Pet": pet_name,
                "Task": task.name,
                "Duration (min)": task.duration_minutes,
                "Priority": task.priority,
                "Frequency": task.frequency,
            }
            for pet_name, task in sorted_tasks
        ]
        st.table(schedule_rows)

        # Show any scheduling conflicts
        conflicts = scheduler.detect_conflicts()
        if conflicts:
            st.warning("Scheduling conflicts detected:")
            for c in conflicts:
                st.write(f"  • {c}")
        else:
            st.success("No scheduling conflicts.")
