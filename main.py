"""Demonstrate PawPal+ core behavior in the terminal."""

from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def main():
    """Create two pets and display today's care tasks."""
    today = date.today()

    owner = Owner(name="Haida", available_minutes=60)

    dog = Pet(name="Mochi", species="dog")
    cat = Pet(name="Luna", species="cat")

    owner.add_pet(dog)
    owner.add_pet(cat)

    # Add tasks out of chronological order.
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


if __name__ == "__main__":
    main()