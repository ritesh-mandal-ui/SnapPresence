import streamlit as st

from src.pipelines.voice_pipeline import (
    get_voice_embedding,
    cosine_similarity,
    VOICE_MATCH_THRESHOLD
)

from src.database.db import (
    create_attendance,
    get_all_students
)


@st.dialog("Voice Attendance")
def student_voice_attendance_dialog(
    student_id,
    subject_id,
    subject_name
):

    st.write(
        f"Record your voice to mark attendance "
        f"for **{subject_name}**."
    )

    st.info(
        "Please speak clearly for a few seconds "
        "in a quiet environment."
    )

    voice_dialog_key = st.session_state.get(
        "voice_dialog_key",
        0
    )

    audio_data = st.audio_input(
        "Record your voice",
        key=(
            f"student_voice_input_"
            f"{student_id}_"
            f"{subject_id}_"
            f"{voice_dialog_key}"
        )
    )

    if st.button(
        "Verify & Mark Attendance",
        type="primary",
        width="stretch"
    ):

        if audio_data is None:

            st.warning(
                "Please record your voice first."
            )

            return

        with st.spinner(
            "AI is verifying your voice..."
        ):

            audio_bytes = audio_data.read()

            detected_embedding = get_voice_embedding(
                audio_bytes
            )

            if detected_embedding is None:

                st.error(
                    "Could not process your voice. "
                    "Please try recording again."
                )

                return

            students = get_all_students()

            student = next(
                (
                    item
                    for item in students
                    if int(item["student_id"])
                    == int(student_id)
                ),
                None
            )

            if not student:

                st.error(
                    "Student profile could not be found."
                )

                return

            saved_embedding = student.get(
                "voice_embedding"
            )

            if not saved_embedding:

                st.warning(
                    "Voice profile not found. "
                    "Please add or update your Voice Profile first."
                )

                return

            score = cosine_similarity(
                detected_embedding,
                saved_embedding
            )

            if score < VOICE_MATCH_THRESHOLD:

                st.error(
                    "Voice verification failed. "
                    "Your voice could not be matched."
                )

                st.write(
                    f"Voice similarity: {score:.3f}"
                )

                return

            attendance_log = {
                "student_id": int(student_id),
                "subject_id": int(subject_id),
                "is_present": True
            }

            saved_attendance = create_attendance(
                [attendance_log]
            )

            if not saved_attendance:

                st.warning(
                    "⚠️ Attendance already marked for today."
                )

                st.session_state["voice_dialog_key"] = (
                    voice_dialog_key + 1
                )

                st.rerun(scope="app")

                return

            st.success(
                "✅ Voice verified! "
                "Attendance marked successfully."
            )

            st.write(
                f"Voice similarity: {score:.3f}"
            )

            st.session_state["voice_dialog_key"] = (
                voice_dialog_key + 1
            )

            st.rerun(scope="app")