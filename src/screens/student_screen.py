import time

import streamlit as st
import numpy as np

from PIL import Image

from src.ui.base_layout import (
    style_background_dashboard,
    style_base_layout
)

from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card
from src.components.dialog_student_voice_attendance import (
    student_voice_attendance_dialog
)

from src.pipelines.face_pipeline import (
    get_face_embeddings,
    get_trained_model,
    clear_face_model_cache,
    FACE_MATCH_THRESHOLD
)

from src.pipelines.voice_pipeline import (
    get_voice_embedding
)

from src.database.db import (
    get_all_students,
    create_student,
    get_student_subjects,
    get_student_attendance,
    unenroll_student_to_subject,
    update_student_voice_embedding
)


# =========================================================
# VOICE PROFILE DIALOG
# =========================================================

@st.dialog("Voice Profile")
def voice_profile_dialog():

    student_data = st.session_state.get(
        "student_data"
    )

    if not student_data:

        st.error(
            "Student information not found."
        )

        return

    st.write(
        "Record your voice to enable "
        "voice-based attendance."
    )

    st.info(
        "For better accuracy, speak clearly "
        "for a few seconds in a quiet environment."
    )

    audio_data = st.audio_input(
        "Record your voice"
    )

    if st.button(
        "Save Voice Profile",
        type="primary",
        width="stretch"
    ):

        if audio_data is None:

            st.warning(
                "Please record your voice first."
            )

            return

        with st.spinner(
            "Creating your voice profile..."
        ):

            voice_embedding = get_voice_embedding(
                audio_data.read()
            )

            if voice_embedding is None:

                st.error(
                    "Could not create voice profile. "
                    "Please try recording again."
                )

                return

            response = update_student_voice_embedding(
                student_data["student_id"],
                voice_embedding
            )

            if not response:

                st.error(
                    "Could not save your voice profile."
                )

                return

        st.session_state["student_data"][
            "voice_embedding"
        ] = voice_embedding

        st.success(
            "Voice profile updated successfully!"
        )

        time.sleep(1)

        st.rerun()


# =========================================================
# STUDENT DASHBOARD
# =========================================================

def student_dashboard():

    student_data = st.session_state.student_data

    student_id = student_data["student_id"]

    c1, c2 = st.columns(
        2,
        vertical_alignment="center",
        gap="xxlarge"
    )

    with c1:

        header_dashboard()

    with c2:

        st.subheader(
            f"Welcome, {student_data['name']}"
        )

        if st.button(
            "Logout",
            type="secondary",
            key="student_logout",
            shortcut="control+backspace"
        ):

            st.session_state["is_logged_in"] = False

            st.session_state["user_role"] = None

            st.session_state.pop(
                "student_data",
                None
            )

            st.rerun()

    st.space()

    c1, c2, c3 = st.columns(3)

    with c1:

        st.header(
            "Your Enrolled Subjects"
        )

    with c2:

        if st.button(
            "➕ Enroll in Subject",
            type="primary",
            width="stretch",
            key="student_enroll_subject"
        ):

            enroll_dialog()

    with c3:

        if st.button(
            "🎙️ Add / Update Voice Profile",
            type="primary",
            width="stretch"
        ):

            voice_profile_dialog()

    st.divider()

    with st.spinner(
        "Loading your enrolled subjects..."
    ):

        subjects = get_student_subjects(
            student_id
        )

        logs = get_student_attendance(
            student_id
        )

    # =====================================================
    # ATTENDANCE STATS
    # =====================================================

    stats_map = {}

    for log in logs:

        subject_id = log["subject_id"]

        if subject_id not in stats_map:

            stats_map[subject_id] = {
                "total": 0,
                "attended": 0
            }

        stats_map[subject_id]["total"] += 1

        if log.get("is_present"):

            stats_map[subject_id]["attended"] += 1

    if not subjects:

        st.info(
            "You are not enrolled in any subjects yet."
        )

    # =====================================================
    # SUBJECT CARDS + VOICE ATTENDANCE
    # =====================================================

    cols = st.columns(2)

    for index, subject_node in enumerate(subjects):

        subject = subject_node["subjects"]

        if not subject:
            continue

        subject_id = subject["subject_id"]

        stats = stats_map.get(
            subject_id,
            {
                "total": 0,
                "attended": 0
            }
        )

        with cols[index % 2]:

            # ---------------------------------------------
            # SUBJECT CARD
            # ---------------------------------------------

            subject_card(
                name=subject["name"],
                code=subject["subject_code"],
                section=subject["section"],
                stats=[
                    (
                        "📅",
                        "Total",
                        stats["total"]
                    ),
                    (
                        "✅",
                        "Attended",
                        stats["attended"]
                    )
                ]
            )

            # ---------------------------------------------
            # UNENROLL BUTTON
            # ---------------------------------------------

            if st.button(
                "Unenroll from this course",
                type="tertiary",
                width="stretch",
                icon=":material/delete_forever:",
                key=f"unenroll_{student_id}_{subject_id}"
            ):

                unenroll_student_to_subject(
                    student_id,
                    subject_id
                )

                st.toast(
                    f"Unenrolled from {subject['name']} successfully!"
                )

                st.rerun()

            # ---------------------------------------------
            # VOICE ATTENDANCE
            # ---------------------------------------------

            voice_button_key = (
                f"student_voice_attendance_"
                f"{student_id}_"
                f"{subject_id}"
            )

            voice_button_clicked = st.button(
                "🎙️ Voice Attendance",
                type="primary",
                width="stretch",
                key=voice_button_key
            )

            if voice_button_clicked:

                student_voice_attendance_dialog(
                    student_id,
                    subject_id,
                    subject["name"]
                )

    footer_dashboard()


# =========================================================
# STUDENT SCREEN
# =========================================================

def student_screen():

    style_background_dashboard()

    style_base_layout()

    if "student_data" in st.session_state:

        student_dashboard()

        return

    c1, c2 = st.columns(
        2,
        vertical_alignment="center",
        gap="xxlarge"
    )

    with c1:

        header_dashboard()

    with c2:

        if st.button(
            "Go back to Home",
            type="secondary",
            key="student_login_back",
            shortcut="control+backspace"
        ):

            st.session_state["login_type"] = None

            st.rerun()

    st.header(
        "Login using FaceID",
        text_alignment="center"
    )

    st.space()
    st.space()

    photo_source = st.camera_input(
        "Position your face in the center"
    )

    show_registration = False

    if photo_source:

        image = np.array(
            Image.open(
                photo_source
            ).convert("RGB")
        )

        with st.spinner(
            "AI is scanning..."
        ):

            encodings = get_face_embeddings(
                image
            )

            num_faces = len(encodings)

            best_student_id = None
            best_distance = None

            if num_faces == 1:

                model_data = get_trained_model()

                if model_data is not None:

                    (
                        best_student_id,
                        best_distance
                    ) = find_best_face_match(
                        encodings[0],
                        model_data["X"],
                        model_data["y"]
                    )

        with st.expander(
            "Face Recognition Diagnostic"
        ):

            st.write(
                "Detected faces:",
                num_faces
            )

            st.write(
                "Best matching student ID:",
                best_student_id
            )

            if best_distance is not None:

                st.write(
                    "Best face distance:",
                    round(
                        best_distance,
                        4
                    )
                )

                st.write(
                    "Current match threshold:",
                    FACE_MATCH_THRESHOLD
                )

            else:

                st.write(
                    "Best face distance:",
                    "N/A"
                )

        if num_faces == 0:

            st.warning(
                "Face not found! "
                "Please position your face clearly "
                "inside the camera frame."
            )

        elif num_faces > 1:

            st.warning(
                "Multiple faces found. "
                "Please make sure only one person "
                "is visible."
            )

        else:

            if (
                best_student_id is not None
                and best_distance is not None
                and best_distance <= FACE_MATCH_THRESHOLD
            ):

                all_students = get_all_students()

                student = next(
                    (
                        student
                        for student in all_students
                        if student["student_id"]
                        == best_student_id
                    ),
                    None
                )

                if student:

                    st.session_state[
                        "is_logged_in"
                    ] = True

                    st.session_state[
                        "user_role"
                    ] = "student"

                    st.session_state[
                        "student_data"
                    ] = student

                    st.toast(
                        f"Welcome back {student['name']}!",
                        icon="👋"
                    )

                    time.sleep(1)

                    st.rerun()

                else:

                    st.warning(
                        "Face matched, but student "
                        "profile was not found."
                    )

            else:

                st.info(
                    "Face not recognized! "
                    "You might be a new student."
                )

                show_registration = True

    if show_registration:

        with st.container(
            border=True
        ):

            st.header(
                "Register New Profile"
            )

            new_name = st.text_input(
                "Enter your name",
                placeholder="E.g. Hamza Rizvi"
            )

            st.subheader(
                "Optional: Voice Enrollment"
            )

            st.info(
                "Enroll your voice for voice-only attendance."
            )

            audio_data = st.audio_input(
                "Record a short phrase like "
                "'I am present, My name is Akash.'"
            )

            if st.button(
                "Create Account",
                type="primary"
            ):

                if not new_name:

                    st.warning(
                        "Please enter your name!"
                    )

                    return

                if photo_source is None:

                    st.error(
                        "Please capture your face first."
                    )

                    return

                with st.spinner(
                    "Creating profile..."
                ):

                    image = np.array(
                        Image.open(
                            photo_source
                        ).convert("RGB")
                    )

                    encodings = get_face_embeddings(
                        image
                    )

                    if not encodings:

                        st.error(
                            "Couldn't capture your facial "
                            "features for registration."
                        )

                        return

                    face_embedding = (
                        encodings[0].tolist()
                    )

                    voice_embedding = None

                    if audio_data:

                        voice_embedding = (
                            get_voice_embedding(
                                audio_data.read()
                            )
                        )

                    response_data = create_student(
                        new_name,
                        face_embedding=face_embedding,
                        voice_embedding=voice_embedding
                    )

                    if response_data:

                        clear_face_model_cache()

                        st.session_state[
                            "is_logged_in"
                        ] = True

                        st.session_state[
                            "user_role"
                        ] = "student"

                        st.session_state[
                            "student_data"
                        ] = response_data[0]

                        st.toast(
                            f"Profile created! Hi {new_name}!",
                            icon="🎉"
                        )

                        time.sleep(1)

                        st.rerun()

                    else:

                        st.error(
                            "Could not create student profile."
                        )

    footer_dashboard()


# =========================================================
# HELPER
# =========================================================

def find_best_face_match(
    face_embedding,
    X,
    y
):

    if X is None or len(X) == 0:

        return None, None

    if y is None or len(y) == 0:

        return None, None

    distances = np.linalg.norm(
        X - face_embedding,
        axis=1
    )

    best_index = int(
        np.argmin(distances)
    )

    best_distance = float(
        distances[best_index]
    )

    best_student_id = int(
        y[best_index]
    )

    return (
        best_student_id,
        best_distance
    )