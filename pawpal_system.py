"""Core classes for the PawPal+ pet care planner."""

from dataclasses import dataclass, field
from datetime import date, timedelta


@dataclass
class Task:
    """Represent one care task for a pet."""

    description: str
    due_date: date
    time: str
    duration_minutes: int
    priority: str = "medium"
    frequency: str = "once"
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def update_details(
        self,
        description: str,
        due_date: date,
        time: str,
        duration_minutes: int,
        priority: str,
        frequency: str,
    ) -> None:
        """Update task details while preserving completion status."""
        if not description.strip():
            raise ValueError("Task description cannot be empty.")

        if duration_minutes <= 0:
            raise ValueError("Task duration must be greater than zero.")

        if priority not in ("low", "medium", "high"):
            raise ValueError("Priority must be low, medium, or high.")

        if frequency not in ("once", "daily", "weekly"):
            raise ValueError("Frequency must be once, daily, or weekly.")

        self.description = description.strip()
        self.due_date = due_date
        self.time = time
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.frequency = frequency


@dataclass
class Pet:
    """Represent a pet and its care tasks."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        self.tasks.append(task)


@dataclass
class Owner:
    """Represent an owner, their pets, and available care time."""

    name: str
    available_minutes: int
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[tuple[Pet, Task]]:
        """Return pet-task pairs across all of this owner's pets."""
        all_tasks = []

        for pet in self.pets:
            for task in pet.tasks:
                all_tasks.append((pet, task))

        return all_tasks


class Scheduler:
    """Organize care tasks retrieved through Owner.get_all_tasks()."""

    def __init__(self, owner: Owner) -> None:
        """Connect this scheduler to an owner."""
        self.owner = owner

    def sort_by_time(self) -> list[tuple[Pet, Task]]:
        """Return pet-task pairs ordered by due date and time."""
        return sorted(
            self.owner.get_all_tasks(),
            key=lambda pair: (pair[1].due_date, pair[1].time),
        )

    def filter_tasks(
        self,
        pet_name: str | None = None,
        completed: bool | None = None,
        due_date: date | None = None,
    ) -> list[tuple[Pet, Task]]:
        """Return pet-task pairs matching the optional filters."""
        matching_tasks = []

        for pet, task in self.owner.get_all_tasks():
            if (
                pet_name is not None
                and pet.name.casefold() != pet_name.casefold()
            ):
                continue

            if completed is not None and task.completed != completed:
                continue

            if due_date is not None and task.due_date != due_date:
                continue

            matching_tasks.append((pet, task))

        return matching_tasks

    def generate_daily_plan(
        self,
        due_date: date,
    ) -> tuple[list[tuple[Pet, Task]], list[str]]:
        """Select pending tasks by priority within the daily time budget."""
        if self.owner.available_minutes < 0:
            raise ValueError("Available care time cannot be negative.")

        priority_order = {"high": 0, "medium": 1, "low": 2}

        candidates = self.filter_tasks(
            completed=False,
            due_date=due_date,
        )

        for pet, task in candidates:
            if task.duration_minutes <= 0:
                raise ValueError("Task duration must be greater than zero.")

            if task.priority not in priority_order:
                raise ValueError("Priority must be low, medium, or high.")

        # Consider higher priorities first, then earlier start times.
        candidates = sorted(
            candidates,
            key=lambda pair: (
                priority_order[pair[1].priority],
                pair[1].time,
            ),
        )

        selected = []
        explanations = []
        remaining_minutes = self.owner.available_minutes

        for pet, task in candidates:
            label = f"{pet.name}: {task.description}"

            if task.duration_minutes <= remaining_minutes:
                selected.append((pet, task))
                remaining_minutes -= task.duration_minutes

                explanations.append(
                    f"Selected {label} ({task.priority} priority, "
                    f"{task.duration_minutes} min); "
                    f"{remaining_minutes} min remaining."
                )
            else:
                explanations.append(
                    f"Skipped {label}: needs {task.duration_minutes} min, "
                    f"but only {remaining_minutes} min remain."
                )

        # Display the selected tasks chronologically.
        selected = sorted(
            selected,
            key=lambda pair: pair[1].time,
        )

        return selected, explanations

    def mark_task_complete(self, pet: Pet, task: Task) -> None:
        """Complete a task and create its next occurrence if recurring."""
        if not any(owned_pet is pet for owned_pet in self.owner.pets):
            raise ValueError("This pet does not belong to this owner.")

        if not any(pet_task is task for pet_task in pet.tasks):
            raise ValueError("This task does not belong to this pet.")

        # Avoid creating duplicate occurrences on repeated completion.
        if task.completed:
            return

        task.mark_complete()

        if task.frequency == "daily":
            interval = timedelta(days=1)
        elif task.frequency == "weekly":
            interval = timedelta(days=7)
        else:
            return

        next_task = Task(
            description=task.description,
            due_date=task.due_date + interval,
            time=task.time,
            duration_minutes=task.duration_minutes,
            priority=task.priority,
            frequency=task.frequency,
        )

        pet.add_task(next_task)

    def detect_conflicts(self) -> list[str]:
        """Warn when incomplete tasks share the same date and start time."""
        warnings = []
        tasks_by_slot = {}

        for pet, task in self.owner.get_all_tasks():
            if task.completed:
                continue

            slot = (task.due_date, task.time)

            if slot not in tasks_by_slot:
                tasks_by_slot[slot] = []

            tasks_by_slot[slot].append((pet, task))

        for (due_date, time), tasks in sorted(tasks_by_slot.items()):
            if len(tasks) > 1:
                descriptions = [
                    f"{pet.name}: {task.description}"
                    for pet, task in tasks
                ]

                warnings.append(
                    f"Conflict on {due_date.isoformat()} at {time}: "
                    + "; ".join(descriptions)
                )

        return warnings