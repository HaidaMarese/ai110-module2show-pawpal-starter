# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial design included four classes: Task, Pet, Owner, and Scheduler.
The three main user actions were adding pets, adding or editing care
tasks, and viewing a daily plan across all pets.

Task represents a care activity, such as feeding, walking, or medication.
It stores the description, due date, time, duration, priority, frequency,
and completion status. Its methods support completion and task editing.

Pet stores a pet's name, species, and individual task list.
Its add_task() method adds a task to that pet.

Owner stores the owner's name, available care time, and pets.
Its get_all_tasks() method returns pet-task pairs across all pets.

Scheduler receives an Owner and retrieves tasks through
Owner.get_all_tasks(). It handles sorting, filtering, recurring task
completion, conflict warnings, and daily planning.

This structure separates backend scheduling decisions from the
Streamlit interface.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

The four-class structure remained consistent, but the design became
more detailed during implementation.

During planning, I included duration, priority, and available care time
to support the README requirements.

Recurring completion is handled by Scheduler.mark_task_complete().
This method completes the original task and adds its next occurrence
to the correct pet. Task.mark_complete() only changes status.

The daily planner returns both selected pet-task pairs and explanations.
This allows the CLI and browser interface to show why tasks were
selected or skipped.

The interface stores the Owner object in st.session_state so pets and
tasks remain available during interactions in the current session.

I saved the final UML in diagrams/uml_final.mmd and previewed it
to confirm that the four classes and their relationships rendered.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The scheduler considers due dates, start times, completion status,
duration, priority, frequency, and the owner's available care time.

Daily planning considers only incomplete tasks due on the selected date.
It tries high-priority tasks first, followed by medium and low.
Tasks with equal priority are considered by start time.

A task is selected when its duration fits the remaining budget.
If it does not fit, the scheduler explains why it was skipped and
continues checking other tasks. Selected tasks display chronologically.

I prioritized these constraints because the project requires a plan
that considers time and priority and explains its decisions.

Conflict detection checks incomplete tasks with matching dates and
start times across all pets. Recurrence uses task frequency to create
the next daily or weekly occurrence.

Owner preferences beyond the available-time budget are not modeled.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The daily planner uses a greedy algorithm: it considers higher-priority
tasks first and selects each task that fits the remaining time.

This is straightforward to understand and explain, but it does not
guarantee the largest number of tasks or the best possible combination.
A long high-priority task can leave little time for shorter tasks.

Conflict detection checks identical dates and start times. It does
not detect overlapping durations when tasks start at different times.
The daily planner also does not resolve conflicts or move start times.

These choices keep the initial system manageable and its decisions
visible. More advanced planning would require additional rules and tests.

Recurring tasks use the original due date to calculate the next
occurrence. This preserves the interval, but completing an overdue
task could create another occurrence that is already overdue.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used ChatGPT for design guidance, explanations, code suggestions,
test examples, and documentation updates.

The most useful assistance was breaking the assignment into small steps,
explaining the class relationships, and providing complete code updates
that I could apply in VS Code.

Sharing my actual files and terminal output helped keep the guidance
connected to the current implementation.

AI assistance supported the class skeletons, scheduling methods,
CLI demo, Streamlit integration, Mermaid UML, and automated tests.

During the readability review of filter_tasks(), AI suggested combining
nested conditions while preserving the behavior.

I worked through the phases step by step in the conversation. I did
not use separate chat sessions for every phase, so I cannot compare
that approach from this project.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

I have not documented a specific code suggestion that I independently
rejected or modified. I cannot provide a concrete rejection example
from the work recorded so far.

I accepted the suggested simplification of filter_tasks(), then reran
the CLI demo and tests. The displayed results stayed the same, and
the six tests available at that stage passed.

As the project developed, I expanded the suite to 12 tests and confirmed
that all passed.

I also checked suggested changes using Python's syntax check, main.py,
the browser interface, and the rendered UML.

In the browser, a warning showed two Breakfast tasks at the same time.
This helped distinguish adding another task from editing an existing
task and showed why checking the saved data matters.

I verified daily recurrence by completing Luna's October 27 Breakfast
task and checking that a pending October 28 occurrence appeared with
the same time, duration, priority, and frequency.

These checks provide evidence for specific behaviors. They do not
prove that every input or browser interaction works correctly.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I ran 12 automated tests in tests/test_pawpal.py.

The tests cover:

- Task completion.
- Adding a task to a pet.
- Daily recurrence.
- Weekly recurrence.
- Conflict warnings across different pets.
- Ignoring completed tasks and different dates during conflict checks.
- Editing details while preserving completion status.
- Selecting tasks by priority within a time budget.
- Skipping oversized tasks and excluding completed or other-date tasks.
- Selecting no tasks with a zero-minute budget.
- Sorting across pets and dates.
- Combining pet, completion-status, and date filters.

The recurrence tests also check that task details are preserved and
repeated completion does not create duplicate occurrences.

The latest test run reported:

12 passed in 0.18s

I ran main.py to demonstrate sorting, filtering, conflict warnings,
weekly recurrence, and a 30-minute daily plan.

The CLI plan selected Breakfast and Morning walk and explained why
Evening walk was skipped.

In the browser, I added pets and tasks, viewed a chronological schedule,
generated a plan using the saved time budget, and observed a conflict
warning for matching start times.

I also verified task completion and daily recurrence in the browser.
Luna's October 27 Breakfast task became Complete, and a new Pending
Breakfast appeared on October 28 at 08:00. It preserved the 10-minute
duration, high priority, and daily frequency.

These tests and demonstrations helped verify the implementation
instead of relying only on the suggested code.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I have confidence in the behaviors covered by the 12 passing tests
and the CLI examples. Browser checks also showed task creation,
schedules, time-budget planning, conflict warnings, completion,
and daily recurrence.

My confidence is limited to the cases checked. The tests do not cover
every invalid input or all Streamlit interactions.

Next, I would test:

- An owner with no pets and a pet with no tasks.
- Invalid task descriptions, durations, priorities, and frequencies.
- Recurrence across month and year boundaries.
- Completing a task belonging to another pet or owner.
- Multiple tasks sharing one start time.
- Equal-priority choices under a limited budget.
- Duplicate pet names.
- Browser editing and completion after several reruns.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

The strongest result is seeing the four classes work together across
multiple pets.

The CLI demonstrates sorting, filtering, conflict detection, recurrence,
and daily planning with explanations.

The browser interface connects these backend methods to forms,
schedule filters, completion controls, warnings, and a daily-plan button.

Seeing the next daily Breakfast task appear after completing the
original task confirmed that the browser action reached the backend.

The 12 passing tests provide a useful foundation for checking
future changes, and the final UML makes the structure easier to explain.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would improve backend input validation, especially for time formats,
and add more tests for invalid inputs and empty collections.

I would consider detecting duration overlaps and defining a clearer
policy for overdue recurring tasks.

I would also improve duplicate-task handling and make adding versus
editing tasks clearer in the interface.

Saving data between application runs would be another improvement.
The current session state does not provide permanent storage.
During browser testing, I encountered an empty session and had to
re-enter a pet and task.

I would add more systematic browser checks alongside the backend tests.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

I learned that clear requirements and actual code make AI guidance
more useful, but suggestions still need verification.

The CLI-first workflow helped me check the backend before connecting
it to the browser. Automated tests then helped detect unintended changes.

Being the lead architect means understanding class responsibilities,
checking the results, and distinguishing implemented features from
behaviors that have actually been tested.