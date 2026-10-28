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
and completion status. Its mark_complete() method updates the completion
status. The update_details() method is still a placeholder.

Pet stores a pet's name, species, and individual task list. Its
add_task() method adds a task to that pet.

Owner stores the owner's name, available care time, and pets.
Its add_pet() method adds pets, and get_all_tasks() returns pet-task
pairs across every pet.

Scheduler receives an Owner and retrieves tasks through
Owner.get_all_tasks(). Its sort_by_time() method orders tasks by
due date and time. The remaining scheduling methods are placeholders.

This structure separates the backend logic from the Streamlit interface.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

The four-class structure has remained consistent during Phase 2.

During planning, the design expanded to include task duration, priority,
and the owner's available care time after reviewing the README.

The skeleton review also led to default values for priority, frequency,
and completion status, along with clearer Scheduler return type hints.

The implementation keeps each task associated with its pet by returning
pet-task pairs from get_all_tasks(). This supports a combined schedule
that identifies which pet needs each activity.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The current scheduler sorts tasks by due date and time. The main.py
demo displays only tasks due today.

Tasks store duration, priority, frequency, and completion status.
Owner stores available care time. These fields are included for later
scheduling features, but the current implementation does not yet use
priority or available time to choose tasks.

I plan to add daily planning that considers incomplete tasks, priority,
and whether task durations fit within the owner's available minutes.
These constraints come from the project requirements.

Owner preferences are not yet modeled.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The current scheduler stores task times as zero-padded HH:MM strings.
This makes the initial implementation straightforward because values
such as 08:00 and 18:00 sort chronologically.

The tradeoff is that this depends on consistent formatting.
Automatic time validation is not implemented yet.

For a later phase, I plan to detect conflicts using exact date-and-time
matches. This is simpler than checking overlapping task durations,
but it will not detect every possible overlap.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used ChatGPT for design guidance, explanations, and code suggestions.
It helped break the assignment into smaller steps and explain how to
work with the project in Windows and VS Code.

AI assistance helped with the class skeletons, core method
implementations, CLI demo, and two initial pytest tests.

Sharing the actual code and requesting a complete update for the current
step was helpful. It made the suggestions easier to apply and kept the
work focused on the current phase.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

I have not yet documented a specific AI suggestion that I rejected.
I will update this section if I modify or reject a suggestion during
the remaining phases.

I checked the suggested implementation by running Python's syntax check,
executing main.py, and running pytest.

The CLI output showed tasks from both pets in chronological order.
The two automated tests passed. These results provide evidence for the
implemented behavior, while the unfinished features still need testing.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I ran two automated tests in tests/test_pawpal.py.

The first verifies that Task.mark_complete() changes completed from
False to True.

The second verifies that Pet.add_task() increases the pet's task count
and stores the supplied task.

Both tests passed. After moving the test file into the tests folder,
I ran pytest again and confirmed that both still passed.

I also ran main.py, which creates one owner, two pets, and three tasks.
The tasks were added out of order and displayed chronologically.

These checks verify basic task management before connecting the backend
to the interface. Dedicated automated tests for sorting and multi-pet
scheduling are still planned.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I have initial confidence in task completion and task addition because
both automated tests passed. The CLI demo also showed the expected
combined schedule for two pets.

The current checks do not cover the complete application.
Filtering, recurring tasks, conflict detection, and time-budget planning
have not been implemented or verified yet.

Next, I would test an owner with no pets, a pet with no tasks, tasks
on different dates, and tasks with matching times.

After implementing recurrence and daily planning, I would test duplicate
completion, zero available minutes, and tasks that exceed the time budget.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am most satisfied with seeing the classes work together in main.py.
The schedule includes tasks from both pets and displays them in the
correct time order.

The two passing tests also give me a starting point for checking
future changes.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

My next priorities are connecting the backend to Streamlit, implementing
the remaining scheduling methods, and expanding the tests.

I would also improve input validation, especially for task times.
After completing the required features, I would consider detecting
overlapping task durations and saving data between application runs.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

I learned that providing clear requirements and actual code helps
make AI suggestions more useful.

I also learned the value of checking the backend before building the
interface. Running the CLI demo and automated tests helped me verify
the implemented behavior instead of assuming the suggested code worked.