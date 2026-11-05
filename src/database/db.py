
import time
import bcrypt

from datetime import datetime, timedelta, timezone

from src.database.config import supabase, supabase_admin


def hash_pass(password):
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()


def check_pass(password, hashed):
    return bcrypt.checkpw(
        password.encode(),
        hashed.encode()
    )

def check_teacher_exists(username):
    response = (
        supabase_admin
        .table("teachers")
        .select("teacher_id")
        .eq("username", username)
        .execute()
    )

    return len(response.data or []) > 0

def create_teacher(username, password, name, email):
    data = {
        "username": username,
        "password": hash_pass(password),
        "name": name,
        "email": email
    }

    response = (
        supabase_admin
        .table("teachers")
        .insert(data)
        .execute()
    )

    return response.data



def teacher_login(username, password):
    response = (
        supabase_admin
        .table("teachers")
        .select("*")
        .eq("username", username)
        .execute()
    )

    if not response.data:
        return None

    teacher = response.data[0]

    try:
        if check_pass(password, teacher["password"]):
            return teacher
    except (ValueError, TypeError, KeyError):
        return None

    return None


def get_all_students():
    """Fetch student records for trusted server-side operations."""
    response = (
        supabase_admin
        .table("students")
        .select("*")
        .execute()
    )

    return response.data or []


def get_all_students_for_face_login():
    """Load student face profiles for server-side face matching."""
    response = (
        supabase_admin
        .table("students")
        .select(
            "student_id, name, face_embedding, voice_embedding"
        )
        .execute()
    )

    return response.data or []


def create_student(
    new_name,
    face_embedding=None,
    voice_embedding=None
):
    if not isinstance(new_name, str) or not new_name.strip():
        raise ValueError("Student name is required.")

    if face_embedding is None:
        raise ValueError("Face embedding is required.")

    data = {
        "name": new_name.strip(),
        "face_embedding": face_embedding,
        "voice_embedding": voice_embedding
    }

    response = (
        supabase_admin
        .table("students")
        .insert(data)
        .execute()
    )

    return response.data


def update_student_voice_embedding(student_id, voice_embedding):
    response = (
        supabase_admin
        .table("students")
        .update({
            "voice_embedding": voice_embedding
        })
        .eq("student_id", student_id)
        .execute()
    )

    return response.data


def create_subject(subject_code, name, section, teacher_id):
    data = {
        "subject_code": subject_code,
        "name": name,
        "section": section,
        "teacher_id": teacher_id
    }

    response = (
        supabase_admin
        .table("subjects")
        .insert(data)
        .execute()
    )

    return response.data


def delete_subject(subject_id):
    response = (
        supabase_admin
        .table("subjects")
        .delete()
        .eq("subject_id", subject_id)
        .execute()
    )

    return response.data


def get_teacher_subjects(teacher_id):
    last_error = None

    for attempt in range(3):
        try:
            response = (
                supabase_admin
                .table("subjects")
                .select(
                    "*, subject_students(count), "
                    "attendance_logs(timestamp)"
                )
                .eq("teacher_id", teacher_id)
                .execute()
            )

            subjects = response.data or []

            for subject in subjects:
                student_counts = subject.get("subject_students") or []

                subject["total_students"] = (
                    student_counts[0].get("count", 0)
                    if student_counts
                    else 0
                )

                attendance = subject.get("attendance_logs") or []

                subject["total_classes"] = len({
                    log["timestamp"]
                    for log in attendance
                    if log.get("timestamp")
                })

                subject.pop("subject_students", None)
                subject.pop("attendance_logs", None)

            return subjects

        except Exception as exc:
            last_error = exc

            if attempt < 2:
                time.sleep(1)

    raise last_error


def enroll_student_to_subject(student_id, subject_id):
    data = {
        "student_id": student_id,
        "subject_id": subject_id
    }

    response = (
        supabase_admin
        .table("subject_students")
        .insert(data)
        .execute()
    )

    return response.data


def unenroll_student_to_subject(student_id, subject_id):
    response = (
        supabase_admin
        .table("subject_students")
        .delete()
        .eq("student_id", student_id)
        .eq("subject_id", subject_id)
        .execute()
    )

    return response.data


def get_student_subjects(student_id):
    """
    Fetch enrolled subjects and return the nested structure
    expected by student_screen.py.
    """

    if student_id is None:
        return []

    try:
        student_id = int(student_id)

        enrollment_response = (
            supabase_admin
            .table("subject_students")
            .select("subject_id")
            .eq("student_id", student_id)
            .execute()
        )

        enrollments = enrollment_response.data or []

        if not enrollments:
            return []

        subject_ids = list(dict.fromkeys(
            int(row["subject_id"])
            for row in enrollments
            if row.get("subject_id") is not None
        ))

        if not subject_ids:
            return []

        subjects_response = (
            supabase_admin
            .table("subjects")
            .select("*")
            .in_("subject_id", subject_ids)
            .execute()
        )

        subject_rows = subjects_response.data or []

        subjects_by_id = {
            int(subject["subject_id"]): subject
            for subject in subject_rows
            if subject.get("subject_id") is not None
        }

        result = []

        for row in enrollments:
            subject_id = row.get("subject_id")

            if subject_id is None:
                continue

            subject_id = int(subject_id)
            subject = subjects_by_id.get(subject_id)

            if subject is not None:
                result.append({
                    "subject_id": subject_id,
                    "subjects": subject
                })

        return result

    except Exception as exc:
        error_message = f"{type(exc).__name__}: {exc}"

        print(
            f"get_student_subjects failed for "
            f"student_id={student_id}: {error_message}"
        )

        # Display the actual database error during debugging.
        import streamlit as st

        st.error(
            f"Could not load enrolled subjects for "
            f"student ID {student_id}: {error_message}"
        )

        return []

def has_attendance_today(student_id, subject_id):
    """Return True if attendance already exists for this student and subject today in IST."""
    student_id = int(student_id)
    subject_id = int(subject_id)

    ist = timezone(timedelta(hours=5, minutes=30))
    now_ist = datetime.now(ist)

    start_ist = now_ist.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )
    end_ist = start_ist + timedelta(days=1)

    start_utc = start_ist.astimezone(timezone.utc).isoformat()
    end_utc = end_ist.astimezone(timezone.utc).isoformat()

    response = (
        supabase_admin
        .table("attendance_logs")
        .select("id")
        .eq("student_id", student_id)
        .eq("subject_id", subject_id)
        .gte("timestamp", start_utc)
        .lt("timestamp", end_utc)
        .limit(1)
        .execute()
    )

    return bool(response.data)


def create_attendance(logs):
    if not logs:
        return []

    allowed_logs = []

    # India calendar day (IST).
    ist = timezone(timedelta(hours=5, minutes=30))
    now_ist = datetime.now(ist)

    start_ist = now_ist.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )

    end_ist = start_ist + timedelta(days=1)

    # Convert IST boundaries to UTC.
    start_utc = start_ist.astimezone(
        timezone.utc
    ).isoformat()

    end_utc = end_ist.astimezone(
        timezone.utc
    ).isoformat()

    already_added = set()

    for log in logs:
        student_id = log.get("student_id")
        subject_id = log.get("subject_id")

        if student_id is None or subject_id is None:
            continue

        try:
            student_id = int(student_id)
            subject_id = int(subject_id)
        except (TypeError, ValueError, OverflowError):
            continue

        key = (student_id, subject_id)

        if key in already_added:
            continue

        existing = (
            supabase_admin
            .table("attendance_logs")
            .select("timestamp")
            .eq("student_id", student_id)
            .eq("subject_id", subject_id)
            .gte("timestamp", start_utc)
            .lt("timestamp", end_utc)
            .execute()
        )

        if existing.data:
            already_added.add(key)
            continue

        allowed_log = dict(log)
        allowed_log["student_id"] = student_id
        allowed_log["subject_id"] = subject_id

        allowed_logs.append(allowed_log)
        already_added.add(key)

    if not allowed_logs:
        return []

    response = (
        supabase_admin
        .table("attendance_logs")
        .insert(allowed_logs)
        .execute()
    )

    return response.data or []


def get_student_attendance(student_id):
    response = (
        supabase_admin
        .table("attendance_logs")
        .select("*, subjects(*)")
        .eq("student_id", student_id)
        .execute()
    )

    return response.data or []


def get_attendance_for_teacher(teacher_id):
    response = (
        supabase_admin
        .table("attendance_logs")
        .select("*, subjects!inner(*)")
        .eq("subjects.teacher_id", teacher_id)
        .execute()
    )

    return response.data or []

def get_teacher_by_email(email):
    try:
        response = (
            supabase_admin
            .table("teachers")
            .select(
                "teacher_id, username, name, email, auth_user_id"
            )
            .eq("email", email.strip())
            .execute()
        )

        if not response.data:
            return None

        if len(response.data) != 1:
            raise ValueError(
                "Multiple teacher accounts found for this email."
            )

        return response.data[0]

    except Exception as exc:
        print("Teacher email lookup failed:", repr(exc))
        raise

def update_teacher_password(
    teacher_id,
    auth_user_id,
    new_password
):
    if not auth_user_id:
        raise ValueError(
            "Teacher does not have a linked Auth account."
        )

    response = (
        supabase_admin
        .table("teachers")
        .update({
            "password": hash_pass(new_password)
        })
        .eq("teacher_id", teacher_id)
        .eq("auth_user_id", auth_user_id)
        .execute()
    )

    if not response.data:
        raise ValueError(
            "Teacher/Auth identity verification failed."
        )

    return response.data
