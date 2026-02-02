from pydantic import BaseModel
from datetime import datetime

class SessionEntry(BaseModel):
    timestamp: datetime
    face_count: int
    confusion_score: float
    status: str