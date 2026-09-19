import streamlit as st

from src.database.config import supabase
from src.database.db import delete_subject


@st.dialog("Remove Subject")
def remove_subject_dialog(subjects):

    st.subheader(
        "Remove a Subject"
    )

    st.caption(
        "Select the subject you want to permanently remove."
    )

    st.write("")

    options = {
        f"{subject['name']} - {subject['subject_code']}": subject
        for subject in subjects
    }

    selected_label = st.selectbox(
        "Select Subject",
        options=list(options.keys()),
        key="remove_subject_select"
    )

    selected = options[selected_label]

    st.write("")

    with st.container(
        border=True
    ):

        st.subheader(
            selected["name"]
        )

        st.caption(
            f"{selected['subject_code']}  •  Section {selected['section']}"
        )

    st.write("")

    st.warning(
        f"Removing **{selected['name']}** will also delete "
        "its enrolled students and attendance records. "
        "This action cannot be undone."
    )

    st.write("")

    col1, col2 = st.columns(
        2,
        gap="small"
    )

    with col1:

        if st.button(
            "Cancel",
            width="stretch",
            key="remove_subject_cancel",
            type="secondary",
            icon=":material/close:"
        ):

            st.rerun()

    with col2:

        if st.button(
            "Yes, Remove",
            type="primary",
            width="stretch",
            key="remove_subject_confirm",
            icon=":material/delete_forever:"
        ):

            try:

                subject_id = selected["subject_id"]

                supabase.table(
                    "attendance_logs"
                ).delete().eq(
                    "subject_id",
                    subject_id
                ).execute()

                supabase.table(
                    "subject_students"
                ).delete().eq(
                    "subject_id",
                    subject_id
                ).execute()

                delete_subject(
                    subject_id
                )

                st.toast(
                    f"{selected['name']} removed successfully!"
                )

                st.rerun()

            except Exception as error:

                st.error(
                    f"Unable to remove subject: {error}"
                )