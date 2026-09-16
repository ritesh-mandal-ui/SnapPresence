import time
import bcrypt

from src.database.config import supabase


# =========================================================
# TEACHER AUTHENTICATION
# =========================================================

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
    name
):
    data = {
        "username": username,
        "password": hash_pass(password),
        "name": name
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


# =========================================================
# STUDENT MANAGEMENT
# =========================================================

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


# =========================================================
# SUBJECT MANAGEMENT
# =========================================================

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

                # -----------------------------------------
                # TOTAL ENROLLED STUDENTS
                # -----------------------------------------

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

                # -----------------------------------------
                # TOTAL CLASSES
                # -----------------------------------------

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

                # -----------------------------------------
                # REMOVE RAW RELATION DATA
                # -----------------------------------------

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


# =========================================================
# SUBJECT ENROLLMENT
# =========================================================

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


# =========================================================
# ATTENDANCE
# =========================================================

def create_attendance(logs):

    if not logs:
        return []

    response = (
        supabase
        .table("attendance_logs")
        .insert(logs)
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