import { useEffect, useState } from "react";
import TimelineChart from "./TimelineChart.jsx";

const API = "http://127.0.0.1:8000";

export default function TeacherDashboard() {
  const [session, setSession] = useState([]);

  const fetchSession = async () => {
    try {
      const res = await fetch(`${API}/session`);
      const data = await res.json();
      setSession(data.reverse());
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchSession();
    const interval = setInterval(fetchSession, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="card">
      <h2>Teacher Dashboard</h2>

      {session.length === 0 && <p>No session data yet</p>}

      {session.map((s, i) => (
        <div key={i} className="session-row">
          <span>👤 Faces: {s.face_count}</span>
          <span>😕 Confusion: {s.confusion_score}</span>
          <span>📌 {s.status}</span>
        </div>
      ))}

      <TimelineChart data={session} />
    </div>
  );
}