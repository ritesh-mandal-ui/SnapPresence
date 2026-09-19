import streamlit as st
import pandas as pd

from src.pipelines.voice_pipeline import (
    process_bulk_audio,
    VOICE_MATCH_THRESHOLD
)

from src.database.config import supabase


@st.dialog("Voice Attendance")
def voice_attendance_dialog(selected_subject_id):

    st.subheader(
        "Mark Attendance Using Voice"
    )

    st.caption(
        "Record classroom audio and let AI identify registered "
        "student voices automatically."
    )

    st.write("")

    with st.container(
        border=True
    ):

        st.subheader(
            "🎙️ Record Classroom Audio"
        )

        st.caption(
            "Students should speak one at a time and clearly "
            "while the teacher records the classroom audio."
        )

        voice_recording_key = (
            f"teacher_voice_recording_"
            f"{selected_subject_id}_"
            f"{st.session_state.get('voice_recording_version', 0)}"
        )

        audio_data = st.audio_input(
            "Record classroom audio",
            key=voice_recording_key
        )

    st.write("")

    if st.button(
        "Analyze Audio",
        width="stretch",
        type="primary",
        icon=":material/graphic_eq:"
    ):

        if audio_data is None:

            st.warning(
                "Please record classroom audio first."
            )

            return

        with st.spinner(
            "AI is analyzing classroom voices..."
        ):

            enrolled_res = (
                supabase
                .table("subject_students")
                .select("*, students(*)")
                .eq(
                    "subject_id",
                    selected_subject_id
                )
                .execute()
            )

            enrolled_students = (
                enrolled_res.data
                or []
            )

            if not enrolled_students:

                st.warning(
                    "Students need to enroll first."
                )

                return

            candidates_dict = {}

            for node in enrolled_students:

                student = node.get(
                    "students"
                )

                if not student:
                    continue

                student_id = student.get(
                    "student_id"
                )

                voice_embedding = student.get(
                    "voice_embedding"
                )

                if (
                    student_id is not None
                    and voice_embedding
                ):

                    candidates_dict[
                        int(student_id)
                    ] = voice_embedding

            if not candidates_dict:

                st.error(
                    "No enrolled students have "
                    "voice profiles registered."
                )

                return

            audio_bytes = audio_data.read()

            if not audio_bytes:

                st.warning(
                    "Recorded audio could not be read."
                )

                return

            detected_scores = process_bulk_audio(
                audio_bytes,
                candidates_dict,
                threshold=VOICE_MATCH_THRESHOLD
            )

            results = []
            attendance_to_log = []

            for node in enrolled_students:

                student = node.get(
                    "students"
                )

                if not student:
                    continue

                student_id = int(
                    student["student_id"]
                )

                score = detected_scores.get(
                    student_id,
                    0.0
                )

                is_present = (
                    score >= VOICE_MATCH_THRESHOLD
                )

                results.append({
                    "Name": student["name"],
                    "ID": student_id,
                    "Confidence": (
                        f"{score:.3f}"
                        if score > 0
                        else "-"
                    ),
                    "Status": (
                        "✅ Present"
                        if is_present
                        else "❌ Absent"
                    )
                })

                attendance_to_log.append({
                    "student_id": student_id,
                    "subject_id": int(
                        selected_subject_id
                    ),
                    "is_present": is_present
                })

            if not results:

                st.warning(
                    "No valid enrolled students were found."
                )

                return

            st.session_state[
                "voice_attendance_pending"
            ] = {
                "df": pd.DataFrame(results),
                "logs": attendance_to_log
            }

            st.session_state[
                "voice_recording_version"
            ] = st.session_state.get(
                "voice_recording_version",
                0
            ) + 1

            st.rerun(
                scope="app"
            )