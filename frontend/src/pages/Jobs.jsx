
import { useState } from "react";
import api from "../services/api";
import Sidebar from "../components/Sidebar";

function Jobs() {

    const [title, setTitle] = useState("");
    const [description, setDescription] = useState("");
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [matchResult, setMatchResult] = useState(null);
    const [matchLoading, setMatchLoading] = useState(false);


    const handleAnalyze = async (e) => {

        e.preventDefault();

        if (!title || !description) {
            alert("Please enter job title and description.");
            return;
        }

        try {

            setLoading(true);

            const token = localStorage.getItem("token");

            const response = await api.post(
                "/jobs/analyze",
                {
                    title: title,
                    description: description
                },
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );

            console.log("JOB RESPONSE:", response.data);

            setResult(response.data);

            // Store the latest job ID
            localStorage.setItem(
                "latestJobId",
                response.data.job_id
            );

            // Clear previous match result
            setMatchResult(null);

        } catch (error) {

            console.log(error);

            alert(
                error.response?.data?.detail ||
                "Job analysis failed."
            );

        } finally {

            setLoading(false);

        }
    };


    const handleMatch = async () => {

        try {

            setMatchLoading(true);

            const token = localStorage.getItem("token");

            const response = await api.post(
                `/jobs/match?job_id=${result.job_id}`,
                {},
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );

            console.log("MATCH RESPONSE:", response.data);

            setMatchResult(response.data);

        } catch (error) {

            console.log(error);

            alert(
                error.response?.data?.detail ||
                "Job matching failed."
            );

        } finally {

            setMatchLoading(false);

        }
    };


    return (
        <div className="dashboard-layout">

            <Sidebar />

            <main className="dashboard-content">

                <div className="jobs-page">

                    <h1>Job Analysis</h1>

                    <p>
                        Enter a job description to find the required skills.
                    </p>


                    <form
                        className="job-form"
                        onSubmit={handleAnalyze}
                    >

                        <input
                            type="text"
                            placeholder="Job Title"
                            value={title}
                            onChange={(e) => setTitle(e.target.value)}
                        />

                        <textarea
                            placeholder="Paste Job Description"
                            value={description}
                            onChange={(e) => setDescription(e.target.value)}
                            rows="10"
                        />

                        <button
                            type="submit"
                            disabled={loading}
                        >
                            {loading
                                ? "Analyzing..."
                                : "Analyze Job"
                            }
                        </button>

                    </form>


                    {result && (

                        <div className="job-result">

                            <h2>Analysis Result</h2>

                            <p>
                                Job ID: {result.job_id}
                            </p>

                            <h3>Required Skills</h3>

                            {result.required_skills?.length > 0 ? (

                                <ul>

                                    {result.required_skills.map(
                                        (skill, index) => (
                                            <li key={index}>
                                                {skill}
                                            </li>
                                        )
                                    )}

                                </ul>

                            ) : (

                                <p>
                                    No required skills detected.
                                </p>

                            )}


                            <button
                                type="button"
                                onClick={handleMatch}
                                disabled={matchLoading}
                            >
                                {matchLoading
                                    ? "Matching..."
                                    : "Match My Resume"
                                }
                            </button>

                        </div>

                    )}


                    {matchResult && (

                        <div className="match-result">

                            <h2>Resume Match</h2>

                            <div className="match-score">

                                <span>
                                    {matchResult.match_percentage}%
                                </span>

                                <p>
                                    Resume Match
                                </p>

                            </div>


                            <h3>Matched Skills</h3>

                            {matchResult.matched_skills?.length > 0 ? (

                                <ul>

                                    {matchResult.matched_skills.map(
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


                            <h3>Missing Skills</h3>

                            {matchResult.missing_skills?.length > 0 ? (

                                <ul>

                                    {matchResult.missing_skills.map(
                                        (skill, index) => (
                                            <li key={index}>
                                                {skill}
                                            </li>
                                        )
                                    )}

                                </ul>

                            ) : (

                                <p>
                                    No missing skills 🎉
                                </p>

                            )}

                        </div>

                    )}

                </div>

            </main>

        </div>
    );
}

export default Jobs;