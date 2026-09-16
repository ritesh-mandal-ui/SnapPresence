
import streamlit as st
import pandas as pd

from datetime import datetime

from src.pipelines.voice_pipeline import (
    process_bulk_audio,
    VOICE_MATCH_THRESHOLD
)

from src.database.config import supabase

from src.components.dialog_attendance_results import (
    show_attendance_result
)


@st.dialog("Voice Attendance")
def voice_attendance_dialog(selected_subject_id):

    st.write(
        "Record classroom audio while students say "
        "'I am present'. AI will recognize registered voices."
    )

    st.info(
        "Students should speak one at a time and clearly "
        "while the teacher records the classroom audio."
    )

    audio_data = st.audio_input(
        "Record classroom audio"
    )

    if st.button(
        "Analyze Audio",
        width="stretch",
        type="primary"
    ):

        if audio_data is None:
            st.warning("Please record classroom audio first.")
            return

        with st.spinner("AI is analyzing classroom voices..."):

            enrolled_res = (
                supabase
                .table("subject_students")
                .select("*, students(*)")
                .eq("subject_id", selected_subject_id)
                .execute()
            )

            enrolled_students = enrolled_res.data or []

            if not enrolled_students:
                st.warning("Students need to enroll first.")
                return

            candidates_dict = {}

            for node in enrolled_students:

                student = node.get("students")

                if not student:
                    continue

                student_id = student.get("student_id")
                voice_embedding = student.get("voice_embedding")

                if student_id is not None and voice_embedding:
                    candidates_dict[int(student_id)] = voice_embedding

            if not candidates_dict:
                st.error(
                    "No enrolled students have voice profiles registered."
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

            current_timestamp = datetime.now().strftime(
                "%Y-%m-%dT%H:%M:%S"
            )

            for node in enrolled_students:

                student = node.get("students")

                if not student:
                    continue

                student_id = int(student["student_id"])

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
                    "subject_id": selected_subject_id,
                    "timestamp": current_timestamp,
                    "is_present": is_present
                })

            if not results:
                st.warning(
                    "No valid enrolled students were found."
                )
                return

            # IMPORTANT:
            # Do NOT call attendance_result_dialog() here.
            # voice_attendance_dialog() is already a dialog,
            # so opening another dialog would create a nested dialog.
            show_attendance_result(
                pd.DataFrame(results),
                attendance_to_log
            )

