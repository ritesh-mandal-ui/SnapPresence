import streamlit as st
import numpy as np
import pandas as pd

import base64
import hashlib
import secrets

from datetime import datetime

from src.ui.base_layout import (
    style_background_dashboard,
    style_base_layout
)

from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.subject_card import subject_card
from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photo import add_photos_dialog
from src.components.dialog_attendance_results import attendance_result_dialog
from src.components.dialog_voice_attendance import voice_attendance_dialog

from src.pipelines.face_pipeline import predict_attendance

from src.database.config import supabase

from src.database.db import (
    check_teacher_exists,
    create_teacher,
    teacher_login,
    get_teacher_subjects,
    get_attendance_for_teacher,
    unenroll_student_to_subject,
    get_teacher_by_email,
    update_teacher_password
)


# =========================================================
# TEACHER PASSWORD RECOVERY
# =========================================================

def generate_recovery_pkce():

    code_verifier = secrets.token_urlsafe(64)

    digest = hashlib.sha256(
        code_verifier.encode("ascii")
    ).digest()

    code_challenge = (
        base64.urlsafe_b64encode(digest)
        .decode("ascii")
        .rstrip("=")
    )

    return (
        code_verifier,
        code_challenge
    )


def send_teacher_password_reset(email):

    if not email:
        return (
            False,
            "Please enter your email."
        )

    teacher = get_teacher_by_email(
        email
    )

    if not teacher:
        return (
            False,
            "No teacher account found with this email."
        )

    try:

        (
            code_verifier,
            code_challenge
        ) = generate_recovery_pkce()

        # Keep verifier in Streamlit session
        st.session_state[
            "teacher_recovery_code_verifier"
        ] = code_verifier

        # Also keep verifier in Supabase auth storage
        supabase.auth._storage.set_item(
            f"{supabase.auth._storage_key}-code-verifier",
            code_verifier
        )

        # Start PKCE password recovery
        supabase.auth._request(
            "POST",
            "recover",
            body={
                "email": email,
                "code_challenge": code_challenge,
                "code_challenge_method": "s256"
            },
            redirect_to="http://localhost:8501"
        )

        return (
            True,
            "Password reset link has been sent to your email."
        )

    except Exception as e:

        return (
            False,
            f"Unable to send password reset email: {e}"
        )


def check_teacher_recovery_session():

    try:

        # -------------------------------------------------
        # IMPORTANT:
        # Only process recovery when ?code= exists.
        #
        # Normal teacher login also creates a Supabase
        # session, so checking get_session() alone would
        # incorrectly open the password reset screen.
        # -------------------------------------------------

        code = st.query_params.get(
            "code"
        )

        if not code:
            return False

        # -------------------------------------------------
        # Get PKCE verifier from Streamlit session first
        # -------------------------------------------------

        code_verifier = st.session_state.get(
            "teacher_recovery_code_verifier"
        )

        # -------------------------------------------------
        # Fallback to Supabase storage
        # -------------------------------------------------

        if not code_verifier:

            code_verifier = (
                supabase
                .auth
                ._storage
                .get_item(
                    f"{supabase.auth._storage_key}-code-verifier"
                )
            )

        if not code_verifier:

            print(
                "Teacher recovery error: "
                "PKCE code verifier not found."
            )

            return False

        # -------------------------------------------------
        # Exchange recovery code for authenticated session
        # -------------------------------------------------

        response = (
            supabase.auth.exchange_code_for_session(
                {
                    "auth_code": code,
                    "code_verifier": code_verifier
                }
            )
        )

        # -------------------------------------------------
        # Make sure exchange was successful
        # -------------------------------------------------

        if not response or not response.session:

            return False

        # -------------------------------------------------
        # Clear callback URL only after successful exchange
        # -------------------------------------------------

        st.query_params.clear()

        st.session_state.pop(
            "teacher_recovery_code_verifier",
            None
        )

        # -------------------------------------------------
        # Get authenticated session
        # -------------------------------------------------

        session = supabase.auth.get_session()

        if not session:

            return False

        user = getattr(
            session,
            "user",
            None
        )

        if not user:

            return False

        user_id = getattr(
            user,
            "id",
            None
        )

        if not user_id:

            return False

        # -------------------------------------------------
        # Find matching teacher
        # -------------------------------------------------

        teacher = (
            supabase
            .table("teachers")
            .select("*")
            .eq(
                "auth_user_id",
                user_id
            )
            .execute()
        )

        if not teacher.data:

            return False

        st.session_state[
            "teacher_recovery"
        ] = teacher.data[0]

        return True

    except Exception as e:

        print(
            f"Teacher recovery error: {e}"
        )

        return False


# =========================================================
# TEACHER SCREEN ROUTER
# =========================================================

def teacher_screen():

    style_background_dashboard()
    style_base_layout()

    if "teacher_data" in st.session_state:

        teacher_dashboard()

        return

    if (
        "teacher_recovery"
        not in st.session_state
    ):

        check_teacher_recovery_session()

    if (
        "teacher_recovery"
        in st.session_state
    ):

        teacher_screen_update_password()

    elif (
        "teacher_login_type"
        not in st.session_state

        or st.session_state.teacher_login_type
        == "login"
    ):

        teacher_screen_login()

    elif (
        st.session_state.teacher_login_type
        == "register"
    ):

        teacher_screen_register()

    elif (
        st.session_state.teacher_login_type
        == "forgot_password"
    ):

        teacher_screen_forgot_password()


# =========================================================
# TEACHER DASHBOARD
# =========================================================

def teacher_dashboard():

    teacher_data = st.session_state.teacher_data

    c1, c2 = st.columns(
        2,
        vertical_alignment="center",
        gap="xxlarge"
    )

    with c1:

        header_dashboard()

    with c2:

        st.subheader(
            f"Welcome, {teacher_data['name']}"
        )

        if st.button(
            "Logout",
            type="secondary",
            key="teacher_logout",
            shortcut="control+backspace"
        ):

            st.session_state["is_logged_in"] = False

            st.session_state["user_role"] = None

            st.session_state.pop(
                "teacher_data",
                None
            )

            st.rerun()

    st.space()

    if "current_teacher_tab" not in st.session_state:

        st.session_state.current_teacher_tab = (
            "take_attendance"
        )

    tab1, tab2, tab3, tab4 = st.columns(4)

    with tab1:

        button_type = (
            "primary"
            if (
                st.session_state.current_teacher_tab
                == "take_attendance"
            )
            else "tertiary"
        )

        if st.button(
            "Take Attendance",
            type=button_type,
            width="stretch",
            icon=":material/ar_on_you:"
        ):

            st.session_state.current_teacher_tab = (
                "take_attendance"
            )

            st.rerun()

    with tab2:

        button_type = (
            "primary"
            if (
                st.session_state.current_teacher_tab
                == "manage_subjects"
            )
            else "tertiary"
        )

        if st.button(
            "Manage Subjects",
            type=button_type,
            width="stretch",
            icon=":material/book_ribbon:"
        ):

            st.session_state.current_teacher_tab = (
                "manage_subjects"
            )

            st.rerun()

    with tab3:

        button_type = (
            "primary"
            if (
                st.session_state.current_teacher_tab
                == "manage_students"
            )
            else "tertiary"
        )

        if st.button(
            "Manage Students",
            type=button_type,
            width="stretch",
            icon=":material/group:"
        ):

            st.session_state.current_teacher_tab = (
                "manage_students"
            )

            st.rerun()

    with tab4:

        button_type = (
            "primary"
            if (
                st.session_state.current_teacher_tab
                == "attendance_records"
            )
            else "tertiary"
        )

        if st.button(
            "Attendance Records",
            type=button_type,
            width="stretch",
            icon=":material/cards_stack:"
        ):

            st.session_state.current_teacher_tab = (
                "attendance_records"
            )

            st.rerun()

    st.divider()

    if (
        st.session_state.current_teacher_tab
        == "take_attendance"
    ):

        teacher_tab_take_attendance()

    elif (
        st.session_state.current_teacher_tab
        == "manage_subjects"
    ):

        teacher_tab_manage_subjects()

    elif (
        st.session_state.current_teacher_tab
        == "manage_students"
    ):

        teacher_tab_manage_students()

    elif (
        st.session_state.current_teacher_tab
        == "attendance_records"
    ):

        teacher_tab_attendance_records()

    footer_dashboard()


# =========================================================
# TAKE ATTENDANCE
# =========================================================

def teacher_tab_take_attendance():

    teacher_id = st.session_state.teacher_data[
        "teacher_id"
    ]

    st.header(
        "Take AI Attendance"
    )

    if "attendance_images" not in st.session_state:

        st.session_state.attendance_images = []

    subjects = get_teacher_subjects(
        teacher_id
    )

    if not subjects:

        st.warning(
            "You haven't created any subjects yet! "
            "Please create one to begin!"
        )

        return

    subject_options = {
        f"{subject['name']} - {subject['subject_code']}":
        subject["subject_id"]
        for subject in subjects
    }

    col1, col2 = st.columns(
        [3, 1],
        vertical_alignment="bottom"
    )

    with col1:

        selected_subject_label = st.selectbox(
            "Select Subject",
            options=list(
                subject_options.keys()
            )
        )

    with col2:

        if st.button(
            "Add Photos",
            type="primary",
            icon=":material/photo_prints:",
            width="stretch"
        ):

            add_photos_dialog()

    selected_subject_id = (
        subject_options[
            selected_subject_label
        ]
    )

    st.divider()

    if st.session_state.attendance_images:

        st.header(
            "Added Photos"
        )

        gallery_cols = st.columns(4)

        for idx, image in enumerate(
            st.session_state.attendance_images
        ):

            with gallery_cols[
                idx % 4
            ]:

                st.image(
                    image,
                    width="stretch",
                    caption=f"Photo {idx + 1}"
                )

    has_photos = bool(
        st.session_state.attendance_images
    )

    c1, c2 = st.columns(2)

    with c1:

        if st.button(
            "Clear all photos",
            width="stretch",
            type="tertiary",
            icon=":material/delete:",
            disabled=not has_photos
        ):

            st.session_state.attendance_images = []

            st.rerun()

    with c2:

        if st.button(
            "Run Face Analysis",
            width="stretch",
            type="secondary",
            icon=":material/analytics:",
            disabled=not has_photos
        ):

            with st.spinner(
                "Deep scanning classroom photos..."
            ):

                enrolled_res = (
                    supabase
                    .table("subject_students")
                    .select(
                        "*, students(*)"
                    )
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

                enrolled_ids = set()

                valid_enrolled_students = []

                for node in enrolled_students:

                    student = node.get(
                        "students"
                    )

                    if not student:
                        continue

                    student_id = student.get(
                        "student_id"
                    )

                    if student_id is None:
                        continue

                    student_id = int(
                        student_id
                    )

                    enrolled_ids.add(
                        student_id
                    )

                    valid_enrolled_students.append(
                        node
                    )

                if not enrolled_ids:

                    st.warning(
                        "Students need to enroll first."
                    )

                    return

                all_detected_ids = {}

                total_faces_detected = 0

                for idx, image in enumerate(
                    st.session_state.attendance_images
                ):

                    image_np = np.array(
                        image.convert("RGB")
                    )

                    detected, _, face_count = (
                        predict_attendance(
                            image_np,
                            allowed_student_ids=enrolled_ids
                        )
                    )

                    total_faces_detected += (
                        face_count
                    )

                    for student_id in detected.keys():

                        student_id = int(
                            student_id
                        )

                        all_detected_ids.setdefault(
                            student_id,
                            []
                        ).append(
                            f"Photo {idx + 1}"
                        )

                if not all_detected_ids:

                    if total_faces_detected > 0:

                        st.warning(
                            "No enrolled student was recognized. "
                            "Unknown or non-enrolled faces are ignored. "
                            "Attendance was not generated."
                        )

                    else:

                        st.info(
                            "No face was detected in the "
                            "uploaded photos."
                        )

                    return

                results = []

                attendance_to_log = []

                current_timestamp = (
                    datetime.now().strftime(
                        "%Y-%m-%dT%H:%M:%S"
                    )
                )

                for node in valid_enrolled_students:

                    student = node["students"]

                    student_id = int(
                        student["student_id"]
                    )

                    sources = all_detected_ids.get(
                        student_id,
                        []
                    )

                    is_present = bool(
                        sources
                    )

                    results.append({
                        "Name": student["name"],
                        "ID": student_id,
                        "Source": (
                            ", ".join(
                                sources
                            )
                            if is_present
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

                if results:

                    attendance_result_dialog(
                        pd.DataFrame(
                            results
                        ),
                        attendance_to_log
                    )

    st.divider()

    st.header(
        "Voice Attendance"
    )

    st.write(
        "Record live classroom audio and let AI "
        "recognize enrolled student voices."
    )

    if st.button(
        "🎙️ Start Voice Attendance",
        type="primary",
        width="stretch"
    ):

        voice_attendance_dialog(
            selected_subject_id
        )


# =========================================================
# MANAGE SUBJECTS
# =========================================================

def teacher_tab_manage_subjects():

    teacher_id = st.session_state.teacher_data[
        "teacher_id"
    ]

    col1, col2 = st.columns(2)

    with col1:

        st.header(
            "Manage Subjects"
        )

    with col2:

        if st.button(
            "Create New Subject",
            width="stretch"
        ):

            create_subject_dialog(
                teacher_id
            )

    subjects = get_teacher_subjects(
        teacher_id
    )

    if not subjects:

        st.info(
            "No subjects found. Create one above."
        )

        return

    for sub in subjects:

        stats = [
            (
                "🫂",
                "Students",
                sub.get(
                    "total_students",
                    0
                )
            ),
            (
                "🕰️",
                "Classes",
                sub.get(
                    "total_classes",
                    0
                )
            )
        ]

        def share_btn(
            subject_name=sub["name"],
            subject_code=sub["subject_code"]
        ):

            if st.button(
                f"Share Code: {subject_name}",
                key=f"share_{subject_code}",
                icon=":material/share:"
            ):

                share_subject_dialog(
                    subject_name,
                    subject_code
                )

        subject_card(
            name=sub["name"],
            code=sub["subject_code"],
            section=sub["section"],
            stats=stats,
            footer_callback=share_btn
        )


# =========================================================
# MANAGE STUDENTS
# =========================================================

def teacher_tab_manage_students():

    teacher_id = st.session_state.teacher_data[
        "teacher_id"
    ]

    st.header(
        "Manage Students"
    )

    st.write(
        "View and manage students enrolled in your subjects."
    )

    subjects = get_teacher_subjects(
        teacher_id
    )

    if not subjects:

        st.info(
            "No subjects found. Create a subject first."
        )

        return

    subject_options = {
        f"{subject['name']} - "
        f"{subject['subject_code']}":
        subject["subject_id"]
        for subject in subjects
    }

    selected_subject_label = st.selectbox(
        "Select Subject",
        options=list(
            subject_options.keys()
        ),
        key="manage_students_subject"
    )

    selected_subject_id = (
        subject_options[
            selected_subject_label
        ]
    )

    st.divider()

    enrolled_res = (
        supabase
        .table("subject_students")
        .select(
            "student_id, subject_id, students(*)"
        )
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

        st.info(
            "No students are enrolled in this subject."
        )

        return

    st.subheader(
        f"Enrolled Students ({len(enrolled_students)})"
    )

    for node in enrolled_students:

        student = node.get(
            "students"
        )

        if not student:
            continue

        student_id = student.get(
            "student_id"
        )

        student_name = student.get(
            "name",
            "Unknown Student"
        )

        col1, col2 = st.columns(
            [4, 1],
            vertical_alignment="center"
        )

        with col1:

            st.markdown(
                f"""
                <div style="
                    padding:10px 0;
                ">
                    <strong>{student_name}</strong><br>
                    <span style="
                        color:#666666;
                        font-size:14px;
                    ">
                        Student ID: {student_id}
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:

            if st.button(
                "Remove",
                key=(
                    f"remove_student_"
                    f"{selected_subject_id}_"
                    f"{student_id}"
                ),
                type="secondary",
                icon=":material/person_remove:"
            ):

                try:

                    unenroll_student_to_subject(
                        student_id,
                        selected_subject_id
                    )

                    st.success(
                        f"{student_name} removed from "
                        f"{selected_subject_label}."
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"Unable to remove {student_name}: {e}"
                    )


# =========================================================
# ATTENDANCE RECORDS
# =========================================================

def teacher_tab_attendance_records():

    st.header(
        "Attendance Records"
    )

    teacher_id = st.session_state.teacher_data[
        "teacher_id"
    ]

    records = get_attendance_for_teacher(
        teacher_id
    )

    if not records:

        st.info(
            "No attendance records found."
        )

        return

    data = []

    for record in records:

        timestamp = record.get(
            "timestamp"
        )

        if not timestamp:
            continue

        try:

            parsed_time = datetime.fromisoformat(
                timestamp.replace(
                    "Z",
                    "+00:00"
                )
            )

            display_time = parsed_time.strftime(
                "%Y-%m-%d %I:%M %p"
            )

        except ValueError:

            display_time = timestamp

        subject = record.get(
            "subjects",
            {}
        )

        data.append({
            "ts_group": timestamp.split(".")[0],
            "Time": display_time,
            "Subject": subject.get(
                "name",
                "Unknown"
            ),
            "Subject Code": subject.get(
                "subject_code",
                "N/A"
            ),
            "is_present": bool(
                record.get(
                    "is_present",
                    False
                )
            )
        })

    if not data:

        st.info(
            "No valid attendance records found."
        )

        return

    df = pd.DataFrame(
        data
    )

    summary = (
        df.groupby(
            [
                "ts_group",
                "Time",
                "Subject",
                "Subject Code"
            ]
        )
        .agg(
            Present_Count=(
                "is_present",
                "sum"
            ),
            Total_Count=(
                "is_present",
                "count"
            )
        )
        .reset_index()
    )

    summary["Attendance Stats"] = (
        "✅ "
        + summary[
            "Present_Count"
        ].astype(str)
        + " / "
        + summary[
            "Total_Count"
        ].astype(str)
        + " Students"
    )

    display_df = (
        summary
        .sort_values(
            by="ts_group",
            ascending=False
        )
        [
            [
                "Time",
                "Subject",
                "Subject Code",
                "Attendance Stats"
            ]
        ]
    )

    st.dataframe(
        display_df,
        width="stretch",
        hide_index=True
    )


# =========================================================
# TEACHER LOGIN
# =========================================================

def login_teacher(
    username,
    password
):

    if not username or not password:

        return False

    teacher = teacher_login(
        username,
        password
    )

    if teacher:

        st.session_state[
            "user_role"
        ] = "teacher"

        st.session_state[
            "teacher_data"
        ] = teacher

        st.session_state[
            "is_logged_in"
        ] = True

        return True

    return False


# =========================================================
# TEACHER LOGIN SCREEN
# =========================================================

def teacher_screen_login():

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
            key="teacher_login_back",
            shortcut="control+backspace"
        ):

            st.session_state[
                "login_type"
            ] = None

            st.rerun()

    st.header(
        "Login using password",
        text_alignment="center"
    )

    st.space()
    st.space()

    teacher_username = st.text_input(
        "Enter username",
        placeholder="ananyaroy"
    )

    teacher_password = st.text_input(
        "Enter password",
        type="password",
        placeholder="Enter password"
    )

    if st.button(
        "Forgot Password?",
        type="tertiary",
        width="stretch"
    ):

        st.session_state[
            "teacher_login_type"
        ] = "forgot_password"

        st.rerun()

    st.divider()

    btnc1, btnc2 = st.columns(2)

    with btnc1:

        if st.button(
            "Login",
            icon=":material/passkey:",
            shortcut="control+enter",
            width="stretch"
        ):

            if login_teacher(
                teacher_username,
                teacher_password
            ):

                st.toast(
                    "Welcome back!",
                    icon="👋"
                )

                import time

                time.sleep(1)

                st.rerun()

            else:

                st.error(
                    "Invalid username and password combo"
                )

    with btnc2:

        if st.button(
            "Register Instead",
            type="primary",
            icon=":material/passkey:",
            width="stretch"
        ):

            st.session_state.teacher_login_type = (
                "register"
            )

            st.rerun()

    footer_dashboard()


# =========================================================
# FORGOT PASSWORD SCREEN
# =========================================================

def teacher_screen_forgot_password():

    c1, c2 = st.columns(
        2,
        vertical_alignment="center",
        gap="xxlarge"
    )

    with c1:

        header_dashboard()

    with c2:

        if st.button(
            "Back to Login",
            type="secondary",
            key="teacher_forgot_back"
        ):

            st.session_state.teacher_login_type = (
                "login"
            )

            st.rerun()

    st.header(
        "Reset your password",
        text_alignment="center"
    )

    st.write(
        "Enter the email address linked to your teacher account."
    )

    teacher_email = st.text_input(
        "Enter email",
        placeholder="ananya@example.com"
    )

    if st.button(
        "Send Reset Link",
        type="primary",
        width="stretch"
    ):

        success, message = (
            send_teacher_password_reset(
                teacher_email
            )
        )

        if success:

            st.success(
                message
            )

        else:

            st.error(
                message
            )

    footer_dashboard()


# =========================================================
# UPDATE PASSWORD SCREEN
# =========================================================

def teacher_screen_update_password():

    teacher = st.session_state.get(
        "teacher_recovery"
    )

    if not teacher:

        st.session_state.pop(
            "teacher_recovery",
            None
        )

        st.session_state.teacher_login_type = (
            "login"
        )

        st.rerun()

    c1, c2 = st.columns(
        2,
        vertical_alignment="center",
        gap="xxlarge"
    )

    with c1:

        header_dashboard()

    st.header(
        "Create a new password",
        text_alignment="center"
    )

    st.write(
        f"Reset password for {teacher['name']}"
    )

    new_password = st.text_input(
        "New password",
        type="password",
        placeholder="Enter new password"
    )

    confirm_password = st.text_input(
        "Confirm new password",
        type="password",
        placeholder="Enter new password again"
    )

    if st.button(
        "Update Password",
        type="primary",
        width="stretch"
    ):

        if not new_password or not confirm_password:

            st.error(
                "Both password fields are required."
            )

            return

        if new_password != confirm_password:

            st.error(
                "Passwords don't match."
            )

            return

        if len(new_password) < 6:

            st.error(
                "Password must be at least 6 characters."
            )

            return

        try:

            supabase.auth.update_user({
                "password": new_password
            })

            update_teacher_password(
                teacher["teacher_id"],
                new_password
            )

            st.session_state.pop(
                "teacher_recovery",
                None
            )

            st.session_state.pop(
                "teacher_recovery_code_verifier",
                None
            )

            st.session_state.teacher_login_type = (
                "login"
            )

            st.success(
                "Password updated successfully. "
                "You can now login with your new password."
            )

            import time

            time.sleep(1)

            st.rerun()

        except Exception as e:

            st.error(
                f"Unable to update password: {e}"
            )

    footer_dashboard()


# =========================================================
# REGISTER TEACHER
# =========================================================

def register_teacher(
    teacher_username,
    teacher_name,
    teacher_email,
    teacher_password,
    teacher_password_confirm
):

    if (
        not teacher_username
        or not teacher_name
        or not teacher_email
        or not teacher_password
    ):

        return (
            False,
            "All fields are required!"
        )

    if check_teacher_exists(
        teacher_username
    ):

        return (
            False,
            "Username already taken"
        )

    if teacher_password != teacher_password_confirm:

        return (
            False,
            "Passwords don't match"
        )

    try:

        create_teacher(
            teacher_username,
            teacher_password,
            teacher_name,
            teacher_email
        )

        return (
            True,
            "Successfully created! Login now."
        )

    except Exception:

        return (
            False,
            "Unexpected error while creating account."
        )


def teacher_screen_register():

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
            key="teacher_register_back",
            shortcut="control+backspace"
        ):

            st.session_state[
                "login_type"
            ] = None

            st.rerun()

    st.header(
        "Register your teacher profile"
    )

    st.space()
    st.space()

    teacher_username = st.text_input(
        "Enter username",
        placeholder="ananyaroy"
    )

    teacher_name = st.text_input(
        "Enter name",
        placeholder="Ananya Roy"
    )

    teacher_email = st.text_input(
        "Enter email",
        placeholder="ananya@example.com"
    )

    teacher_password = st.text_input(
        "Enter password",
        type="password",
        placeholder="Enter password"
    )

    teacher_password_confirm = st.text_input(
        "Confirm your password",
        type="password",
        placeholder="Enter password"
    )

    st.divider()

    btnc1, btnc2 = st.columns(2)

    with btnc1:

        if st.button(
            "Register now",
            icon=":material/passkey:",
            shortcut="control+enter",
            width="stretch"
        ):

            success, message = register_teacher(
                teacher_username,
                teacher_name,
                teacher_email,
                teacher_password,
                teacher_password_confirm
            )

            if success:

                st.success(
                    message
                )

                import time

                time.sleep(1)

                st.session_state.teacher_login_type = (
                    "login"
                )

                st.rerun()

            else:

                st.error(
                    message
                )

    with btnc2:

        if st.button(
            "Login Instead",
            type="primary",
            icon=":material/passkey:",
            width="stretch"
        ):

            st.session_state.teacher_login_type = (
                "login"
            )

            st.rerun()

    footer_dashboard()