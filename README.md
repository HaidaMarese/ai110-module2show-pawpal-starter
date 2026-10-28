# PawPal+ (Module 2 Project)

PawPal+ is a pet care management project built with Python and Streamlit.
It helps owners organize care activities across multiple pets.

## Scenario

A busy pet owner needs help staying consistent with feeding, walks,
medication, grooming, and appointments.

The completed application will organize tasks, consider available time
and priority, and explain the resulting daily plan.

## Current Progress — Phase 4

Implemented:

- Represent care activities using a Task dataclass.
- Store separate task lists for each Pet.
- Manage multiple pets through an Owner.
- Retrieve tasks across all pets using Owner.get_all_tasks().
- Sort tasks chronologically by due date and time.
- Filter tasks by pet name, completion status, and due date.
- Mark tasks complete.
- Create the next occurrence when a daily or weekly task is completed.
- Prevent duplicate occurrences when the same task is completed again.
- Detect incomplete tasks sharing the same date and start time.
- Connect the Streamlit interface to the backend for adding pets and tasks.
- Keep owner, pet, and task data in session state during app interactions.
- Display today's tasks in chronological order in the browser.
- Demonstrate scheduling behavior through a terminal script.
- Verify task behavior, recurrence, and conflicts with six automated tests.

Still planned:

- Implement task editing.
- Generate daily plans based on available time and priority.
- Add filtering, task completion, and conflict warnings to the interface.
- Add dedicated automated tests for sorting and filtering.
- Test daily planning once implemented.
- Finalize the UML and project reflection.

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

## Implementation Summary

### Task

Task represents a single care activity. It stores:

- Description
- Due date
- Time
- Duration in minutes
- Priority
- Frequency: once, daily, or weekly
- Completion status

`Task.mark_complete()` changes the completion status to `True`.

`Task.update_details()` remains a stub.

### Pet

Pet stores a name, species, and task list.

`Pet.add_task()` adds a Task to that pet.

Each pet receives its own task list through
`field(default_factory=list)`.

### Owner

Owner stores a name, available care time in minutes, and a pet list.

`Owner.add_pet()` adds a pet.

`Owner.get_all_tasks()` returns `(pet, task)` pairs across all pets.
This keeps each task connected to the pet that needs care.

### Scheduler

Scheduler receives an Owner and retrieves tasks through
`Owner.get_all_tasks()`.

Its implemented methods support:

- Sorting by due date and time.
- Filtering by pet name, completion status, and due date.
- Completing tasks and creating recurring occurrences.
- Detecting tasks with identical dates and start times.

`Scheduler.generate_daily_plan()` remains a stub. Available care time
and task priority are stored but do not yet control task selection.

Times use zero-padded 24-hour `HH:MM` strings, such as `08:00` and
`18:00`. Automatic backend time-format validation is not yet implemented.

## Sample Output

Run:

```bash
python main.py
```

Verified terminal output from a run on October 27, 2026:

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
```

Dates change because the demo uses `date.today()`.

The demo first displays three tasks in chronological order. It then
filters Mochi's pending tasks, preserving their insertion order.

Next, it adds Luna's grooming task at the same time as Mochi's morning
walk to demonstrate a conflict warning. Finally, it completes the
weekly grooming task and displays its next occurrence seven days later.

The demo does not yet select tasks using the owner's available-time
budget.

## Testing PawPal+

Run the tests:

```bash
python -m pytest
```

The six tests cover:

- Task completion changes the completion status.
- Adding a task increases a pet's task count and stores that task.
- Daily completion creates a pending occurrence one day later.
- Weekly completion creates a pending occurrence seven days later.
- Tasks for different pets at the same date and time produce a warning.
- Completed tasks and tasks on different dates do not produce a conflict.

The recurrence tests also check that task details are preserved and
repeated completion does not create duplicate occurrences.

Verified test result:

```text
6 passed in 0.06s
```

Sorting and filtering have been demonstrated through the CLI.
Dedicated automated tests for those methods are still planned.

## Smarter Scheduling

| Feature | Method | Behavior |
|---------|--------|----------|
| Chronological sorting | `Scheduler.sort_by_time()` | Orders tasks across all pets by due date and time. |
| Filtering | `Scheduler.filter_tasks()` | Filters by pet name, completion status, and due date. Preserves insertion order. |
| Conflict warnings | `Scheduler.detect_conflicts()` | Warns when incomplete tasks share the same date and start time, including across pets. |
| Recurring task completion | `Scheduler.mark_task_complete()` | Completes a task and creates its next daily or weekly occurrence. Repeated completion creates no duplicates. |
| Daily planning | `Scheduler.generate_daily_plan()` | Planned; currently a stub. |

### Scheduling Tradeoffs

Conflict detection checks identical dates and start times. It does not
detect overlapping durations when tasks start at different times.

Recurring occurrences are calculated from the original task's due date:
one day later for daily tasks and seven days later for weekly tasks.

Use `Scheduler.mark_task_complete(pet, task)` to complete recurring tasks.
Calling `Task.mark_complete()` directly updates status only.

## Demo Walkthrough

### Terminal Demo

1. Run `python main.py`.
2. The script creates an Owner named Haida.
3. It adds Mochi the dog and Luna the cat.
4. It adds three care tasks out of chronological order.
5. Scheduler gathers tasks across both pets and displays them by time.
6. The script displays Mochi's pending tasks for today.
7. It adds a weekly grooming task that conflicts with Mochi's walk.
8. Scheduler prints a conflict warning.
9. The script completes grooming and displays the next weekly occurrence.

### Browser Demo

1. Run `python -m streamlit run app.py`.
2. Enter the owner's name and available care time, then click Save owner.
3. Enter a pet name and species, then click Add pet.
4. Add another pet to demonstrate multiple-pet support.
5. In Schedule a Task, select the pet and enter the task details.
6. Choose today's date and click Add task.
7. Add another task with a different time.
8. Check Today's Schedule to see the tasks displayed chronologically.

The Owner object is stored in `st.session_state` so pets and tasks
remain available during interactions in the current session.

Data is not saved to disk and may be lost when the session ends or
the application restarts.

Filtering, recurring-task completion, and conflict warnings are currently
demonstrated through the backend and CLI. Their interface controls
are still planned.

## Project Files

- `pawpal_system.py` — Backend classes, sorting, filtering, recurrence, and conflict detection.
- `main.py` — Terminal demonstration using two pets and scheduling examples.
- `app.py` — Streamlit interface for owner information, pets, tasks, and today's schedule.
- `diagrams/uml.mmd` — Working Mermaid class diagram; final review is still planned.
- `tests/test_pawpal.py` — Six automated tests for task behavior, recurrence, and conflicts.
- `reflection.md` — Design decisions, tradeoffs, verification, and AI collaboration reflection.
- `requirements.txt` — Project dependencies.

## Development Approach

The project follows a CLI-first workflow:

1. Design the classes and relationships in UML.
2. Create matching Python skeletons.
3. Implement core behavior.
4. Verify behavior with a terminal demo and automated tests.
5. Connect the backend to Streamlit.
6. Implement and verify scheduling algorithms.
7. Complete daily planning and task editing.
8. Connect the remaining scheduling features to the interface.
9. Update the final UML, README, and reflection to match the application.