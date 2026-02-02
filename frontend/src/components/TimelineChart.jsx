export default function TimelineChart({ data }) {
  if (!data || data.length === 0) return null;

  return (
    <div style={{ marginTop: "15px" }}>
      <h3>Session Timeline</h3>
      {data.map((d, i) => (
        <div key={i} style={{ fontSize: "13px" }}>
          Faces: {d.face_count} | Confusion: {d.confusion_score}
        </div>
      ))}
    </div>
  );
}