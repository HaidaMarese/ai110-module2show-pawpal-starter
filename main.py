"""Demonstrate PawPal+ core behavior in the terminal."""

from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def main():
    """Demonstrate sorting, filtering, conflicts, and weekly recurrence."""
    today = date.today()

    owner = Owner(name="Haida", available_minutes=60)

    dog = Pet(name="Mochi", species="dog")
    cat = Pet(name="Luna", species="cat")

    owner.add_pet(dog)
    owner.add_pet(cat)

    # Tasks out of chronological order.
    dog.add_task(
        Task(
            description="Evening walk",
            due_date=today,
            time="18:00",
            duration_minutes=20,
            priority="medium",
        )
    )

    cat.add_task(
        Task(
            description="Breakfast",
            due_date=today,
            time="08:00",
            duration_minutes=10,
            priority="high",
        )
    )

    dog.add_task(
        Task(
            description="Morning walk",
            due_date=today,
            time="09:00",
            duration_minutes=20,
            priority="high",
        )
    )

    scheduler = Scheduler(owner)

    print("Today's Schedule")
    print("-" * 60)

    for pet, task in scheduler.sort_by_time():
        if task.due_date == today:
            status = "Complete" if task.completed else "Pending"

            print(
                f"{task.time} | {pet.name} | "
                f"{task.description} | {status}"
            )

    print("\nMochi's Pending Tasks")
    print("-" * 60)

    for pet, task in scheduler.filter_tasks(
        pet_name="Mochi",
        completed=False,
        due_date=today,
    ):
        print(f"{task.time} | {pet.name} | {task.description}")

    # A deliberate conflict after displaying the original schedule.
    grooming_task = Task(
        description="Grooming",
        due_date=today,
        time="09:00",
        duration_minutes=15,
        frequency="weekly",
    )
    cat.add_task(grooming_task)

    print("\nConflict Warnings")
    print("-" * 60)

    warnings = scheduler.detect_conflicts()

    if warnings:
        for warning in warnings:
            print(warning)
    else:
        print("No conflicts found.")

    print("\nComplete Luna's Weekly Grooming")
    print("-" * 60)

    scheduler.mark_task_complete(cat, grooming_task)

    for pet, task in scheduler.filter_tasks(pet_name="Luna"):
        if task.description == "Grooming":
            status = "Complete" if task.completed else "Pending"

            print(
                f"{task.due_date} | {task.time} | "
                f"{pet.name} | {task.description} | {status}"
            )


if __name__ == "__main__":
    main()