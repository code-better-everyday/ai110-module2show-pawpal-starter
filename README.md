# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Run the CLI demo with: `python main.py`

```
==================================================
  Today's Schedule for Jordan
  Date: 2026-07-04
==================================================
  [Mochi ]  [ ] 07:30 | Morning walk (30 min) [high] [daily]
  [Luna  ]  [ ] 08:00 | Feeding (10 min) [high] [daily]
  [Mochi ]  [ ] 09:00 | Flea medication (5 min) [medium] [weekly]
  [Luna  ]  [ ] 09:00 | Vet appointment (60 min) [high] [once]
  [Luna  ]  [ ] 11:00 | Grooming (20 min) [medium] [weekly]
  [Mochi ]  [ ] 18:00 | Evening walk (30 min) [high] [daily]

--- Conflict Check ---
  Conflicts detected:
  ! Conflict at 09:00 on 2026-07-04: 'Flea medication' and 'Vet appointment'

--- Recurring Task Demo ---
  Before: [ ] 07:30 | Morning walk (30 min) [high] [daily]
  Marking 'Morning walk' complete and scheduling next occurrence...
  After:  [x] 07:30 | Morning walk (30 min) [high] [daily]
  Next:   [ ] 07:30 | Morning walk (30 min) [high] [daily] (due: 2026-07-05)

--- Filter: Incomplete tasks only ---
  [Mochi ]  [ ] 18:00 | Evening walk (30 min) [high] [daily]
  [Mochi ]  [ ] 09:00 | Flea medication (5 min) [medium] [weekly]
  ...

--- Filter: Mochi's tasks only ---
  [Mochi ]  [x] 07:30 | Morning walk (30 min) [high] [daily]
  [Mochi ]  [ ] 18:00 | Evening walk (30 min) [high] [daily]
  ...
==================================================
```

## 🧪 Testing PawPal+

Run the full test suite from the project root:

```bash
python -m pytest tests/test_pawpal.py -v
```

**What the tests cover:**
- **Sorting correctness** — tasks return in chronological HH:MM order
- **Conflict detection** — duplicate time slots are flagged with a warning
- **Recurrence logic** — daily/weekly tasks create the next occurrence after completion; `once` tasks do not
- **Filter by status** — only incomplete (or complete) tasks are returned
- **Filter by pet** — name matching is case-insensitive
- **Edge cases** — empty pet, already-completed task, no match on pet filter

```
============================= test session starts =============================
platform win32 -- Python 3.13.13, pytest-9.1.1, pluggy-1.6.0 -- .venv/Scripts/python.exe
collecting ... collected 14 items

tests/test_pawpal.py::test_task_mark_complete PASSED                     [  7%]
tests/test_pawpal.py::test_pet_task_count_increases_on_add PASSED        [ 14%]
tests/test_pawpal.py::test_sort_by_time_orders_chronologically PASSED    [ 21%]
tests/test_pawpal.py::test_sort_by_time_empty_pet PASSED                 [ 28%]
tests/test_pawpal.py::test_detect_conflicts_same_time_flags_warning PASSED [ 35%]
tests/test_pawpal.py::test_detect_conflicts_different_times_no_warning PASSED [ 42%]
tests/test_pawpal.py::test_handle_recurrence_daily_creates_next_day PASSED [ 50%]
tests/test_pawpal.py::test_handle_recurrence_weekly_creates_seven_days_later PASSED [ 57%]
tests/test_pawpal.py::test_handle_recurrence_once_does_not_add_task PASSED [ 64%]
tests/test_pawpal.py::test_filter_by_status_returns_only_incomplete PASSED [ 71%]
tests/test_pawpal.py::test_filter_by_pet_case_insensitive PASSED         [ 78%]
tests/test_pawpal.py::test_mark_complete_twice_stays_true PASSED         [ 85%]
tests/test_pawpal.py::test_handle_recurrence_not_complete_does_nothing PASSED [ 92%]
tests/test_pawpal.py::test_filter_by_pet_no_match_returns_empty PASSED   [100%]

============================== 14 passed in 0.06s ==============================
```

**Confidence level: ⭐⭐⭐⭐ (4/5)**
The core scheduling behaviors are fully tested. One star held back because conflict detection only checks exact time matches — duration overlaps (e.g. a task at 07:30 for 60 min vs one at 08:00) are not yet caught.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting by time | `Scheduler.sort_by_time()` | Sorts all tasks across all pets chronologically using HH:MM string sort with a lambda key |
| Filter by status | `Scheduler.filter_by_status(completed)` | Returns only completed or only incomplete tasks across all pets |
| Filter by pet | `Scheduler.filter_by_pet(pet_name)` | Returns only tasks belonging to a specific named pet (case-insensitive) |
| Conflict detection | `Scheduler.detect_conflicts()` | Flags any two tasks sharing the exact same scheduled_time and due_date; returns warning strings rather than crashing |
| Recurring tasks | `Scheduler.handle_recurrence(task, pet)` | When a daily or weekly task is marked complete, automatically creates the next occurrence with due_date advanced by 1 or 7 days using `timedelta`; "once" tasks are not re-created |

## 📸 Demo Walkthrough

1. Launch the app with `streamlit run app.py` and open `http://localhost:8501` in your browser.
2. Enter your name in the **Owner name** field and your pet's name and species.
3. Add tasks for your pet — enter a task name, scheduled time (HH:MM), duration, priority, and frequency, then click **Add task**. The task table below updates immediately.
4. Add a second task at the same time as an existing one to see the **conflict warning** appear when you generate the schedule.
5. Click **Generate schedule** to see all tasks sorted chronologically with a conflict check — any time clashes are flagged with a warning message.
