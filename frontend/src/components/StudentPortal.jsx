import { useEffect, useRef, useState } from "react";

const API = "http://127.0.0.1:8000";
const WS_URL = "ws://127.0.0.1:8000/ws";

export default function StudentPortal() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const wsRef = useRef(null);
  const [status, setStatus] = useState("Idle");
  const [running, setRunning] = useState(false);

  // -------------------- WEBSOCKET --------------------
  useEffect(() => {
    wsRef.current = new WebSocket(WS_URL);

    wsRef.current.onopen = () => console.log("WebSocket connected");
    wsRef.current.onmessage = (event) => {
      console.log("WS message:", event.data);
    };
    wsRef.current.onclose = () => console.log("WebSocket disconnected");

    return () => {
      wsRef.current.close();
    };
  }, []);

  // -------------------- CAMERA --------------------
  const startCamera = () => {
    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then((stream) => {
        videoRef.current.srcObject = stream;
        setRunning(true);
        setStatus("Analyzing");
      })
      .catch((err) => console.error("Camera error:", err));
  };

  const stopCamera = () => {
    setRunning(false);
    setStatus("Idle");

    const stream = videoRef.current?.srcObject;
    if (stream) {
      stream.getTracks().forEach((track) => track.stop());
      videoRef.current.srcObject = null;
    }

    // Optional: notify backend
    wsRef.current?.send(JSON.stringify({ type: "STOP_ANALYSIS" }));
  };

  // -------------------- SEND FRAME --------------------
  const sendFrame = async () => {
    if (!running) return;

    const video = videoRef.current;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(async (blob) => {
      const formData = new FormData();
      formData.append("file", blob, "frame.jpg");

      try {
        const res = await fetch(`${API}/analyze-frame`, {
          method: "POST",
          body: formData,
        });
        const data = await res.json();

        if (!data.error) {
          setStatus(data.status || "Analyzing");
        } else {
          setStatus("Error");
          console.error(data.error);
        }
      } catch (err) {
        console.error(err);
        setStatus("Error");
      }
    }, "image/jpeg");
  };

  // -------------------- FRAME LOOP --------------------
  useEffect(() => {
    if (!running) return;

    const interval = setInterval(sendFrame, 2000); // every 2 seconds
    return () => clearInterval(interval);
  }, [running]);

  // -------------------- JSX --------------------
  return (
    <div className="card">
      <h2>Student Live Camera</h2>

      <video
        ref={videoRef}
        autoPlay
        playsInline
        width="320"
        style={{ borderRadius: "8px" }}
      />

      <canvas ref={canvasRef} style={{ display: "none" }} />

      <div style={{ marginTop: "10px" }}>
        <button onClick={startCamera}>Start Analysis</button>
        <button onClick={stopCamera} style={{ marginLeft: "10px" }}>
          Stop
        </button>
      </div>

      <p>Status: {status}</p>
    </div>
  );
}