# PawPal+ Project Reflection

## 1. System Design

- You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

## 3 core features 
- Add a pet and their tasks and needs
- schedule a task or care item for any pet based on time and calendar availabiliy 
- See today and weekly schgedule of task define for today based on time availabaility and pet care that is important 




**Assumptions**

- **Single owner per session** — the app supports one owner at a time. The Owner is created from the name entered in the UI and stored in session state for the duration of the app session. There is no login or multi-user system.
- **Time as a string** — `scheduled_time` is stored as a plain "HH:MM" string rather than a full datetime object. This keeps the data simple and is sufficient for sorting with a lambda and detecting exact-time conflicts.
- **Date separate from time** — `due_date` is stored as a `date` object (not combined into a datetime). A task is fully identified by its `due_date` + `scheduled_time` together.
- **Priority and frequency as strings** — both are plain strings ("low"/"medium"/"high" and "once"/"daily"/"weekly") rather than enums, to keep the code approachable at this stage.
- **Conflict detection by exact time match** — two tasks conflict if they share the same `scheduled_time` on the same `due_date`. Overlapping durations are not checked in the core design.
- **All pets belong to one owner** — there is no concept of shared pets between owners in this design.
- **Owner name is unique per session** — the app treats the owner name entered in the UI as the single user identity. There is no authentication or duplicate-name detection.
- **Pet name is unique per owner** — each pet added to an owner is assumed to have a distinct name. The app does not prevent two pets with the same name, but filtering and display logic assumes names are unique.

---

**a. Initial design**

I designed a four-class system where each class has a single, clear responsibility.

- **Task** — represents one care activity. It stores the task name, scheduled time (HH:MM format), duration in minutes, priority (low/medium/high), frequency (once/daily/weekly), completion status, and due date. It can mark itself complete and describe itself as a string.

- **Pet** — stores a pet's name and species, and owns a list of Tasks. It is responsible for adding new tasks and reporting how many tasks it has.

- **Owner** — manages a list of Pets. It acts as the top-level container and can retrieve all tasks across every pet in one call.

- **Scheduler** — the "brain" of the system. It takes an Owner and is responsible for all scheduling intelligence: retrieving the full schedule, sorting tasks by time, filtering by completion status or pet name, detecting time conflicts, and handling recurring task logic.

**b. Design changes**

Yes, one relationship in the UML changed during the design review.

The initial diagram used a `1..*` (one-to-many) relationship between Owner and Pet, meaning an Owner had to have at least one Pet. I changed this to `0..*` (zero-to-many) because in real usage an Owner is created first and pets are added afterward. Requiring at least one pet at creation time would make the system harder to use and less realistic.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers two main constraints: **scheduled time** and **completion status**.

- Scheduled time is the primary constraint — tasks are sorted chronologically so the owner sees what needs to happen first. A pet care schedule is inherently time-driven (morning walk before evening walk, feeding at a consistent time).
- Completion status is used for filtering — the owner can view only what still needs to be done, reducing noise from already-completed tasks.
- Frequency (daily/weekly/once) drives recurrence logic — daily tasks automatically reappear the next day when marked complete.

Priority was collected as an attribute but is not yet used as a sort key. Time ordering felt more natural for a daily schedule view; priority-based sorting is noted as a future enhancement.

**b. Tradeoffs**

The scheduler detects conflicts by **exact time match** (same HH:MM on the same date) rather than checking whether task durations overlap.

For example, a 30-minute walk at 07:30 and a 60-minute vet appointment at 07:30 are flagged as a conflict — but a 30-minute walk at 07:30 and a 60-minute appointment at 07:45 are not, even though they overlap in real time.

This is a reasonable tradeoff for this scenario because: pet care tasks are typically planned at fixed times rather than back-to-back, duration overlap detection would require more complex interval logic, and the simpler check still catches the most common mistake (accidentally scheduling two things at the exact same time).

In testing, the UI allowed adding the same task twice at the same time, which triggered a conflict warning as expected — confirming the detection logic works correctly. This also highlighted the need for a duplicate guard in the UI (planned for Phase 6).

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
