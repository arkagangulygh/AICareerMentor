
import { useState } from "react";
import api from "../services/api";
import Sidebar from "../components/Sidebar";

function Interview() {

    const [interviewId, setInterviewId] = useState(null);
    const [sessionId, setSessionId] = useState(null);

    const [question, setQuestion] = useState("");
    const [questionNumber, setQuestionNumber] = useState(0);
    const [totalQuestions, setTotalQuestions] = useState(5);

    const [answer, setAnswer] = useState("");

    const [result, setResult] = useState(null);

    const [loading, setLoading] = useState(false);
    const [answerLoading, setAnswerLoading] = useState(false);

    const [completed, setCompleted] = useState(false);


    // --------------------------------------------------
    // START INTERVIEW
    // --------------------------------------------------

    const handleStart = async () => {

        try {

            setLoading(true);

            const token = localStorage.getItem("token");

            const jobId = localStorage.getItem("latestJobId");

            if (!jobId) {

                alert(
                    "Please analyze a job first."
                );

                return;
            }


            const response = await api.post(
                `/interview/start?job_id=${jobId}`,
                {},
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );


            console.log(
                "INTERVIEW START RESPONSE:",
                response.data
            );


            setInterviewId(
                response.data.interview_id
            );

            setSessionId(
                response.data.session_id
            );

            setQuestion(
                response.data.question
            );

            setQuestionNumber(
                response.data.question_number
            );

            setTotalQuestions(
                response.data.total_questions
            );

            setAnswer("");

            setResult(null);

            setCompleted(false);


        } catch (error) {

            console.log(error);

            alert(
                error.response?.data?.detail ||
                "Failed to start interview."
            );

        } finally {

            setLoading(false);

        }
    };


    // --------------------------------------------------
    // SUBMIT ANSWER
    // --------------------------------------------------

    const handleAnswer = async () => {

        if (!answer.trim()) {

            alert(
                "Please enter your answer."
            );

            return;
        }


        try {

            setAnswerLoading(true);

            const token = localStorage.getItem("token");


            const response = await api.post(
                "/interview/answer",
                {
                    interview_id: interviewId,
                    answer: answer
                },
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );


            console.log(
                "INTERVIEW ANSWER RESPONSE:",
                response.data
            );


            // Save feedback for current question
            if (response.data.completed_question) {

                setResult(
                    response.data.completed_question
                );

            } else {

                setResult({
                    score: response.data.score,
                    feedback: response.data.feedback
                });

            }


            setAnswer("");


            // --------------------------------------------------
            // CHECK IF INTERVIEW IS COMPLETE
            // --------------------------------------------------

            if (
                response.data.next_question === false
            ) {

                setCompleted(true);

                return;
            }


            // --------------------------------------------------
            // LOAD NEXT QUESTION
            // --------------------------------------------------

            if (response.data.next_question) {

                setInterviewId(
                    response.data.next_question.interview_id
                );

                setQuestion(
                    response.data.next_question.question
                );

                setQuestionNumber(
                    response.data.next_question.question_number
                );

                setTotalQuestions(
                    response.data.next_question.total_questions
                );

            }


        } catch (error) {

            console.log(error);

            alert(
                error.response?.data?.detail ||
                "Failed to submit answer."
            );

        } finally {

            setAnswerLoading(false);

        }
    };


    // --------------------------------------------------
    // NEW INTERVIEW
    // --------------------------------------------------

    const handleNewInterview = () => {

        setInterviewId(null);
        setSessionId(null);
        setQuestion("");
        setQuestionNumber(0);
        setAnswer("");
        setResult(null);
        setCompleted(false);

    };


    return (
        <div className="dashboard-layout">

            <Sidebar />

            <main className="dashboard-content">

                <div className="interview-page">

                    <h1>
                        Mock Interview
                    </h1>

                    <p>
                        Practice interview questions
                        and get AI feedback.
                    </p>


                    {/* START INTERVIEW */}

                    {!interviewId && !completed && (

                        <button
                            className="interview-start-button"
                            onClick={handleStart}
                            disabled={loading}
                        >

                            {loading
                                ? "Starting..."
                                : "Start Interview"
                            }

                        </button>

                    )}


                    {/* INTERVIEW */}

                    {interviewId && !completed && (

                        <div className="interview-container">


                            {/* QUESTION NUMBER */}

                            <div className="question-progress">

                                <p>
                                    Question {questionNumber} of{" "}
                                    {totalQuestions}
                                </p>

                            </div>


                            {/* QUESTION */}

                            <div className="question-card">

                                <h2>
                                    Interview Question
                                </h2>

                                <p>
                                    {question}
                                </p>

                            </div>


                            {/* ANSWER */}

                            <div className="answer-card">

                                <textarea
                                    placeholder="Type your answer here..."
                                    value={answer}
                                    onChange={(e) =>
                                        setAnswer(e.target.value)
                                    }
                                    rows="8"
                                />


                                <button
                                    className="interview-submit-button"
                                    onClick={handleAnswer}
                                    disabled={answerLoading}
                                >

                                    {answerLoading
                                        ? "Evaluating..."
                                        : "Submit Answer"
                                    }

                                </button>

                            </div>


                            {/* FEEDBACK */}

                            {result && (

                                <div className="interview-result">

                                    <h2>
                                        AI Feedback
                                    </h2>


                                    {result.score !== undefined &&
                                        result.score !== null && (

                                            <div className="interview-score">

                                                <span>
                                                    {result.score}/10
                                                </span>

                                                <p>
                                                    Score
                                                </p>

                                            </div>

                                        )}


                                    {result.feedback && (

                                        <div>

                                            <h3>
                                                Feedback
                                            </h3>

                                            <p>
                                                {result.feedback}
                                            </p>

                                        </div>

                                    )}

                                </div>

                            )}

                        </div>

                    )}


                    {/* INTERVIEW COMPLETED */}

                    {completed && (

                        <div className="interview-result">

                            <h2>
                                Interview Completed 🎉
                            </h2>

                            <p>
                                You have completed all{" "}
                                {totalQuestions} interview questions.
                            </p>


                            <button
                                className="interview-start-button"
                                onClick={handleNewInterview}
                            >
                                Start New Interview
                            </button>

                        </div>

                    )}

                </div>

            </main>

        </div>
    );
}

export default Interview;
