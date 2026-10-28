"""Tests for PawPal+ core task behavior."""

from datetime import date

from pawpal_system import Pet, Task


def test_task_completion():
    """Completing a task changes its status."""
    task = Task(
        description="Breakfast",
        due_date=date(2026, 10, 27),
        time="08:00",
        duration_minutes=10,
    )

    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_pet_task_addition():
    """Adding a task increases the pet's task count."""
    pet = Pet(name="Luna", species="cat")
    task = Task(
        description="Breakfast",
        due_date=date(2026, 10, 27),
        time="08:00",
        duration_minutes=10,
    )

    initial_count = len(pet.tasks)

    pet.add_task(task)

    assert len(pet.tasks) == initial_count + 1
    assert pet.tasks[0] is task