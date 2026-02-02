# Smart Session Monitoring

**Smart Session Monitoring** is a real-time student attention and engagement monitoring system. It uses computer vision to track student faces, gaze direction, and confusion levels, providing teachers with a live dashboard for classroom insights.

---

## Problem Statement
Monitoring student attention in online or hybrid classrooms is challenging. Teachers often cannot gauge confusion or engagement in real-time. This project aims to provide a **live, automated solution** for tracking student focus and engagement metrics.

---

## Approach
1. **Student Camera Capture**: Students’ webcams capture frames periodically.  
2. **Face & Gaze Detection**: Detect number of faces and gaze direction using dlib.  
3. **Emotion Analysis**: Compute confusion scores and basic emotional indicators (smile, brow furrow, head tilt).  
4. **Status Determination**: Simple state machine classifies engagement status (focused/confused/idle).  
5. **Telemetry Storage**: Session data is stored in-memory for teacher dashboard visualization.  
6. **Live Dashboard**: Teachers see a session timeline with confusion scores and engagement in real-time.  
7. **WebSocket Support**: Enables real-time updates from students to teacher dashboard.  

---

## Tech Stack

**Backend**  
- Python 3.10+  
- FastAPI  
- OpenCV, dlib  
- NumPy  
- Uvicorn  
- WebSockets  

**Frontend**  
- React.js (Vite)  
- HTML/CSS/JS  
- WebSocket client for live updates  

---

Usage
Student opens portal → allows webcam access.
Click Start Analysis → frames are sent to backend every 2 seconds.
Teacher dashboard receives live session data → visualizes confusion scores and engagement.
Click Stop to end analysis and release the webcam.

---

Limitations
Currently only detects confusion; other emotions are placeholders.
Works best with single face; multiple faces may affect accuracy.
Real-time performance depends on camera quality and network speed.
Session data is stored in-memory → not persistent across server restarts.
WebSocket live updates need proper deployment to work outside localhost.

---

Future Work
Add full emotion recognition (happiness, boredom, frustration).
Persistent database storage for session history.
Mobile browser support.
Multi-student monitoring in classrooms.
