
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import ProtectedRoute from "./components/ProtectedRoute";
import Resume from "./pages/Resume";
import Jobs from "./pages/Jobs";
import SkillGap from "./pages/Skillgap";
import Interview from "./pages/Interview";
import WeeklyTest from "./pages/WeeklyTest";

import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom";


function App() {

  return (

    <BrowserRouter>

      <Routes>

        <Route
          path="/"
          element={<Login />}
        />

        <Route
          path="/login"
          element={<Login />}
        />

        <Route
          path="/register"
          element={<Register />}
        />


        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />


        <Route
          path="/resume"
          element={
            <ProtectedRoute>
              <Resume />
            </ProtectedRoute>
          }
        />


        <Route
          path="/jobs"
          element={
            <ProtectedRoute>
              <Jobs />
            </ProtectedRoute>
          }
        />


        <Route
          path="/skills"
          element={
            <ProtectedRoute>
              <SkillGap />
            </ProtectedRoute>
          }
        />


        <Route
          path="/interview"
          element={
            <ProtectedRoute>
              <Interview />
            </ProtectedRoute>
          }
        />


        <Route
          path="/test"
          element={
            <ProtectedRoute>
              <WeeklyTest />
            </ProtectedRoute>
          }
        />

      </Routes>

    </BrowserRouter>
  );
}


export default App;
