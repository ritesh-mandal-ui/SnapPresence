
import io
import numpy as np
import librosa

from resemblyzer import VoiceEncoder, preprocess_wav


VOICE_MATCH_THRESHOLD = 0.70

_encoder = None


def get_encoder():
    global _encoder

    if _encoder is None:
        _encoder = VoiceEncoder()

    return _encoder


def get_voice_embedding(audio_bytes):
    try:
        audio_buffer = io.BytesIO(audio_bytes)

        audio, sample_rate = librosa.load(
            audio_buffer,
            sr=16000,
            mono=True
        )

        if audio is None or len(audio) == 0:
            return None

        wav = preprocess_wav(audio)

        encoder = get_encoder()

        embedding = encoder.embed_utterance(wav)

        return embedding.astype(np.float32).tolist()

    except Exception:
        return None


def cosine_similarity(embedding_a, embedding_b):
    try:
        a = np.asarray(
            embedding_a,
            dtype=np.float32
        )

        b = np.asarray(
            embedding_b,
            dtype=np.float32
        )

        if a.size == 0 or b.size == 0:
            return 0.0

        if a.shape != b.shape:
            return 0.0

        a_norm = np.linalg.norm(a)
        b_norm = np.linalg.norm(b)

        if a_norm == 0 or b_norm == 0:
            return 0.0

        return float(
            np.dot(a, b) / (a_norm * b_norm)
        )

    except Exception:
        return 0.0


def process_bulk_audio(
    audio_bytes,
    candidates_dict,
    threshold=VOICE_MATCH_THRESHOLD
):
    try:
        audio_buffer = io.BytesIO(audio_bytes)

        audio, sample_rate = librosa.load(
            audio_buffer,
            sr=16000,
            mono=True
        )

        if audio is None or len(audio) == 0:
            return {}

        wav = preprocess_wav(audio)

        encoder = get_encoder()

        detected_embedding = encoder.embed_utterance(wav)

        detected_scores = {}

        for student_id, candidate_embedding in candidates_dict.items():

            score = cosine_similarity(
                detected_embedding,
                candidate_embedding
            )

            if score >= threshold:
                detected_scores[int(student_id)] = score

        return detected_scores

    except Exception:
        return {}

