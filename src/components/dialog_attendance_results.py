import streamlit as st

from src.database.db import create_attendance


def show_attendance_result(df, logs):

    st.subheader(
        "Review Attendance"
    )

    st.caption(
        "Please review the detected attendance before confirming."
    )

    st.write("")

    with st.container(
        border=True
    ):

        st.subheader(
            "Attendance Summary"
        )

        st.dataframe(
            df,
            hide_index=True,
            width="stretch"
        )

    st.write("")

    st.info(
        "Confirm the attendance to save it to the attendance records, "
        "or discard it to start again."
    )

    st.write("")

    col1, col2 = st.columns(
        2,
        gap="small"
    )

    with col1:

        if st.button(
            "Discard",
            width="stretch",
            key="attendance_discard",
            type="secondary",
            icon=":material/delete:"
        ):

            st.session_state.pop(
                "voice_attendance_pending",
                None
            )

            st.session_state.pop(
                "voice_attendance_results",
                None
            )

            st.session_state.pop(
                "voice_attendance_logs",
                None
            )

            st.session_state[
                "attendance_images"
            ] = []

            st.rerun()

    with col2:

        if st.button(
            "Confirm & Save",
            width="stretch",
            type="primary",
            key="attendance_confirm_save",
            icon=":material/check_circle:"
        ):

            try:

                saved_attendance = create_attendance(
                    logs
                )

                if not saved_attendance:

                    st.warning(
                        "Attendance already marked for today."
                    )

                    return

                st.success(
                    "Attendance taken successfully."
                )

                st.session_state.pop(
                    "voice_attendance_pending",
                    None
                )

                st.session_state.pop(
                    "voice_attendance_results",
                    None
                )

                st.session_state.pop(
                    "voice_attendance_logs",
                    None
                )

                st.session_state[
                    "attendance_images"
                ] = []

                st.rerun()

            except Exception as error:

                st.error(
                    f"Sync failed: {error}"
                )


@st.dialog("Attendance Reports")
def attendance_result_dialog(
    df,
    logs
):

    show_attendance_result(
        df,
        logs
    )