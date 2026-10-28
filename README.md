# PawPal+ (Module 2 Project)

PawPal+ is a pet care planner built with Python and Streamlit.
It helps owners manage tasks across multiple pets and generate daily
plans based on task priority and available care time.

## Scenario

A busy pet owner needs help staying consistent with feeding, walks,
medication, grooming, and appointments.

PawPal+ organizes these activities, displays schedules, warns about
matching start times, and explains which tasks fit the daily time budget.

## Features

- Store owner information and available care time.
- Add multiple pets with separate task lists.
- Add and edit tasks with dates, times, durations, and priorities.
- Display tasks chronologically across all pets.
- Filter schedules by pet name, date, and completion status.
- Mark tasks complete.
- Create the next occurrence of daily and weekly tasks.
- Prevent repeated completion from creating duplicate occurrences.
- Warn when incomplete tasks share the same date and start time.
- Generate daily plans within the owner's available minutes.
- Explain selected and skipped tasks.
- Preserve data during interactions in the current Streamlit session.
- Verify backend behavior with 12 automated tests.

## Getting Started

Open a terminal inside the project folder.

### Create a Virtual Environment

If `.venv` does not already exist:

```bash
python -m venv .venv
```

### Activate on Windows Command Prompt

```bat
.venv\Scripts\activate.bat
```

### Activate on Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### Activate on macOS or Linux

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Run the Terminal Demo

```bash
python main.py
```

### Run the Streamlit Application

```bash
python -m streamlit run app.py
```

Open the local URL printed in the terminal.

### Run the Tests

```bash
python -m pytest
```

## System Design

The backend uses four classes: Task, Pet, Owner, and Scheduler.

The final Mermaid UML source is available in
[diagrams/uml_final.mmd](diagrams/uml_final.mmd).

The original draft is kept in
[diagrams/uml.mmd](diagrams/uml.mmd).

### Task

Task represents one care activity and stores:

- Description
- Due date
- Start time
- Duration in minutes
- Priority: low, medium, or high
- Frequency: once, daily, or weekly
- Completion status

`Task.mark_complete()` changes completion status to `True`.

`Task.update_details()` updates task details while preserving completion
status. It rejects blank descriptions, nonpositive durations, and
unsupported priority or frequency values.

### Pet

Pet stores a name, species, and task list.

`Pet.add_task()` adds a task to that pet.

Each pet receives an independent task list through
`field(default_factory=list)`.

### Owner

Owner stores a name, available care time in minutes, and a pet list.

`Owner.add_pet()` adds a pet.

`Owner.get_all_tasks()` returns `(pet, task)` pairs across all pets,
keeping each task connected to the pet that needs care.

### Scheduler

Scheduler receives an Owner and retrieves tasks through
`Owner.get_all_tasks()`.

It provides sorting, filtering, recurring task completion, conflict
warnings, and daily planning.

## Smarter Scheduling

| Feature | Method | Behavior |
|---------|--------|----------|
| Chronological sorting | `Scheduler.sort_by_time()` | Orders tasks across all pets by due date and time. |
| Filtering | `Scheduler.filter_tasks()` | Filters by pet name, completion status, and due date. Preserves insertion order. |
| Task editing | `Task.update_details()` | Updates care details while preserving completion status. |
| Conflict warnings | `Scheduler.detect_conflicts()` | Warns when incomplete tasks share the same date and start time, including across pets. |
| Recurring tasks | `Scheduler.mark_task_complete()` | Completes the original task and creates its next daily or weekly occurrence. |
| Daily planning | `Scheduler.generate_daily_plan()` | Selects pending tasks by priority within the available-time budget and returns explanations. |

### Daily Planning Rules

1. Consider only incomplete tasks due on the selected date.
2. Try high-priority tasks first, then medium and low.
3. For equal priorities, consider earlier start times first.
4. Select a task when its duration fits the remaining minutes.
5. Skip tasks that do not fit and continue checking other tasks.
6. Display selected tasks chronologically.
7. Explain each selection or skipped task.

Daily planning does not change task dates, start times, or completion
status.

### Scheduling Tradeoffs and Limitations

- Conflict detection checks identical dates and start times. It does
  not detect overlapping durations with different start times.
- Daily planning limits total care minutes but does not resolve
  conflicts or move tasks into new time slots.
- Priority-based selection uses a greedy approach. It does not
  guarantee the largest possible number of tasks or the best possible
  combination.
- Recurrence is calculated from the original due date: one day later
  for daily tasks and seven days later for weekly tasks. An overdue
  task can therefore create another overdue occurrence.
- Times use zero-padded 24-hour `HH:MM` strings. The browser supplies
  this format; automatic backend time-format validation is not implemented.
- Pet-name filtering is case-insensitive. Pets with matching names
  are included together.
- Editing a completed task does not update a future occurrence that
  has already been created.

Use `Scheduler.mark_task_complete(pet, task)` for recurring tasks.
Calling `Task.mark_complete()` directly changes status only.

## Sample CLI Output

Run:

```bash
python main.py
```

Verified output from a run on October 27, 2026:

```text
Today's Schedule
------------------------------------------------------------
08:00 | Luna | Breakfast | Pending
09:00 | Mochi | Morning walk | Pending
18:00 | Mochi | Evening walk | Pending

Mochi's Pending Tasks
------------------------------------------------------------
18:00 | Mochi | Evening walk
09:00 | Mochi | Morning walk

Conflict Warnings
------------------------------------------------------------
Conflict on 2026-10-27 at 09:00: Mochi: Morning walk; Luna: Grooming

Complete Luna's Weekly Grooming
------------------------------------------------------------
2026-10-27 | 09:00 | Luna | Grooming | Complete
2026-11-03 | 09:00 | Luna | Grooming | Pending

Daily Plan — 30-Minute Budget
------------------------------------------------------------
08:00 | Luna | Breakfast | 10 min | high
09:00 | Mochi | Morning walk | 20 min | high

Plan Explanations
Selected Luna: Breakfast (high priority, 10 min); 20 min remaining.
Selected Mochi: Morning walk (high priority, 20 min); 0 min remaining.
Skipped Mochi: Evening walk: needs 20 min, but only 0 min remain.
```

Dates change because the demo uses `date.today()`.

The filtered section preserves insertion order. The schedule and
selected daily plan display tasks chronologically.

The grooming task is added after the initial schedule is printed,
then completed before the daily plan is generated.

## Testing PawPal+

Run:

```bash
python -m pytest
```

The 12 tests cover:

1. Task completion changes completion status.
2. Task addition stores the supplied task.
3. Daily completion creates the next occurrence.
4. Weekly completion creates the next occurrence.
5. Tasks across pets with matching dates and times produce a warning.
6. Completed tasks and tasks on different dates do not conflict.
7. Task editing updates details and preserves completion status.
8. Daily planning prioritizes tasks within the time budget.
9. Daily planning skips oversized tasks and excludes completed tasks
   and tasks on other dates.
10. A zero-minute budget selects no tasks.
11. Sorting works across pets and dates.
12. Filtering combines pet name, completion status, and date.

The recurrence tests also verify that task details are preserved and
repeated completion does not create duplicate occurrences.

Verified test result:

```text
12 passed in 0.18s
```

These automated tests exercise backend behavior. Browser interactions
are checked separately.

## Demo Walkthrough

### Terminal Demo

1. Run `python main.py`.
2. The script creates Haida as the owner.
3. It adds Mochi the dog and Luna the cat.
4. It adds three tasks out of chronological order.
5. Scheduler displays the combined schedule chronologically.
6. The script filters Mochi's pending tasks.
7. It adds Luna's weekly grooming at the same time as Mochi's walk.
8. Scheduler prints a conflict warning.
9. Completing grooming creates the next weekly occurrence.
10. A 30-minute budget selects Breakfast and Morning walk.
11. Explanations show why Evening walk was skipped.

### Browser Demo

1. Run `python -m streamlit run app.py`.
2. Enter the owner's name and available care time, then click
   **Save owner**.
3. Add Mochi as a dog and Luna as a cat.
4. Under **Schedule a Task**, add these tasks using the same date:

   | Pet | Task | Time | Minutes | Priority | Frequency |
   |-----|------|------|---------|----------|-----------|
   | Luna | Breakfast | 08:00 | 10 | high | daily |
   | Mochi | Morning walk | 09:00 | 20 | high | daily |
   | Mochi | Evening walk | 18:00 | 20 | medium | once |

5. Under **View Schedule**, select that date to see tasks in time order.
6. Try the pet and status filters.
7. Under **Edit or Complete a Task**, select a task, change its details,
   and click **Save task changes**.
8. To demonstrate a conflict, temporarily change Evening walk to 09:00
   on the same date. A warning identifies the matching start times.
   Restore its time to 18:00 afterward.
9. Save an owner budget of 30 minutes and generate a daily plan for
   the task date. Breakfast and Morning walk fit; Evening walk is skipped.
10. Select Breakfast and click **Mark selected task complete**.
11. View the original date with status **Complete** to see the completed task.
12. View the following date with status **Pending** to see its next
    daily occurrence.

## Session Storage

The Owner object is stored in `st.session_state`, keeping pets and tasks
available during interactions in the current browser session.

Data is not saved to disk and may be lost when the session ends or the
application restarts.

## Project Files

| File | Purpose |
|------|---------|
| `pawpal_system.py` | Backend classes and scheduling logic. |
| `main.py` | CLI demonstration across two pets. |
| `app.py` | Streamlit interface for pets, tasks, schedules, and daily plans. |
| `diagrams/uml.mmd` | Original UML draft. |
| `diagrams/uml_final.mmd` | Final UML matching the implemented classes. |
| `tests/test_pawpal.py` | Twelve automated backend tests. |
| `reflection.md` | Design decisions, tradeoffs, verification, and AI collaboration. |
| `requirements.txt` | Project dependencies. |

## Development Approach

The project follows a CLI-first workflow:

1. Design the classes and relationships in UML.
2. Create matching Python skeletons.
3. Implement core behavior.
4. Verify the backend with a terminal demo and automated tests.
5. Connect the backend to Streamlit using session state.
6. Implement sorting, filtering, recurrence, and conflict warnings.
7. Add task editing and daily planning.
8. Connect scheduling features to browser controls.
9. Update the UML, README, and reflection to match the implementation.

## Author

**Haida Makouangou**  
CodePath AI110 — Fall 2026
