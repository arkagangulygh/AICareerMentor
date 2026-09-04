
import { useState } from "react";
import api from "../services/api";
import Sidebar from "../components/Sidebar";

function WeeklyTest() {

    const [questions, setQuestions] = useState([]);
    const [testSessionId, setTestSessionId] = useState(null);

    const [currentQuestion, setCurrentQuestion] = useState(0);

    const [answer, setAnswer] = useState("");

    const [result, setResult] = useState(null);

    const [loading, setLoading] = useState(false);
    const [submitLoading, setSubmitLoading] = useState(false);

    const [completed, setCompleted] = useState(false);


    // --------------------------------------------------
    // GENERATE TEST
    // --------------------------------------------------

    const handleStartTest = async () => {

        try {

            setLoading(true);

            const token = localStorage.getItem("token");

            const response = await api.post(
                "/test/generate",
                {},
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );

            console.log(
                "TEST GENERATE RESPONSE:",
                response.data
            );
            console.log(
    "FIRST QUESTION:",
    response.data.questions[0]
);

            setTestSessionId(
                response.data.session_id
            );

            setQuestions(
                response.data.questions
            );

            setCurrentQuestion(0);

            setAnswer("");

            setResult(null);

            setCompleted(false);


        } catch (error) {

            console.log(error);

            alert(
                error.response?.data?.detail ||
                "Failed to generate test."
            );

        } finally {

            setLoading(false);

        }
    };


    // --------------------------------------------------
    // SUBMIT ANSWER
    // --------------------------------------------------

    const handleSubmitAnswer = async () => {

        if (!answer.trim()) {

            alert(
                "Please enter your answer."
            );

            return;
        }


        try {

            setSubmitLoading(true);

            const token = localStorage.getItem("token");

            const question =
                questions[currentQuestion];


            const response = await api.post(
                "/test/submit",
                {
                    test_session_id: testSessionId,
                    question_number: question.question_number,
                    answer: answer
                },
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );


            console.log(
                "TEST SUBMIT RESPONSE:",
                response.data
            );


            setResult(response.data);

            setAnswer("");


            // Check if test is completed
            if (response.data.completed) {

                setCompleted(true);

                return;
            }


            // Move to next question
            if (
                currentQuestion <
                questions.length - 1
            ) {

                setCurrentQuestion(
                    currentQuestion + 1
                );

            }


        } catch (error) {

            console.log(error);

            alert(
                error.response?.data?.detail ||
                "Failed to submit answer."
            );

        } finally {

            setSubmitLoading(false);

        }
    };


    // --------------------------------------------------
    // NEW TEST
    // --------------------------------------------------

    const handleNewTest = () => {

        setQuestions([]);

        setTestSessionId(null);

        setCurrentQuestion(0);

        setAnswer("");

        setResult(null);

        setCompleted(false);

    };


    return (
        <div className="dashboard-layout">

            <Sidebar />

            <main className="dashboard-content">

                <div className="test-page">

                    <h1>
                        Weekly Test
                    </h1>

                    <p>
                        Test your technical knowledge
                        with AI-generated questions.
                    </p>


                    {/* START TEST */}

                    {!testSessionId && !completed && (

                        <button
                            className="test-start-button"
                            onClick={handleStartTest}
                            disabled={loading}
                        >

                            {loading
                                ? "Generating Test..."
                                : "Start Weekly Test"
                            }

                        </button>

                    )}


                    {/* TEST */}

                    {testSessionId &&
                        !completed &&
                        questions.length > 0 && (

                        <div className="test-container">


                            {/* PROGRESS */}

                            <div className="test-progress">

                                <p>
                                    Question{" "}
                                    {currentQuestion + 1}
                                    {" "}of{" "}
                                    {questions.length}
                                </p>

                            </div>


                            {/* QUESTION */}

                            <div className="test-question-card">

                                <h2>
                                    Question{" "}
                                    {currentQuestion + 1}
                                </h2>

                                <p>
                                    {
                                        questions[
                                            currentQuestion
                                        ].question
                                    }
                                </p>

                            </div>


                            {/* ANSWER */}

                            <div className="test-answer-card">

                                <textarea
                                    placeholder="Type your answer here..."
                                    value={answer}
                                    onChange={(e) =>
                                        setAnswer(
                                            e.target.value
                                        )
                                    }
                                    rows="8"
                                />


                                <button
                                    className="test-submit-button"
                                    onClick={
                                        handleSubmitAnswer
                                    }
                                    disabled={
                                        submitLoading
                                    }
                                >

                                    {submitLoading
                                        ? "Evaluating..."
                                        : currentQuestion ===
                                          questions.length - 1
                                            ? "Submit Final Answer"
                                            : "Submit Answer"
                                    }

                                </button>

                            </div>


                            {/* FEEDBACK */}

                            {result && (

                                <div className="test-result">

                                    <h2>
                                        AI Feedback
                                    </h2>


                                    {result.score !==
                                        undefined &&
                                        result.score !==
                                        null && (

                                        <div className="test-score">

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


                    {/* TEST COMPLETED */}

                    {completed && (

                        <div className="test-result">

                            <h2>
                                Test Completed 🎉
                            </h2>

                            <p>
                                You have completed your
                                weekly test.
                            </p>


                            {result?.total_score !==
                                undefined && (

                                <div className="test-score">

                                    <span>
                                        {result.total_score}
                                    </span>

                                    <p>
                                        Total Score
                                    </p>

                                </div>

                            )}


                            {result?.average_score !==
                                undefined && (

                                <div className="test-score">

                                    <span>
                                        {result.average_score}/10
                                    </span>

                                    <p>
                                        Average Score
                                    </p>

                                </div>

                            )}


                            <button
                                className="test-start-button"
                                onClick={handleNewTest}
                            >
                                Start New Test
                            </button>

                        </div>

                    )}

                </div>

            </main>

        </div>
    );
}

export default WeeklyTest;
