import streamlit as st

from src.database.config import supabase
from src.database.db import enroll_student_to_subject


def auto_enroll(subject_code):

    student_data = st.session_state.get("student_data")

    if not student_data:

        st.error(
            "Student information not found."
        )

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

        st.error(
            "Subject code not found."
        )

        if st.button(
            "Close",
            type="secondary",
            width="stretch",
            icon=":material/close:"
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

        st.subheader(
            "Already Enrolled"
        )

        st.info(
            f"You're already enrolled in **{subject['name']}**."
        )

        if st.button(
            "Got it!",
            type="primary",
            width="stretch",
            icon=":material/check:"
        ):

            st.query_params.clear()
            st.rerun()

        return

    st.subheader(
        "Quick Enrollment"
    )

    st.caption(
        "You've been invited to join a subject."
    )

    st.write("")

    with st.container(
        border=True
    ):

        st.subheader(
            subject["name"]
        )

        st.caption(
            f"Subject Code: {subject_code}"
        )

        st.write(
            "Would you like to enroll in this subject?"
        )

    st.write("")

    col1, col2 = st.columns(
        2,
        gap="small"
    )

    with col1:

        if st.button(
            "No, thanks",
            type="secondary",
            width="stretch",
            icon=":material/close:"
        ):

            st.query_params.clear()
            st.rerun()

    with col2:

        if st.button(
            "Yes, enroll",
            type="primary",
            width="stretch",
            icon=":material/how_to_reg:"
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

                st.success(
                    "Joined successfully!"
                )

                st.session_state[
                    "quick_enrollment_completed"
                ] = True

                st.rerun(
                    scope="app"
                )

            except Exception as error:

                st.error(
                    f"Enrollment failed: {error}"
                )