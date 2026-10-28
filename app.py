"""Streamlit interface for the PawPal+ pet care planner."""

from datetime import date, time

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task


def task_rows(pairs):
    """Convert pet-task pairs into readable table rows."""
    return [
        {
            "Date": task.due_date.isoformat(),
            "Time": task.time,
            "Pet": pet.name,
            "Task": task.description,
            "Minutes": task.duration_minutes,
            "Priority": task.priority,
            "Frequency": task.frequency,
            "Status": "Complete" if task.completed else "Pending",
        }
        for pet, task in pairs
    ]


st.set_page_config(
    page_title="PawPal+",
    page_icon="🐾",
    layout="centered",
)

st.title("🐾 PawPal+")
st.write("Add your pets, organize care tasks, and build a daily plan.")

# Preserve the Owner object during interactions in this session.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(
        name="Haida",
        available_minutes=60,
    )

owner = st.session_state.owner
scheduler = Scheduler(owner)

# Display feedback after actions that trigger a rerun.
if "feedback" in st.session_state:
    st.success(st.session_state.pop("feedback"))


st.subheader("Owner Information")

with st.form("owner_form"):
    owner_name = st.text_input("Owner name", value=owner.name)

    available_minutes = st.number_input(
        "Available care time per day (minutes)",
        min_value=0,
        value=owner.available_minutes,
        step=5,
    )

    save_owner = st.form_submit_button("Save owner")

if save_owner:
    if owner_name.strip():
        owner.name = owner_name.strip()
        owner.available_minutes = int(available_minutes)
        st.success("Owner information saved.")
    else:
        st.error("Please enter an owner name.")


st.divider()
st.subheader("Add a Pet")

with st.form("pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    add_pet = st.form_submit_button("Add pet")

if add_pet:
    if pet_name.strip():
        pet = Pet(name=pet_name.strip(), species=species)
        owner.add_pet(pet)
        st.success(f"{pet.name} added.")
    else:
        st.error("Please enter a pet name.")

if owner.pets:
    st.write("Your pets:")
    st.table([
        {"Name": pet.name, "Species": pet.species}
        for pet in owner.pets
    ])
else:
    st.info("No pets yet. Add one above.")


st.divider()
st.subheader("Schedule a Task")

if owner.pets:
    with st.form("task_form", clear_on_submit=True):
        pet_index = st.selectbox(
            "Choose a pet",
            options=list(range(len(owner.pets))),
            format_func=lambda index: (
                f"{owner.pets[index].name} "
                f"({owner.pets[index].species}) — Pet {index + 1}"
            ),
        )

        description = st.text_input("Task description")
        due_date = st.date_input("Due date", value=date.today())
        task_time = st.time_input("Time", value=time(8, 0))

        duration = st.number_input(
            "Duration (minutes)",
            min_value=1,
            max_value=240,
            value=20,
        )

        priority = st.selectbox(
            "Priority",
            ["low", "medium", "high"],
            index=1,
        )

        frequency = st.selectbox(
            "Frequency",
            ["once", "daily", "weekly"],
        )

        add_task = st.form_submit_button("Add task")

    if add_task:
        if description.strip():
            selected_pet = owner.pets[pet_index]

            task = Task(
                description=description.strip(),
                due_date=due_date,
                time=task_time.strftime("%H:%M"),
                duration_minutes=int(duration),
                priority=priority,
                frequency=frequency,
            )

            selected_pet.add_task(task)
            st.success(f"Task added for {selected_pet.name}.")
        else:
            st.error("Please enter a task description.")
else:
    st.info("Add a pet before scheduling a task.")


st.divider()
st.subheader("Edit or Complete a Task")

all_tasks = owner.get_all_tasks()

if all_tasks:
    selected_index = st.selectbox(
        "Choose a task",
        options=list(range(len(all_tasks))),
        format_func=lambda index: (
            f"{all_tasks[index][0].name} — "
            f"{all_tasks[index][1].description} — "
            f"{all_tasks[index][1].due_date.isoformat()} "
            f"{all_tasks[index][1].time} — Task {index + 1}"
        ),
        key="manage_task_selection",
    )

    selected_pet, selected_task = all_tasks[selected_index]

    st.write(
        "Status:",
        "Complete" if selected_task.completed else "Pending",
    )

    # Separate widget keys keep each task's editing fields independent.
    edit_key = f"edit_task_{selected_index}"

    with st.form(f"{edit_key}_form"):
        edited_description = st.text_input(
            "Task description",
            value=selected_task.description,
            key=f"{edit_key}_description",
        )

        edited_date = st.date_input(
            "Due date",
            value=selected_task.due_date,
            key=f"{edit_key}_date",
        )

        edited_time = st.time_input(
            "Time",
            value=time.fromisoformat(selected_task.time),
            key=f"{edit_key}_time",
        )

        edited_duration = st.number_input(
            "Duration (minutes)",
            min_value=1,
            value=selected_task.duration_minutes,
            step=1,
            key=f"{edit_key}_duration",
        )

        priorities = ["low", "medium", "high"]
        edited_priority = st.selectbox(
            "Priority",
            priorities,
            index=priorities.index(selected_task.priority),
            key=f"{edit_key}_priority",
        )

        frequencies = ["once", "daily", "weekly"]
        edited_frequency = st.selectbox(
            "Frequency",
            frequencies,
            index=frequencies.index(selected_task.frequency),
            key=f"{edit_key}_frequency",
        )

        save_task = st.form_submit_button("Save task changes")

    if save_task:
        try:
            selected_task.update_details(
                description=edited_description,
                due_date=edited_date,
                time=edited_time.strftime("%H:%M"),
                duration_minutes=int(edited_duration),
                priority=edited_priority,
                frequency=edited_frequency,
            )
        except ValueError as error:
            st.error(str(error))
        else:
            st.session_state.feedback = "Task changes saved."
            st.rerun()

    st.caption(
        "Save any edits before completing the task. Daily and weekly "
        "tasks create their next occurrence when completed. "
        "Editing a completed task does not update an occurrence "
        "that was already created."
    )

    if st.button(
        "Mark selected task complete",
        disabled=selected_task.completed,
    ):
        try:
            scheduler.mark_task_complete(selected_pet, selected_task)
        except ValueError as error:
            st.error(str(error))
        else:
            st.session_state.feedback = (
                f"Completed {selected_task.description} "
                f"for {selected_pet.name}."
            )
            st.rerun()
else:
    st.info("Add a task before editing or completing one.")


st.divider()
st.subheader("View Schedule")

schedule_date = st.date_input(
    "Schedule date",
    value=date.today(),
    key="schedule_date",
)

# Combine identical names because the backend filters by pet name.
pet_names = list(dict.fromkeys(pet.name for pet in owner.pets))

pet_filter = st.selectbox(
    "Filter by pet",
    options=[None] + pet_names,
    format_func=lambda name: "All pets" if name is None else name,
)

status_filter = st.selectbox(
    "Filter by status",
    ["All", "Pending", "Complete"],
)

completion_filter = {
    "All": None,
    "Pending": False,
    "Complete": True,
}[status_filter]

filtered_tasks = scheduler.filter_tasks(
    pet_name=pet_filter,
    completed=completion_filter,
    due_date=schedule_date,
)

filtered_tasks = sorted(
    filtered_tasks,
    key=lambda pair: (pair[1].due_date, pair[1].time),
)

if filtered_tasks:
    st.table(task_rows(filtered_tasks))
else:
    st.info("No tasks match these filters.")


st.subheader("Conflict Warnings")

st.caption(
    "Checks incomplete tasks across all pets and dates, regardless of "
    "the display filters. Warnings identify identical start times; "
    "overlapping durations are not checked."
)

warnings = scheduler.detect_conflicts()

if warnings:
    for warning in warnings:
        st.warning(warning)
else:
    st.success("No tasks share the same date and start time.")


st.divider()
st.subheader("Build a Daily Plan")

plan_date = st.date_input(
    "Plan date",
    value=date.today(),
    key="plan_date",
)

st.write(
    f"Saved care-time budget: **{owner.available_minutes} minutes**"
)

st.caption(
    "The plan considers pending tasks across all pets on the selected "
    "date. It tries high priority first, then medium and low, using "
    "earlier times to break ties. Selected tasks display chronologically."
)

st.caption(
    "Tasks keep their scheduled start times. Planning limits total care "
    "minutes but does not resolve conflicts or duration overlaps."
)

if st.button("Generate daily plan"):
    try:
        selected, explanations = scheduler.generate_daily_plan(plan_date)
    except ValueError as error:
        st.error(str(error))
    else:
        if selected:
            st.table(task_rows(selected))

            total_minutes = sum(
                task.duration_minutes for pet, task in selected
            )

            st.success(
                f"Selected {len(selected)} task(s), using "
                f"{total_minutes} of {owner.available_minutes} minutes."
            )
        else:
            st.info("No tasks selected for this plan.")

        st.write("Plan explanations:")

        if explanations:
            for explanation in explanations:
                st.write(f"- {explanation}")
        else:
            st.write("No pending tasks are due on this date.")


st.caption(
    "Data stays in the current Streamlit session. "
    "It is not saved permanently."
)