import { NavLink } from "react-router-dom";
function Sidebar()
{
    return(
        <div className="sidebar">
            <h2>Ai Career Mentor</h2>
            <nav>
                <NavLink to="/dashboard">Dashboard</NavLink>
                <NavLink to="/resume">Resume</NavLink>
                <NavLink to="/jobs">Jobs</NavLink>
                <NavLink to="/interview">Mock Interview</NavLink>
                <NavLink to="/test">Weekly test</NavLink>
                <NavLink to="/skills">Skill gaps</NavLink>
            </nav>
        </div>
    )
}
export default Sidebar;