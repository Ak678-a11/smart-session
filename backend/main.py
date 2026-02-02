from fastapi import FastAPI, UploadFile, File, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
import os
import uvicorn

from session_manager import add_session_entry, get_session
from ml.emotion_logic import compute_confusion_score
from ml.gaze_tracker import detect_gaze_and_faces
from state_machine import determine_status

app = FastAPI()

# -------------------- CORS --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- WEBSOCKET MANAGER --------------------
active_connections: list[WebSocket] = []

async def broadcast(data: dict):
    for ws in active_connections:
        await ws.send_json(data)

# -------------------- ROOT --------------------
@app.get("/")
def root():
    return {"status": "Smart Sessions Backend Running"}

# -------------------- WEBSOCKET --------------------
@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    active_connections.append(ws)
    try:
        while True:
            await ws.receive_text()  # keep alive
    except WebSocketDisconnect:
        active_connections.remove(ws)

# -------------------- ANALYZE FRAME --------------------
@app.post("/analyze-frame")
async def analyze_frame(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        np_img = np.frombuffer(contents, np.uint8)
        frame = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        if frame is None:
            return {"error": "Invalid image"}

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        face_count, gaze_direction = detect_gaze_and_faces(gray)

        confusion_score = compute_confusion_score(
            face_count=face_count,
            gaze_direction=gaze_direction,
            brow_furrow=False,
            smiling=False,
            head_tilt=False
        )

        status = determine_status(confusion_score)

        entry = {
            "face_count": face_count,
            "gaze": gaze_direction,
            "confusion_score": round(confusion_score, 2),
            "status": status
        }

        add_session_entry(
            face_count=face_count,
            confusion_score=confusion_score,
            status=status
        )

        # 🔥 SEND LIVE UPDATE
        await broadcast(entry)

        return entry

    except Exception as e:
        return {"error": str(e)}

# -------------------- SESSION DATA --------------------
@app.get("/session")
def session_data():
    return get_session()

# -------------------- LATEST SESSION --------------------
@app.get("/latest-session")
def latest_session():
    data = get_session()
    if not data:
        return {
            "face_count": 0,
            "confusion_score": 0,
            "status": "Idle"
        }
    return data[-1]

# -------------------- RUN --------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)