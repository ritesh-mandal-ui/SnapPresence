
import time
import bcrypt

from datetime import datetime, timedelta, timezone

from src.database.config import supabase


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
        supabase
        .table("teachers")
        .select("username")
        .eq("username", username)
        .execute()
    )

    return len(response.data) > 0


def create_teacher(
    username,
    password,
    name,
    email
):
    data = {
        "username": username,
        "password": hash_pass(password),
        "name": name,
        "email": email
    }

    response = (
        supabase
        .table("teachers")
        .insert(data)
        .execute()
    )

    return response.data


def teacher_login(
    username,
    password
):
    response = (
        supabase
        .table("teachers")
        .select("*")
        .eq("username", username)
        .execute()
    )

    if not response.data:
        return None

    teacher = response.data[0]

    try:
        if check_pass(
            password,
            teacher["password"]
        ):
            return teacher

    except (ValueError, TypeError):
        return None

    return None


def get_all_students():
    response = (
        supabase
        .table("students")
        .select("*")
        .execute()
    )

    return response.data


def create_student(
    new_name,
    face_embedding=None,
    voice_embedding=None
):
    data = {
        "name": new_name,
        "face_embedding": face_embedding,
        "voice_embedding": voice_embedding
    }

    response = (
        supabase
        .table("students")
        .insert(data)
        .execute()
    )

    return response.data


def update_student_voice_embedding(
    student_id,
    voice_embedding
):
    response = (
        supabase
        .table("students")
        .update({
            "voice_embedding": voice_embedding
        })
        .eq(
            "student_id",
            student_id
        )
        .execute()
    )

    return response.data


def create_subject(
    subject_code,
    name,
    section,
    teacher_id
):
    data = {
        "subject_code": subject_code,
        "name": name,
        "section": section,
        "teacher_id": teacher_id
    }

    response = (
        supabase
        .table("subjects")
        .insert(data)
        .execute()
    )

    return response.data


def delete_subject(subject_id):
    response = (
        supabase
        .table("subjects")
        .delete()
        .eq(
            "subject_id",
            subject_id
        )
        .execute()
    )

    return response.data


def get_teacher_subjects(teacher_id):
    last_error = None

    for attempt in range(3):
        try:
            response = (
                supabase
                .table("subjects")
                .select(
                    "*, subject_students(count), "
                    "attendance_logs(timestamp)"
                )
                .eq(
                    "teacher_id",
                    teacher_id
                )
                .execute()
            )

            subjects = response.data

            for subject in subjects:

                subject_students = subject.get(
                    "subject_students"
                )

                if subject_students:
                    subject["total_students"] = (
                        subject_students[0].get(
                            "count",
                            0
                        )
                    )
                else:
                    subject["total_students"] = 0

                attendance = subject.get(
                    "attendance_logs",
                    []
                )

                unique_sessions = len(
                    set(
                        log["timestamp"]
                        for log in attendance
                        if log.get("timestamp")
                    )
                )

                subject["total_classes"] = unique_sessions

                subject.pop(
                    "subject_students",
                    None
                )

                subject.pop(
                    "attendance_logs",
                    None
                )

            return subjects

        except Exception as e:
            last_error = e

            if attempt < 2:
                time.sleep(1)

    raise last_error


def enroll_student_to_subject(
    student_id,
    subject_id
):
    data = {
        "student_id": student_id,
        "subject_id": subject_id
    }

    response = (
        supabase
        .table("subject_students")
        .insert(data)
        .execute()
    )

    return response.data


def unenroll_student_to_subject(
    student_id,
    subject_id
):
    response = (
        supabase
        .table("subject_students")
        .delete()
        .eq(
            "student_id",
            student_id
        )
        .eq(
            "subject_id",
            subject_id
        )
        .execute()
    )

    return response.data


def get_student_subjects(student_id):
    response = (
        supabase
        .table("subject_students")
        .select("*, subjects(*)")
        .eq(
            "student_id",
            student_id
        )
        .execute()
    )

    return response.data


def create_attendance(logs):

    if not logs:
        return []

    allowed_logs = []

    # India calendar day (IST)
    IST = timezone(
        timedelta(hours=5, minutes=30)
    )

    now_ist = datetime.now(IST)

    start_ist = now_ist.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )

    end_ist = start_ist + timedelta(
        days=1
    )

    # Convert IST boundaries to UTC
    start_utc = start_ist.astimezone(
        timezone.utc
    ).isoformat()

    end_utc = end_ist.astimezone(
        timezone.utc
    ).isoformat()

    # Prevent duplicate entries
    # inside the same request
    already_added = set()

    for log in logs:

        student_id = log.get(
            "student_id"
        )

        subject_id = log.get(
            "subject_id"
        )

        if (
            student_id is None
            or subject_id is None
        ):
            continue

        key = (
            int(student_id),
            int(subject_id)
        )

        if key in already_added:
            continue

        existing = (
            supabase
            .table("attendance_logs")
            .select("timestamp")
            .eq(
                "student_id",
                int(student_id)
            )
            .eq(
                "subject_id",
                int(subject_id)
            )
            .gte(
                "timestamp",
                start_utc
            )
            .lt(
                "timestamp",
                end_utc
            )
            .execute()
        )

        if existing.data:
            continue

        allowed_logs.append(log)

        already_added.add(key)

    if not allowed_logs:
        return []

    response = (
        supabase
        .table("attendance_logs")
        .insert(allowed_logs)
        .execute()
    )

    return response.data


def get_student_attendance(student_id):
    response = (
        supabase
        .table("attendance_logs")
        .select("*, subjects(*)")
        .eq(
            "student_id",
            student_id
        )
        .execute()
    )

    return response.data


def get_attendance_for_teacher(teacher_id):
    response = (
        supabase
        .table("attendance_logs")
        .select(
            "*, subjects!inner(*)"
        )
        .eq(
            "subjects.teacher_id",
            teacher_id
        )
        .execute()
    )

    return response.data


def get_teacher_by_email(email):
    response = (
        supabase
        .table("teachers")
        .select("*")
        .eq("email", email)
        .execute()
    )

    if not response.data:
        return None

    return response.data[0]


def update_teacher_password(
    teacher_id,
    new_password
):
    response = (
        supabase
        .table("teachers")
        .update({
            "password": hash_pass(new_password)
        })
        .eq(
            "teacher_id",
            teacher_id
        )
        .execute()
    )

    return response.data

