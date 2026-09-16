import streamlit as st

from src.database.db import create_subject


@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id):

    st.write(
        "Enter the details of the new subject."
    )

    subject_code = st.text_input(
        "Subject Code",
        placeholder="CS101"
    )

    subject_name = st.text_input(
        "Subject Name",
        placeholder="Introduction to Computer Science"
    )

    section = st.text_input(
        "Section",
        placeholder="A"
    )

    if st.button(
        "Create Subject Now",
        type="primary",
        width="stretch"
    ):

        if not subject_code or not subject_name or not section:

            st.warning(
                "Please fill all the fields."
            )

            return

        try:

            create_subject(
                subject_code,
                subject_name,
                section,
                teacher_id
            )

            st.toast(
                "Subject created successfully!"
            )

            st.rerun()

        except Exception as error:

            st.error(
                f"Error: {error}"
            )