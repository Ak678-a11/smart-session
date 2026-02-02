from collections import deque
from datetime import datetime

SESSION_BUFFER_SIZE = 100
session_data = deque(maxlen=SESSION_BUFFER_SIZE)


def add_session_entry(face_count: int, confusion_score: float, status: str):
    session_data.append({
        "timestamp": datetime.utcnow().isoformat(),
        "face_count": face_count,
        "confusion_score": round(confusion_score, 2),
        "status": status
    })


def get_session():
    return list(session_data)