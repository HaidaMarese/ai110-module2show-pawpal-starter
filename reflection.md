# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial design uses four classes: Task, Pet, Owner, and Scheduler.
The three main user actions are adding pets, adding or editing care
tasks, and viewing a daily plan across all pets.

Task represents a care activity, such as feeding, walking, or medication.
It stores the description, due date, time, duration, priority, frequency,
and completion status. Its methods will support updating task details
and marking a task complete.

Pet stores a pet's name, species, and individual task list. It provides
an add_task() method.

Owner stores the owner's name, available care time in minutes, and pets.
Its get_all_tasks() method will return pet-task pairs across all pets,
keeping each task connected to the correct pet.

Scheduler receives an Owner and retrieves tasks through
Owner.get_all_tasks(). It will organize tasks, filter results, generate
daily plans, detect conflicts, and manage recurring task completion.

This structure separates scheduling decisions from data storage and
the Streamlit interface.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Implementation has not started, so I cannot describe implementation
changes yet. During planning, the design expanded to include task
duration, task priority, and the owner's available care time after
reviewing the README requirements.

The design also includes pet-task pairs when collecting tasks across
pets. This will allow the scheduler to identify which pet each task
belongs to.

I will update this section if the design changes during implementation.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The planned scheduler will consider due dates, task times, completion
status, task duration, priority, and the owner's available care time.

For the daily plan, I plan to select incomplete tasks due on the chosen
date, consider higher-priority tasks first, and check whether their
durations fit within the available minutes. Selected tasks will be
displayed chronologically, with explanations for skipped tasks.

I chose these constraints because they directly support the README's
requirements and help an owner understand what can fit into the day.
Owner preferences are not yet modeled in this initial design.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The initial plan is to detect conflicts when incomplete tasks share
the same date and start time. This approach will not detect every
overlap caused by task duration.

This is a reasonable starting point because exact-time checks are
simple to explain and verify, and they meet the basic conflict
detection requirement. Since tasks include durations, overlap
detection would be a useful improvement later.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

So far, I have used ChatGPT to break the assignment into steps,
understand the Windows and VS Code setup, and plan the responsibilities
of the four classes.

Providing the README and reflection template made the guidance more
specific. Reviewing the README revealed that the design needed duration,
priority, and available care time in addition to basic task scheduling.

Prompts that specify the required classes, relationships, and current
phase are useful because they keep the suggested design focused.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

The earlier AI-proposed design focused on task dates, times, and
recurrence. After the README was provided, the proposed design was
revised to include duration, priority, and available care time.

This showed why AI suggestions need to be compared with the actual
project requirements. The revised design better matches the README.

I have not yet verified the generated skeleton or scheduling behavior.
I will review the saved code against the UML and use a CLI demo and
automated tests during later phases.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I have not run behavioral tests yet because this phase focuses on
system design and class skeletons.

My planned tests cover task addition, task completion, chronological
sorting, filtering, multi-pet scheduling, daily and weekly recurrence,
conflict detection, and selecting tasks within an available-time budget.

These tests will help verify that the implementation follows the design
and handles important scheduling situations correctly.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I cannot rate the scheduler's reliability yet because its behavior has
not been implemented and tested.

Important edge cases include an owner with no pets, a pet with no tasks,
zero available minutes, tasks longer than the available time, equal
priorities, and tasks sharing a start time.

I also plan to check that completing a recurring task twice does not
create duplicate future tasks.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

The clearest part of the planning process is separating the project
into four classes with distinct responsibilities. This gives me a
manageable structure for implementing the backend before the interface.

Reading the README also helped identify requirements that could have
been missed in a simpler design.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

After completing the required features, I would consider detecting
overlapping task durations and saving data between application runs.

I would also explore how owner preferences could influence the daily
plan. These improvements would require additional design decisions
and tests.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

My main takeaway so far is that useful AI guidance depends on clear
context. Providing the actual project requirements helps produce a
more appropriate design.

As the lead architect, I still need to understand the suggested
structure, compare it with the requirements, and verify the final
behavior through execution and testing.