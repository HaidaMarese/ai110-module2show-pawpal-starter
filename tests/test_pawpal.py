"""Tests for PawPal+ tasks, scheduling, recurrence, and daily planning."""

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


def test_update_task_details_preserves_completion():
    """Editing updates task details without changing completion status."""
    task = Task(
        description="Breakfast",
        due_date=date(2026, 10, 27),
        time="08:00",
        duration_minutes=10,
        completed=True,
    )

    task.update_details(
        description="  Evening feeding  ",
        due_date=date(2026, 10, 28),
        time="18:00",
        duration_minutes=15,
        priority="high",
        frequency="daily",
    )

    assert task.description == "Evening feeding"
    assert task.due_date == date(2026, 10, 28)
    assert task.time == "18:00"
    assert task.duration_minutes == 15
    assert task.priority == "high"
    assert task.frequency == "daily"
    assert task.completed is True


def test_daily_plan_prioritizes_tasks_within_budget():
    """Higher-priority tasks get the budget before lower-priority tasks."""
    today = date(2026, 10, 28)
    owner = Owner(name="Haida", available_minutes=30)
    dog = Pet(name="Mochi", species="dog")
    cat = Pet(name="Luna", species="cat")

    owner.add_pet(dog)
    owner.add_pet(cat)

    dog.add_task(
        Task(
            description="Enrichment",
            due_date=today,
            time="07:00",
            duration_minutes=20,
            priority="low",
        )
    )

    dog.add_task(
        Task(
            description="Walk",
            due_date=today,
            time="09:00",
            duration_minutes=20,
            priority="high",
        )
    )

    cat.add_task(
        Task(
            description="Feeding",
            due_date=today,
            time="08:00",
            duration_minutes=10,
            priority="high",
        )
    )

    selected, explanations = Scheduler(owner).generate_daily_plan(today)

    assert [task.description for pet, task in selected] == [
        "Feeding",
        "Walk",
    ]
    assert sum(task.duration_minutes for pet, task in selected) == 30
    assert len(explanations) == 3
    assert any(
        "Skipped Mochi: Enrichment" in text
        for text in explanations
    )


def test_daily_plan_skips_long_tasks_and_excludes_ineligible_tasks():
    """Skip oversized tasks and consider only pending tasks on the date."""
    today = date(2026, 10, 28)
    owner = Owner(name="Haida", available_minutes=10)
    pet = Pet(name="Mochi", species="dog")

    owner.add_pet(pet)

    pet.add_task(
        Task(
            description="Long walk",
            due_date=today,
            time="08:00",
            duration_minutes=20,
            priority="high",
        )
    )

    pet.add_task(
        Task(
            description="Feeding",
            due_date=today,
            time="09:00",
            duration_minutes=10,
            priority="medium",
        )
    )

    pet.add_task(
        Task(
            description="Already done",
            due_date=today,
            time="07:00",
            duration_minutes=5,
            completed=True,
        )
    )

    pet.add_task(
        Task(
            description="Tomorrow",
            due_date=today + timedelta(days=1),
            time="10:00",
            duration_minutes=5,
        )
    )

    selected, explanations = Scheduler(owner).generate_daily_plan(today)

    assert [task.description for pet, task in selected] == ["Feeding"]
    assert len(explanations) == 2
    assert any(
        "Skipped Mochi: Long walk" in text
        for text in explanations
    )


def test_daily_plan_with_zero_budget():
    """A zero-minute budget selects no tasks."""
    today = date(2026, 10, 28)
    owner = Owner(name="Haida", available_minutes=0)
    pet = Pet(name="Luna", species="cat")

    owner.add_pet(pet)

    pet.add_task(
        Task(
            description="Breakfast",
            due_date=today,
            time="08:00",
            duration_minutes=10,
        )
    )

    selected, explanations = Scheduler(owner).generate_daily_plan(today)

    assert selected == []
    assert len(explanations) == 1
    assert "Skipped Luna: Breakfast" in explanations[0]


def test_sort_by_time_across_pets_and_dates():
    """Sort tasks across pets by date first, then time."""
    today = date(2026, 10, 28)
    owner = Owner(name="Haida", available_minutes=60)
    dog = Pet(name="Mochi", species="dog")
    cat = Pet(name="Luna", species="cat")

    owner.add_pet(dog)
    owner.add_pet(cat)

    dog.add_task(
        Task("Evening walk", today, "18:00", 20)
    )

    dog.add_task(
        Task(
            "Tomorrow's walk",
            today + timedelta(days=1),
            "07:00",
            20,
        )
    )

    cat.add_task(
        Task("Breakfast", today, "08:00", 10)
    )

    result = Scheduler(owner).sort_by_time()

    assert [
        (pet.name, task.description)
        for pet, task in result
    ] == [
        ("Luna", "Breakfast"),
        ("Mochi", "Evening walk"),
        ("Mochi", "Tomorrow's walk"),
    ]


def test_filter_tasks_combines_pet_status_and_date():
    """Apply all filters together with case-insensitive pet names."""
    today = date(2026, 10, 28)
    owner = Owner(name="Haida", available_minutes=60)
    dog = Pet(name="Mochi", species="dog")
    cat = Pet(name="Luna", species="cat")

    owner.add_pet(dog)
    owner.add_pet(cat)

    matching_task = Task("Morning walk", today, "09:00", 20)
    dog.add_task(matching_task)

    dog.add_task(
        Task(
            "Completed walk",
            today,
            "08:00",
            20,
            completed=True,
        )
    )

    dog.add_task(
        Task(
            "Tomorrow's walk",
            today + timedelta(days=1),
            "09:00",
            20,
        )
    )

    cat.add_task(
        Task("Breakfast", today, "08:00", 10)
    )

    result = Scheduler(owner).filter_tasks(
        pet_name="mochi",
        completed=False,
        due_date=today,
    )

    assert len(result) == 1
    assert result[0][0] is dog
    assert result[0][1] is matching_task