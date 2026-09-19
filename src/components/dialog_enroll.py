import time

import streamlit as st

from src.database.config import supabase
from src.database.db import enroll_student_to_subject


@st.dialog("Enroll in Subject")
def enroll_dialog():

    st.subheader(
        "Join a Subject"
    )

    st.caption(
        "Enter the subject code provided by your teacher "
        "to join the class."
    )

    st.write("")

    join_code = st.text_input(
        "Subject Code",
        placeholder="e.g. CS101",
        key="student_subject_code"
    )

    st.caption(
        "You can find the subject code in your teacher's "
        "subject details."
    )

    st.write("")

    if st.button(
        "Enroll Now",
        type="primary",
        width="stretch",
        icon=":material/how_to_reg:"
    ):

        if not join_code:

            st.warning(
                "Please enter a subject code."
            )

            return

        response = (
            supabase
            .table("subjects")
            .select(
                "subject_id, name, subject_code"
            )
            .eq(
                "subject_code",
                join_code.strip()
            )
            .execute()
        )

        if not response.data:

            st.error(
                "Subject code not found."
            )

            return

        subject = response.data[0]

        student_data = st.session_state.get(
            "student_data"
        )

        if not student_data:

            st.error(
                "Student information not found."
            )

            return

        student_id = student_data["student_id"]

        check = (
            supabase
            .table("subject_students")
            .select("*")
            .eq(
                "subject_id",
                subject["subject_id"]
            )
            .eq(
                "student_id",
                student_id
            )
            .execute()
        )

        if check.data:

            st.warning(
                "You are already enrolled in this subject."
            )

            return

        enroll_student_to_subject(
            student_id,
            subject["subject_id"]
        )

        st.success(
            "Successfully enrolled!"
        )

        time.sleep(1)

        st.rerun()