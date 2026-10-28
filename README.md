# PawPal+ (Module 2 Project)

PawPal+ is a pet care management project built with Python and Streamlit.
It helps owners organize care activities across multiple pets.

## Scenario

A busy pet owner needs help staying consistent with feeding, walks,
medication, grooming, and appointments.

The completed application will organize tasks, consider time and priority,
and explain the resulting daily plan.

## Current Progress — Phase 2

Implemented:

- Represent care tasks using a Task dataclass.
- Store separate task lists for each Pet.
- Manage multiple pets through an Owner.
- Retrieve tasks across all pets using Owner.get_all_tasks().
- Sort tasks chronologically by due date and time.
- Mark individual tasks complete.
- Demonstrate the backend through a terminal script.
- Verify task completion and task addition with two automated tests.

Still planned:

- Implement task editing.
- Connect the backend classes to the Streamlit interface.
- Filter tasks by pet, date, and completion status.
- Generate daily plans based on available time and priority.
- Create future occurrences of daily and weekly tasks.
- Display conflict warnings.
- Expand the automated test suite.

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

### Run the Streamlit Starter Interface

```bash
python -m streamlit run app.py
```

The Streamlit interface is currently the starter UI. Backend integration
is planned for Phase 3.

## Implementation Summary

### Task

Task represents a single care activity. It stores:

- Description
- Due date
- Time
- Duration in minutes
- Priority
- Frequency
- Completion status

`Task.mark_complete()` changes the completion status to `True`.
`Task.update_details()` remains a stub.

### Pet

Pet stores a name, species, and task list.
`Pet.add_task()` adds a Task to that pet.

Each pet receives its own task list through `field(default_factory=list)`.

### Owner

Owner stores a name, available care time, and pet list.

`Owner.add_pet()` adds a pet.
`Owner.get_all_tasks()` returns `(pet, task)` pairs across every pet.

Keeping the pet associated with each task allows the schedule to show
which pet needs care.

### Scheduler

Scheduler receives an Owner.

`Scheduler.sort_by_time()` retrieves tasks through `Owner.get_all_tasks()`
and sorts them by due date, then time.

Times currently use zero-padded 24-hour `HH:MM` strings, such as `08:00`
and `18:00`. Automatic time-format validation is not yet implemented.

The remaining scheduling methods are stubs for later phases.

## Sample Output

Run:

```bash
python main.py
```

Verified terminal output:

```text
Today's Schedule
------------------------------------------------------------
08:00 | Luna | Breakfast | Pending
09:00 | Mochi | Morning walk | Pending
18:00 | Mochi | Evening walk | Pending
```

The demo creates one owner and two pets. It adds three tasks out of
chronological order, then displays today's tasks in chronological order.

This demonstrates task collection across multiple pets. It does not yet
select tasks using the owner's available-time budget.

## Testing PawPal+

Run the tests:

```bash
python -m pytest
```

The initial suite covers:

- Task completion: `mark_complete()` changes `completed` from `False` to `True`.
- Task addition: `add_task()` increases the pet's task count and stores
  the supplied task.

Verified test result:

```text
tests\test_pawpal.py ..                                        [100%]

2 passed in 0.06s
```

These tests verify basic task behavior. Chronological sorting and
multi-pet scheduling were checked through the CLI demo. Dedicated
automated tests for sorting and the remaining scheduling features
are still planned.

## Smarter Scheduling

| Feature | Method | Current Status |
|---------|--------|----------------|
| Chronological sorting | `Scheduler.sort_by_time()` | Implemented; demonstrated through `main.py` |
| Filtering | `Scheduler.filter_tasks()` | Planned; currently a stub |
| Daily planning | `Scheduler.generate_daily_plan()` | Planned; currently a stub |
| Conflict warnings | `Scheduler.detect_conflicts()` | Planned; currently a stub |
| Recurring task completion | `Scheduler.mark_task_complete()` | Planned; currently a stub |

`Task.mark_complete()` currently updates status only. It does not create
a recurring task's next occurrence.

## Demo Walkthrough

1. Run `python main.py`.
2. The script creates an Owner named Haida.
3. It adds Mochi the dog and Luna the cat.
4. It assigns three care tasks to the pets.
5. Scheduler retrieves tasks across both pets through `Owner.get_all_tasks()`.
6. Today's tasks print in chronological order with pet names and status.

An interactive browser workflow will be added after backend integration.

## Project Files

- `pawpal_system.py` — Backend classes and scheduling method declarations.
- `main.py` — Terminal demonstration using two pets and three tasks.
- `app.py` — Streamlit starter interface.
- `diagrams/uml.mmd` — Initial Mermaid class diagram.
- `tests/test_pawpal.py` — Automated tests for task completion and task addition.
- `reflection.md` — Design decisions and AI collaboration reflection.
- `requirements.txt` — Project dependencies.

## Development Approach

The project follows a CLI-first workflow:

1. Design the classes and relationships in UML.
2. Create matching Python skeletons.
3. Implement core behavior.
4. Verify behavior with a terminal demo and automated tests.
5. Connect the backend to Streamlit.
6. Add and test the remaining scheduling algorithms.
7. Update the UML, README, and reflection to match the final application.