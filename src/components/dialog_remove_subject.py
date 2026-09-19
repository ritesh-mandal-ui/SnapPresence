import streamlit as st

from src.database.config import supabase
from src.database.db import delete_subject


@st.dialog("Remove Subject")
def remove_subject_dialog(subjects):

    options = {
        f"{subject['name']} - {subject['subject_code']}": subject
        for subject in subjects
    }

    selected_label = st.selectbox(
        "Select subject to remove",
        options=list(options.keys()),
        key="remove_subject_select"
    )

    selected = options[selected_label]

    st.warning(
        f"Are you sure you want to remove "
        f"**{selected['name']}**? Enrolled students and "
        f"attendance records of this subject will also be deleted."
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "Cancel",
            width="stretch",
            key="remove_subject_cancel"
        ):
            st.rerun()

    with col2:

        if st.button(
            "Yes, remove",
            type="primary",
            width="stretch",
            key="remove_subject_confirm"
        ):

            try:

                subject_id = selected["subject_id"]

                supabase.table("attendance_logs").delete().eq(
                    "subject_id", subject_id
                ).execute()

                supabase.table("subject_students").delete().eq(
                    "subject_id", subject_id
                ).execute()

                delete_subject(subject_id)

                st.toast(
                    f"{selected['name']} removed successfully!"
                )

                st.rerun()

            except Exception as error:

                st.error(
                    f"Unable to remove subject: {error}"
                )