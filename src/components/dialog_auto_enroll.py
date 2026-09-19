import streamlit as st

from src.database.config import supabase
from src.database.db import enroll_student_to_subject


def auto_enroll(subject_code):

    student_data = st.session_state.get("student_data")

    if not student_data:
        st.error("Student information not found.")
        return

    student_id = student_data["student_id"]

    response = (
        supabase
        .table("subjects")
        .select("subject_id, name")
        .eq("subject_code", subject_code)
        .execute()
    )

    if not response.data:
        st.error("Subject Code not found!")

        if st.button(
            "Close",
            width="stretch"
        ):
            st.query_params.clear()
            st.rerun()

        return

    subject = response.data[0]
    subject_id = subject["subject_id"]

    check = (
        supabase
        .table("subject_students")
        .select("*")
        .eq("subject_id", subject_id)
        .eq("student_id", student_id)
        .execute()
    )

    if check.data:
        st.info("You're already enrolled!")

        if st.button(
            "Got it!",
            width="stretch"
        ):
            st.query_params.clear()
            st.rerun()

        return

    st.header("Quick Enrollment")

    st.write(
        f"Would you like to enroll in "
        f"**{subject['name']}**?"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "No thanks",
            width="stretch"
        ):
            st.query_params.clear()
            st.rerun()

    with col2:

        if st.button(
            "Yes, enroll now!",
            type="primary",
            width="stretch"
        ):

            try:

                result = enroll_student_to_subject(
                    student_id,
                    subject_id
                )

                if not result:
                    st.error(
                        "Could not enroll in this subject."
                    )
                    return

                st.success("Joined successfully!")

                # app.py handles the rest on the next run:
                # sets student session state and clears query params
                st.session_state["quick_enrollment_completed"] = True

                st.rerun(scope="app")

            except Exception as error:

                st.error(
                    f"Enrollment failed: {error}"
                )