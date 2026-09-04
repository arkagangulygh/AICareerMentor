
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import Sidebar from "../components/Sidebar";
function Dashboard() {

    const navigate = useNavigate();

    const [dashboardData, setDashboardData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {

        const fetchDashboard = async () => {

            try {

                const token = localStorage.getItem("token");

                const response = await api.get("/dashboard", {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                });

                console.log("DASHBOARD RESPONSE:", response.data);

                setDashboardData(response.data);

            } catch (error) {

                console.log(error);

                if (error.response?.status === 401) {
                    localStorage.removeItem("token");
                    navigate("/login");
                }

            } finally {

                setLoading(false);

            }
        };

        fetchDashboard();

    }, [navigate]);


    const handleLogout = () => {

        localStorage.removeItem("token");

        navigate("/login");

    };


    if (loading) {
        return <h2>Loading Dashboard...</h2>;
    }


    return (
            <div className="dashboard-layout">
                <Sidebar></Sidebar>
                <div className="dashboard-container">

                <div className="dashboard-header">

                    <div>
                        <h1>AI Career Mentor</h1>
                        <p>Welcome to your career dashboard.</p>
                    </div>

                    <button onClick={handleLogout}>
                        Logout
                    </button>

                </div>


                <div className="stats-container">

                    <div className="stat-card">

                        <h3>Resume Score</h3>

                        <h2>
                            {dashboardData?.resume?.score ?? 0}
                        </h2>

                        <p>Out of 100</p>

                    </div>


                    <div className="stat-card">

                        <h3>Job Match</h3>

                        <h2>
                            {dashboardData?.latest_job?.match_percentage ?? 0}%
                        </h2>

                        <p>Latest job match</p>

                    </div>


                    <div className="stat-card">

                        <h3>Interview Score</h3>

                        <h2>
                            {dashboardData?.latest_interview?.average_score ?? 0}
                        </h2>

                        <p>Average score</p>

                    </div>

                </div>

            </div>
            </div>
    );
}

export default Dashboard;
