import streamlit as st

from src.database.config import supabase
from src.database.db import create_subject


@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id):

    st.subheader(
        "Create a New Subject"
    )

    st.caption(
        "Add the subject details below to create a new class."
    )

    st.write("")

    subject_code = st.text_input(
        "Subject Code",
        placeholder="e.g. CS101"
    )

    subject_name = st.text_input(
        "Subject Name",
        placeholder="e.g. Introduction to Computer Science"
    )

    section = st.text_input(
        "Section",
        placeholder="e.g. A"
    )

    st.write("")

    if st.button(
        "Create Subject",
        type="primary",
        width="stretch",
        icon=":material/add:"
    ):

        if not subject_code or not subject_name or not section:

            st.warning(
                "Please fill all the fields."
            )

            return

        subject_code = subject_code.strip()

        try:

            existing_subject = (
                supabase
                .table("subjects")
                .select("subject_id")
                .eq(
                    "subject_code",
                    subject_code
                )
                .execute()
            )

            if existing_subject.data:

                st.warning(
                    "This subject code already exists. "
                    "Please use another subject code."
                )

                return

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