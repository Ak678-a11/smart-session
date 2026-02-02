import StudentPortal from "./components/StudentPortal.jsx";
import TeacherDashboard from "./components/TeacherDashboard.jsx";
import "./App.css";

function App() {
  return (
    <div className="container">
      <h1>Smart Session Monitoring System</h1>

      <StudentPortal />
      <TeacherDashboard />
    </div>
  );
}

export default App;