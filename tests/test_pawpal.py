"""Tests for PawPal+ task behavior, recurrence, and conflicts."""

from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


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


def test_daily_task_creates_next_occurrence():
    """Completing a daily task creates one pending occurrence."""
    owner = Owner(name="Haida", available_minutes=60)
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)

    task = Task(
        description="Morning walk",
        due_date=date(2026, 10, 28),
        time="09:00",
        duration_minutes=20,
        priority="high",
        frequency="daily",
    )
    pet.add_task(task)

    scheduler = Scheduler(owner)
    scheduler.mark_task_complete(pet, task)

    assert task.completed is True
    assert len(pet.tasks) == 2

    next_task = pet.tasks[1]

    assert next_task is not task
    assert next_task.due_date == task.due_date + timedelta(days=1)
    assert next_task.completed is False
    assert next_task.description == task.description
    assert next_task.time == task.time
    assert next_task.duration_minutes == task.duration_minutes
    assert next_task.priority == task.priority
    assert next_task.frequency == "daily"

    # Repeating completion must not create another occurrence.
    scheduler.mark_task_complete(pet, task)

    assert len(pet.tasks) == 2


def test_weekly_task_creates_next_occurrence():
    """Completing a weekly task creates an occurrence seven days later."""
    owner = Owner(name="Haida", available_minutes=60)
    pet = Pet(name="Luna", species="cat")
    owner.add_pet(pet)

    task = Task(
        description="Grooming",
        due_date=date(2026, 10, 28),
        time="10:00",
        duration_minutes=15,
        priority="medium",
        frequency="weekly",
    )
    pet.add_task(task)

    scheduler = Scheduler(owner)
    scheduler.mark_task_complete(pet, task)

    assert task.completed is True
    assert len(pet.tasks) == 2

    next_task = pet.tasks[1]

    assert next_task is not task
    assert next_task.due_date == task.due_date + timedelta(days=7)
    assert next_task.completed is False
    assert next_task.description == task.description
    assert next_task.time == task.time
    assert next_task.duration_minutes == task.duration_minutes
    assert next_task.priority == task.priority
    assert next_task.frequency == "weekly"

    # Repeating completion must not create another occurrence.
    scheduler.mark_task_complete(pet, task)

    assert len(pet.tasks) == 2


def test_conflicts_across_pets():
    """Tasks for different pets at the same date and time produce a warning."""
    owner = Owner(name="Haida", available_minutes=60)
    dog = Pet(name="Mochi", species="dog")
    cat = Pet(name="Luna", species="cat")

    owner.add_pet(dog)
    owner.add_pet(cat)

    dog.add_task(
        Task(
            description="Morning walk",
            due_date=date(2026, 10, 28),
            time="09:00",
            duration_minutes=20,
        )
    )

    cat.add_task(
        Task(
            description="Breakfast",
            due_date=date(2026, 10, 28),
            time="09:00",
            duration_minutes=10,
        )
    )

    warnings = Scheduler(owner).detect_conflicts()

    assert len(warnings) == 1
    assert "2026-10-28" in warnings[0]
    assert "09:00" in warnings[0]
    assert "Mochi: Morning walk" in warnings[0]
    assert "Luna: Breakfast" in warnings[0]


def test_conflicts_ignore_completed_tasks_and_different_dates():
    """Completed tasks and tasks on different dates do not conflict."""
    owner = Owner(name="Haida", available_minutes=60)
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)

    pet.add_task(
        Task(
            description="Morning walk",
            due_date=date(2026, 10, 28),
            time="09:00",
            duration_minutes=20,
        )
    )

    pet.add_task(
        Task(
            description="Completed feeding",
            due_date=date(2026, 10, 28),
            time="09:00",
            duration_minutes=10,
            completed=True,
        )
    )

    pet.add_task(
        Task(
            description="Tomorrow's walk",
            due_date=date(2026, 10, 29),
            time="09:00",
            duration_minutes=20,
        )
    )

    assert Scheduler(owner).detect_conflicts() == []