"""Core classes for the PawPal+ pet care planner."""

from dataclasses import dataclass, field
from datetime import date


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
        """Update this task's care and scheduling details."""
        pass


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
        pass

    def generate_daily_plan(
        self,
        due_date: date,
    ) -> tuple[list[tuple[Pet, Task]], list[str]]:
        """Return selected tasks and explanations within the time budget."""
        pass

    def mark_task_complete(self, pet: Pet, task: Task) -> None:
        """Complete a task and create its next occurrence if recurring."""
        pass

    def detect_conflicts(self) -> list[str]:
        """Return warnings for incomplete tasks sharing a date and time."""
        pass