import { useState } from "react";
import api from "../services/api";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";
function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate=useNavigate();
  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const response = await api.post("/auth/login", {
        email,
        password,
      });

      console.log(response.data);

      const token = response.data.access_token;

      localStorage.setItem("token", token);

      alert("Login successful!");
      navigate("/dashboard");
    } catch (error) {
      console.log(error);
      alert(error.response?.data?.detail || "Login failed");
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h1>Welcome Back</h1>

        <p>Login to your AI Career Mentor</p>

        <form onSubmit={handleLogin}>
          <input
            type="email"
            placeholder="Enter Email-ID"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <input
            type="password"
            placeholder="Enter Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <button type="submit">Login</button>
        </form>
      </div>
    </div>
  );
}

export default Login;