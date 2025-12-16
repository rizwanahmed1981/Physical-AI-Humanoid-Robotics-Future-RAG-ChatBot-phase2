---
title: Chapter 5 Section 5 Quiz - Coordinating Perception, Planning, and Control
sidebar_label: Chapter 5 Section 5 Quiz
---

import MCQQuiz from '@site/src/components/MCQQuiz';

<MCQQuiz
  title="Coordinating Perception, Planning, and Control"
  questions={[
    {
      question: "What is the correct order in the end-to-end decision flow?",
      answers: [
        { text: "Perception → Planning → Control → Feedback", correct: true },
        { text: "Control → Perception → Planning → Feedback", correct: false },
        { text: "Feedback → Perception → Planning → Control", correct: false },
        { text: "Planning → Perception → Control → Feedback", correct: false }
      ],
      explanation: "The correct flow is Perception → Processing → Planning → Control → Feedback for continuous operation."
    },
    {
      question: "What is one function of the feedback mechanism?",
      answers: [
        { text: "It makes robots slower", correct: false },
        { text: "It monitors results and adjusts the system", correct: true },
        { text: "It eliminates all planning", correct: false },
        { text: "It reduces robot capabilities", correct: false }
      ],
      explanation: "Feedback mechanisms monitor results and adjust the system based on outcomes for improved performance."
    },
    {
      question: "What is one benefit of the closed-loop system?",
      answers: [
        { text: "It makes robots less adaptable", correct: false },
        { text: "It enables robots to adapt and improve their performance", correct: true },
        { text: "It eliminates the need for planning", correct: false },
        { text: "It makes robots slower", correct: false }
      ],
      explanation: "The closed-loop system enables robots to adapt and improve their performance through continuous feedback."
    },
    {
      question: "What is one way feedback improves robot performance?",
      answers: [
        { text: "It makes robots slower", correct: false },
        { text: "It allows error detection and plan revision", correct: true },
        { text: "It eliminates the need for sensors", correct: false },
        { text: "It reduces robot capabilities", correct: false }
      ],
      explanation: "Feedback allows robots to detect errors and revise plans when circumstances change."
    },
    {
      question: "What does the continuous loop enable in VLA systems?",
      answers: [
        { text: "It makes robots less reliable", correct: false },
        { text: "It enables graceful handling of unexpected situations", correct: true },
        { text: "It eliminates the need for planning", correct: false },
        { text: "It makes robots more expensive", correct: false }
      ],
      explanation: "The continuous loop enables graceful handling of unexpected situations through feedback and correction."
    }
  ]}
/>