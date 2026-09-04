
import { useState } from "react";
import api from "../services/api";
import Sidebar from "../components/Sidebar";

function SkillGap() {

    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);


    const handleAnalyze = async () => {

        try {

            setLoading(true);

            const token = localStorage.getItem("token");

            // Get the latest job ID
            const jobId = localStorage.getItem("latestJobId");

            if (!jobId) {

                alert(
                    "Please analyze a job first."
                );

                return;
            }


            const response = await api.post(
                `/skills/analyze?job_id=${jobId}`,
                {},
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );


            console.log(
                "SKILL GAP RESPONSE:",
                response.data
            );

            setResult(response.data);


        } catch (error) {

            console.log(error);

            alert(
                error.response?.data?.detail ||
                "Skill gap analysis failed."
            );

        } finally {

            setLoading(false);

        }
    };


    return (
        <div className="dashboard-layout">

            <Sidebar />

            <main className="dashboard-content">

                <div className="skills-page">

                    <h1>Skill Gap Analysis</h1>

                    <p>
                        Find out which skills you need to improve
                        for your latest job.
                    </p>


                    <button
                        className="skill-analyze-button"
                        onClick={handleAnalyze}
                        disabled={loading}
                    >

                        {loading
                            ? "Analyzing..."
                            : "Analyze Skill Gap"
                        }

                    </button>


                    {result && (

                        <div className="skill-result">

                            <h2>
                                Skill Analysis
                            </h2>


                            <p>
                                <strong>Job:</strong>{" "}
                                {result.job_title}
                            </p>


                            <h3>
                                Matched Skills
                            </h3>


                            {result.matched_skills?.length > 0 ? (

                                <ul>

                                    {result.matched_skills.map(
                                        (skill, index) => (

                                            <li key={index}>
                                                {skill}
                                            </li>

                                        )
                                    )}

                                </ul>

                            ) : (

                                <p>
                                    No matched skills found.
                                </p>

                            )}


                            <h3>
                                Missing Skills
                            </h3>


                            {result.skill_gap?.length > 0 ? (

                                <ul>

                                    {result.skill_gap.map(
                                        (item, index) => (

                                            <li key={index}>

                                                {item.skill}
                                                {" — "}
                                                {item.priority}

                                            </li>

                                        )
                                    )}

                                </ul>

                            ) : (

                                <p>
                                    No skill gaps found 🎉
                                </p>

                            )}

                        </div>

                    )}

                </div>

            </main>

        </div>
    );
}

export default SkillGap;
