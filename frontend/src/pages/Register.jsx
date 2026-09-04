import { useState } from "react"
import api from "../services/api";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";
function Register()
{
    const [name,setName]=useState("");
    const [email,setEmail]=useState("");
    const [password,setPassword]=useState("");
    const navigate=useNavigate()
    const handleRegister = async (e) => {
    e.preventDefault();

    try {
      const response = await api.post("/auth/register", {name,email,password,});
      console.log(response.data);
      alert("Registration successful!");
      navigate("/login");
    } 
    catch (error) {
  console.log("STATUS:", error.response?.status);
  console.log("DATA:", error.response?.data);
  console.log("ERROR:", error);

  alert(
    error.response?.data?.detail ||
    "Registration failed"
  );
}
}
    return(
        <div className="auth-container">
            <div className="auth-card">
                <h1>Create Account</h1>
                <p>Start your career journey</p>
                <form onSubmit={handleRegister}>
                    <input type="text" placeholder="Your Full Name" value={name} onChange={(e)=>setName(e.target.value)}></input>
                    <input type="email" placeholder="Enter Email-ID" value={email} onChange={(e)=>setEmail(e.target.value)}></input>
                    <input type="password" placeholder="Enter Password" value={password} onChange={(e)=>setPassword(e.target.value)}></input>
                    <button type="submit">Create Account</button>
                </form>
                <p>
                    Already have an Account? <Link to="/login">Login</Link>
                </p>
            </div>
        </div>
    )
}
export default Register;