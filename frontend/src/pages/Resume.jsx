
import { useState } from "react";
import api from "../services/api";
import Sidebar from "../components/Sidebar";

function Resume() {

    const [file, setFile] = useState(null);
    const [message, setMessage] = useState("");
    const [loading, setLoading] = useState(false);
    const [resumeData, setResumeData] = useState(null);

    
const handleUpload = async (e) => {

    e.preventDefault();

    if (!file) {
        setMessage("Please select a PDF resume.");
        return;
    }

    const formData = new FormData();

    formData.append("file", file);

    try {

        setLoading(true);
        setMessage("");
        setResumeData(null);

        const token = localStorage.getItem("token");

        const uploadResponse = await api.post(
            "/resume/upload",
            formData,
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                    "Content-Type": "multipart/form-data"
                }
            }
        );

        console.log(
            "RESUME UPLOAD RESPONSE:",
            uploadResponse.data
        );

        const resumeId = uploadResponse.data.resume_id;

        // Step 2: Get resume analysis
        const scoreResponse = await api.get(
            `/resume/score/${resumeId}`,
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        console.log(
            "RESUME SCORE RESPONSE:",
            scoreResponse.data
        );

        setResumeData(scoreResponse.data);

        setMessage(
            "Resume uploaded and analyzed successfully!"
        );

    } catch (error) {

        console.log(error);

        setMessage(
            error.response?.data?.detail ||
            "Resume analysis failed."
        );

    } finally {

        setLoading(false);

    }
};




    return (
        <div className="dashboard-layout">

            <Sidebar />

            <main className="dashboard-content">

                <div className="resume-page">

                    <h1>Resume</h1>

                    <p className="resume-subtitle">
                        Upload your resume to analyze your profile.
                    </p>


                    {/* Upload Card */}

                    <div className="resume-card">

                        <div className="resume-card-header">

                            <h2>
                                Upload Your Resume
                            </h2>

                            <p>
                                Upload your PDF resume and let AI
                                analyze your skills and profile.
                            </p>

                        </div>


                        <form
                            className="resume-form"
                            onSubmit={handleUpload}
                        >

                            <div className="resume-file-box">

                                <input
                                    id="resume-file"
                                    type="file"
                                    accept=".pdf"
                                    onChange={(e) =>
                                        setFile(
                                            e.target.files[0]
                                        )
                                    }
                                />

                                <label htmlFor="resume-file">
                                    {file
                                        ? file.name
                                        : "Choose PDF Resume"}
                                </label>

                                <span>
                                    PDF files only
                                </span>

                            </div>


                            <button
                                type="submit"
                                className="resume-upload-button"
                                disabled={loading}
                            >
                                {loading
                                    ? "Analyzing..."
                                    : "Upload Resume"}
                            </button>

                        </form>


                        {message && (

                            <div className="resume-message">
                                {message}
                            </div>

                        )}

                    </div>


                    {/* Resume Analysis */}

                    {resumeData && (

                        <div className="resume-analysis">

                            <h2>
                                Resume Analysis
                            </h2>


                            {/* Score */}

                            <div className="resume-score-card">

                                <div className="resume-score">

                                    <span>
                                        {resumeData.score ?? 0}
                                    </span>

                                    <p>
                                        Resume Score
                                    </p>

                                </div>

                                <div className="resume-score-info">

                                    <h3>
                                        Overall Resume Score
                                    </h3>

                                    <p>
                                        Your resume has been analyzed
                                        based on skills and important
                                        resume sections.
                                    </p>

                                </div>

                            </div>


                            {/* Skills */}

                            <div className="resume-section">

                                <h3>
                                    Skills Found
                                </h3>

                                {resumeData.skills_found?.length > 0 ? (

                                    <div className="skills-list">

                                        {resumeData.skills_found.map(
                                            (skill, index) => (

                                                <span
                                                    className="skill-tag"
                                                    key={index}
                                                >
                                                    {skill}
                                                </span>

                                            )
                                        )}

                                    </div>

                                ) : (

                                    <p>
                                        No skills detected.
                                    </p>

                                )}

                            </div>


                            {/* Suggestions */}

                            <div className="resume-section">

                                <h3>
                                    Suggestions
                                </h3>

                                {resumeData.suggestions?.length > 0 ? (

                                    <ul className="suggestions-list">

                                        {resumeData.suggestions.map(
                                            (suggestion, index) => (

                                                <li key={index}>
                                                    {suggestion}
                                                </li>

                                            )
                                        )}

                                    </ul>

                                ) : (

                                    <p>
                                        Your resume looks good based
                                        on the current analysis. 🎉
                                    </p>

                                )}

                            </div>

                        </div>

                    )}

                </div>

            </main>

        </div>
    );
}

export default Resume;
