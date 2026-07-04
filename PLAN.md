# PawPal+ Scheduling Algorithm Improvements — Implementation Plan

These are targeted algorithmic improvements to `pawpal_system.py`.
The UI (`app.py`) requires minimal changes unless noted.

---

## 1. Duration-aware conflict detection

**File:** `pawpal_system.py` — `Scheduler.detect_conflicts()`

**Problem:** Currently flags conflicts only on exact `HH:MM` match. A 30-min walk at 07:30 and a 60-min vet appointment at 07:45 overlap in real time but are not caught.

**Fix:**
- Add a helper that converts `"HH:MM"` string → total minutes (e.g. `"07:30"` → 450).
- Compute each task's end time as `start_minutes + duration_minutes`.
- Two tasks conflict if `A.start < B.end and B.start < A.end` (standard interval overlap check).
- Group tasks by `due_date` before checking — only tasks on the same date can overlap.

```python
def _to_minutes(time_str: str) -> int:
    h, m = map(int, time_str.split(":"))
    return h * 60 + m
```

---

## 2. Priority tie-breaking in sort

**File:** `pawpal_system.py` — `Scheduler.sort_by_time()`

**Problem:** When two tasks share the same `scheduled_time`, sort order is arbitrary.

**Fix:** Add a secondary sort key using a priority rank mapping.

```python
PRIORITY_RANK = {"high": 0, "medium": 1, "low": 2}

def sort_by_time(self) -> list:
    return sorted(
        self.get_schedule(),
        key=lambda x: (x[1].scheduled_time, PRIORITY_RANK.get(x[1].priority, 99))
    )
```

---

## 3. Conflict severity scoring

**File:** `pawpal_system.py` — `Scheduler.detect_conflicts()`

**Problem:** All conflict warnings look identical. A high-vs-high clash is more urgent than low-vs-low.

**Fix:** After detecting a conflict, compare the priorities of the two colliding tasks and prepend a severity label to the warning string.

```python
PRIORITY_RANK = {"high": 0, "medium": 1, "low": 2}

def _conflict_severity(p1: str, p2: str) -> str:
    combined = PRIORITY_RANK.get(p1, 99) + PRIORITY_RANK.get(p2, 99)
    if combined <= 1:
        return "[CRITICAL]"
    elif combined <= 3:
        return "[MODERATE]"
    else:
        return "[LOW]"
```

Use it inside `detect_conflicts()` when building the warning string.

---

## 4. 7-day schedule projection (`project_week`)

**File:** `pawpal_system.py` — new method on `Scheduler`

**Problem:** The app only shows tasks for today (`due_date = date.today()`). The spec calls for a weekly schedule view.

**Fix:** Add `project_week()` that walks each task's frequency forward from its `due_date` and returns all occurrences in the next 7 days.

```python
from datetime import date, timedelta

def project_week(self) -> list:
    """
    Returns a list of (due_date, pet_name, task) tuples for the next 7 days.
    Respects task frequency: daily tasks repeat each day, weekly tasks repeat
    every 7 days, 'once' tasks appear only on their due_date if it falls in range.
    """
    today = date.today()
    window_end = today + timedelta(days=7)
    result = []

    for pet_name, task in self.get_schedule():
        current = task.due_date
        while current <= window_end:
            if current >= today:
                result.append((current, pet_name, task))
            if task.frequency == "daily":
                current += timedelta(days=1)
            elif task.frequency == "weekly":
                current += timedelta(weeks=1)
            else:  # "once"
                break

    return sorted(result, key=lambda x: (x[0], x[2].scheduled_time))
```

**UI note:** In `app.py`, call `scheduler.project_week()` and display a table grouped by date, or use `st.tabs()` — one tab per day.

---

## Implementation priority

| # | Improvement | Impact | Effort |
|---|-------------|--------|--------|
| 4 | `project_week()` | High — unlocks weekly view | Medium |
| 1 | Duration-aware conflicts | High — closes known detection gap | Low |
| 3 | Conflict severity labels | Medium — makes warnings actionable | Low |
| 2 | Priority tie-breaking sort | Low — polish | Trivial |
