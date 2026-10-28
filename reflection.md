# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial design includes four classes: Task, Pet, Owner, and Scheduler.
The three main planned user actions are adding pets, adding or editing
care tasks, and viewing a daily plan across all pets.

Task represents a care activity, such as feeding, walking, or medication.
It stores the description, due date, time, duration, priority, frequency,
and completion status. Its mark_complete() method updates completion
status. The update_details() method remains a placeholder.

Pet stores a pet's name, species, and individual task list. Its
add_task() method adds a task to that pet.

Owner stores the owner's name, available care time, and pets.
Its add_pet() method adds pets, and get_all_tasks() returns pet-task
pairs across every pet.

Scheduler receives an Owner and retrieves tasks through
Owner.get_all_tasks(). It implements chronological sorting, filtering,
recurring task completion, and basic conflict detection.
Daily time-budget planning remains unfinished.

This structure separates the backend logic from the Streamlit interface.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

The four-class structure has remained consistent during implementation.

During planning, the design expanded to include task duration, priority,
and the owner's available care time after reviewing the README.

The design uses pet-task pairs from get_all_tasks() so that each task
remains connected to the correct pet in a combined schedule.

Recurring task completion is handled through Scheduler.mark_task_complete().
This allows the scheduler to mark the original task complete and add
the next occurrence to the correct pet. Task.mark_complete() only
changes completion status.

The Streamlit interface stores the Owner object in session state.
This keeps the owner's pets and tasks available during interactions
instead of creating an empty Owner on every rerun.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The current scheduler sorts tasks by due date and time. It can filter
tasks by pet name, completion status, and due date.

Conflict detection considers incomplete tasks with the same date and
start time across all pets. Recurring task completion uses frequency
to create the next occurrence one day later for daily tasks or seven
days later for weekly tasks.

Tasks also store duration and priority, and Owner stores available
care time. These values do not yet control task selection.

I plan to implement daily planning that considers incomplete tasks,
priority, and whether task durations fit within the owner's available
minutes. These constraints come from the project requirements.

Owner preferences are not yet modeled.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

My scheduler detects conflicts when incomplete tasks share the same
date and start time, including tasks for different pets. This keeps
the algorithm straightforward, but it does not detect overlapping
durations when tasks start at different times.

This is a reasonable starting point for basic conflict warnings.
I verified the behavior through automated tests and a CLI example
involving Mochi's morning walk and Luna's grooming.

Task times are stored as zero-padded HH:MM strings. This makes sorting
straightforward, but it depends on consistent formatting. Automatic
backend time-format validation is not yet implemented.

Recurring tasks use the original due date to calculate the next
occurrence. This preserves the scheduled interval, but completing
an overdue task could create another occurrence that is already overdue.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used ChatGPT for design guidance, explanations, and code suggestions.
It helped break the assignment into smaller steps and explain how to
work with the project in Windows and VS Code.

AI assistance helped with the class skeletons, backend methods,
CLI demo, Streamlit integration, and automated tests.

Sharing the actual code and requesting a complete update for the current
step was helpful. It made the suggestions easier to apply and kept the
work focused on the current feature.

I also used AI to review filter_tasks() for readability. The suggested
revision combined nested conditions while keeping the same behavior.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

I have not documented a specific AI suggestion that I rejected or
modified myself. I do not want to claim a decision that I have not made.

During algorithm review, I accepted the suggested simplification of
filter_tasks(). I then reran the CLI demo and automated tests to check
for unintended changes. The displayed results remained the same,
and all six tests passed.

Throughout implementation, I used Python's syntax check, main.py,
pytest, and the browser interface to check suggested changes.

These checks provide evidence for the behaviors demonstrated, but
they do not prove that every possible input or unfinished feature works.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I ran six automated tests in tests/test_pawpal.py.

The tests verify:

- Task.mark_complete() changes completed from False to True.
- Pet.add_task() increases the task count and stores the supplied task.
- Completing a daily task creates a pending occurrence one day later.
- Completing a weekly task creates a pending occurrence seven days later.
- Tasks for different pets at the same date and time produce a conflict warning.
- Completed tasks and tasks on different dates do not produce a conflict.

The recurrence tests also verify that task details are preserved and
completing the original task again does not create duplicate occurrences.

The latest test run reported six passed tests.

I also ran main.py to check chronological sorting across two pets,
filtering Mochi's pending tasks, displaying a conflict warning, and
creating Luna's next weekly grooming task.

In the browser, I added pets and tasks and checked that today's schedule
displayed tasks from different pets in chronological order.

These checks help catch problems as the backend and interface develop.
Dedicated automated tests for sorting and filtering are still planned.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I have confidence in the specific task, recurrence, and conflict
behaviors covered by the six passing tests. The CLI demo also provides
evidence that sorting and filtering work for the example data.

The current checks do not cover the complete application.
Task editing and daily time-budget planning remain unfinished.
Several backend features still need interface controls.

Next, I would test an owner with no pets, a pet with no tasks, combined
filters, different task dates, and multiple conflicting tasks.

I would also test recurrence across month and year boundaries and
completion attempts involving the wrong pet or owner.

After implementing daily planning, I would test zero available minutes,
tasks longer than the time budget, equal priorities, and tasks that
fit the budget exactly.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

The strongest result so far is seeing the four classes work together
across multiple pets.

The CLI demo shows sorting, filtering, conflict warnings, and weekly
recurrence. The browser interface also lets me add pets and tasks
and view today's schedule.

The six passing tests provide a useful foundation for checking
future changes.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

My next priorities are implementing task editing and daily planning,
connecting the remaining scheduling features to Streamlit, and
expanding the automated tests.

I would improve input validation, especially for task times, and
consider a clearer policy for completing overdue recurring tasks.

After completing the required features, I would consider detecting
overlapping task durations and saving data between application runs.
The current session state does not provide permanent storage.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

I learned that providing clear requirements and actual code makes
AI suggestions more useful.

I also learned the value of verifying the backend through a CLI demo
and automated tests before relying on the interface.

As the lead architect, I need to understand the responsibilities of
each class, review suggested changes, and distinguish demonstrated
behavior from features that are still planned.