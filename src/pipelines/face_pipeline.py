import numpy as np
import dlib
import face_recognition_models

from src.database.db import get_all_students


FACE_MATCH_THRESHOLD = 0.50

_detector = None
_shape_predictor = None
_face_recognition_model = None
_model_cache = None


def get_detector():
    global _detector

    if _detector is None:
        _detector = dlib.get_frontal_face_detector()

    return _detector


def get_shape_predictor():
    global _shape_predictor

    if _shape_predictor is None:
        model_path = face_recognition_models.pose_predictor_model_location()
        _shape_predictor = dlib.shape_predictor(model_path)

    return _shape_predictor


def get_face_recognition_model():
    global _face_recognition_model

    if _face_recognition_model is None:
        model_path = face_recognition_models.face_recognition_model_location()
        _face_recognition_model = dlib.face_recognition_model_v1(
            model_path
        )

    return _face_recognition_model


def get_face_embeddings(image):
    try:
        image = np.asarray(image)

        if image is None or image.size == 0:
            return []

        if image.ndim != 3:
            return []

        if image.shape[2] != 3:
            return []

        image = np.ascontiguousarray(image)

        detector = get_detector()
        predictor = get_shape_predictor()
        recognition_model = get_face_recognition_model()

        faces = detector(image, 1)

        embeddings = []

        for face in faces:
            shape = predictor(image, face)

            embedding = recognition_model.compute_face_descriptor(
                image,
                shape
            )

            embeddings.append(
                np.asarray(
                    embedding,
                    dtype=np.float32
                )
            )

        return embeddings

    except Exception:
        return []


def get_trained_model():
    global _model_cache

    if _model_cache is not None:
        return _model_cache

    try:
        students = get_all_students()

        X = []
        y = []

        for student in students:
            student_id = student.get("student_id")
            face_embedding = student.get("face_embedding")

            if student_id is None:
                continue

            if face_embedding is None:
                continue

            try:
                embedding = np.asarray(
                    face_embedding,
                    dtype=np.float32
                )

                if embedding.shape != (128,):
                    continue

                if not np.all(np.isfinite(embedding)):
                    continue

                X.append(embedding)
                y.append(int(student_id))

            except Exception:
                continue

        if not X:
            _model_cache = {
                "X": np.empty((0, 128), dtype=np.float32),
                "y": np.empty((0,), dtype=np.int64)
            }

            return _model_cache

        _model_cache = {
            "X": np.asarray(
                X,
                dtype=np.float32
            ),
            "y": np.asarray(
                y,
                dtype=np.int64
            )
        }

        return _model_cache

    except Exception:
        return None


def clear_face_model_cache():
    global _model_cache
    _model_cache = None


def predict_attendance(
    image_np,
    allowed_student_ids=None
):
    encodings = get_face_embeddings(image_np)

    face_count = len(encodings)

    if not encodings:
        return {}, None, 0

    model_data = get_trained_model()

    if model_data is None:
        return {}, encodings, face_count

    X = model_data["X"]
    y = model_data["y"]

    if X is None or len(X) == 0:
        return {}, encodings, face_count

    if y is None or len(y) == 0:
        return {}, encodings, face_count

    allowed_ids = None

    if allowed_student_ids is not None:
        allowed_ids = {
            int(student_id)
            for student_id in allowed_student_ids
        }

    detected = {}

    for face_embedding in encodings:

        distances = np.linalg.norm(
            X - face_embedding,
            axis=1
        )

        if len(distances) == 0:
            continue

        best_index = int(
            np.argmin(distances)
        )

        best_distance = float(
            distances[best_index]
        )

        student_id = int(
            y[best_index]
        )

        if allowed_ids is not None:
            if student_id not in allowed_ids:
                continue

        if best_distance <= FACE_MATCH_THRESHOLD:
            detected[student_id] = best_distance

    return detected, encodings, face_count