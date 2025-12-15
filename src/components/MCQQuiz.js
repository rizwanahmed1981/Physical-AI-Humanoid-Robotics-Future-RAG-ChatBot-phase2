import React, { useState } from 'react';
import clsx from 'clsx';
import styles from '../css/quiz.module.css';

const MCQQuiz = ({ questions, title = "Quiz" }) => {
  const [userAnswers, setUserAnswers] = useState(
    Array(questions.length).fill(null)
  );
  const [showResults, setShowResults] = useState(false);
  const [revealedAnswers, setRevealedAnswers] = useState(false);

  const handleAnswerChange = (questionIndex, answerIndex) => {
    if (!showResults) {
      const newAnswers = [...userAnswers];
      newAnswers[questionIndex] = answerIndex;
      setUserAnswers(newAnswers);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setShowResults(true);
  };

  const handleRevealAnswers = () => {
    setRevealedAnswers(true);
  };

  const resetQuiz = () => {
    setUserAnswers(Array(questions.length).fill(null));
    setShowResults(false);
    setRevealedAnswers(false);
  };

  const calculateScore = () => {
    let correct = 0;
    questions.forEach((question, index) => {
      if (
        userAnswers[index] !== null &&
        question.answers[userAnswers[index]].correct
      ) {
        correct++;
      }
    });
    return { correct, total: questions.length };
  };

  const score = showResults ? calculateScore() : { correct: 0, total: questions.length };

  return (
    <div className={styles.quizContainer}>
      <h3 className={styles.quizTitle}>{title}</h3>

      <form onSubmit={handleSubmit} className={styles.quizForm}>
        {questions.map((question, qIndex) => (
          <div key={qIndex} className={styles.questionContainer}>
            <div className={styles.questionText}>
              <strong>{qIndex + 1}. {question.question}</strong>
            </div>

            <div className={styles.answersContainer}>
              {question.answers.map((answer, aIndex) => (
                <div key={aIndex} className={styles.answerOption}>
                  <label className={styles.answerLabel}>
                    <input
                      type="radio"
                      name={`question-${qIndex}`}
                      checked={userAnswers[qIndex] === aIndex}
                      onChange={() => handleAnswerChange(qIndex, aIndex)}
                      disabled={showResults}
                      className={styles.answerInput}
                    />
                    <span className={styles.answerText}>
                      {answer.text}
                    </span>
                  </label>

                  {showResults && answer.correct && userAnswers[qIndex] === aIndex && (
                    <div className={styles.correctIndicator}>✓ Correct!</div>
                  )}
                  {showResults && !answer.correct && userAnswers[qIndex] === aIndex && (
                    <div className={styles.incorrectIndicator}>✗ Incorrect</div>
                  )}
                  {showResults && answer.correct && (
                    <div className={styles.correctAnswer}>✓</div>
                  )}
                </div>
              ))}
            </div>

            {showResults && revealedAnswers && question.explanation && (
              <div className={styles.explanation}>
                <strong>Explanation:</strong> {question.explanation}
              </div>
            )}
          </div>
        ))}

        {!showResults ? (
          <button type="submit" className={styles.submitButton}>
            Submit Answers
          </button>
        ) : (
          <div className={styles.resultsSection}>
            <div className={styles.score}>
              Score: {score.correct} / {score.total}
            </div>
            {!revealedAnswers ? (
              <button
                type="button"
                onClick={handleRevealAnswers}
                className={styles.revealButton}
              >
                Reveal Answers
              </button>
            ) : (
              <button
                type="button"
                onClick={resetQuiz}
                className={styles.resetButton}
              >
                Reset Quiz
              </button>
            )}
          </div>
        )}
      </form>
    </div>
  );
};

export default MCQQuiz;