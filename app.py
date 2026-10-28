"""Streamlit interface for the PawPal+ pet care planner."""

from datetime import date, time

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task


st.set_page_config(
    page_title="PawPal+",
    page_icon="🐾",
    layout="centered",
)

st.title("🐾 PawPal+")
st.write("Add your pets and organize their care tasks.")

# The same Owner object between Streamlit interactions.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(
        name="Haida",
        available_minutes=60,
    )

owner = st.session_state.owner
scheduler = Scheduler(owner)


st.subheader("Owner Information")

with st.form("owner_form"):
    owner_name = st.text_input(
        "Owner name",
        value=owner.name,
    )

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
    species = st.selectbox(
        "Species",
        ["dog", "cat", "other"],
    )

    add_pet = st.form_submit_button("Add pet")

if add_pet:
    if pet_name.strip():
        pet = Pet(
            name=pet_name.strip(),
            species=species,
        )

        owner.add_pet(pet)
        st.success(f"{pet.name} added.")
    else:
        st.error("Please enter a pet name.")

if owner.pets:
    st.write("Your pets:")

    st.table([
        {
            "Name": pet.name,
            "Species": pet.species,
        }
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

        due_date = st.date_input(
            "Due date",
            value=date.today(),
        )

        task_time = st.time_input(
            "Time",
            value=time(8, 0),
        )

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
st.subheader("Today's Schedule")

rows = []

for pet, task in scheduler.sort_by_time():
    if task.due_date == date.today():
        rows.append({
            "Time": task.time,
            "Pet": pet.name,
            "Task": task.description,
            "Minutes": task.duration_minutes,
            "Priority": task.priority,
            "Frequency": task.frequency,
            "Status": "Complete" if task.completed else "Pending",
        })

if rows:
    st.table(rows)
else:
    st.info("No tasks scheduled for today.")