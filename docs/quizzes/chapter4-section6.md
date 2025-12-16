---
title: Chapter 4 Section 6 Quiz - From Perception to Action
sidebar_label: Chapter 4 Section 6 Quiz
---

import MCQQuiz from '@site/src/components/MCQQuiz';

# Chapter 4 Section 6 Quiz: From Perception to Action

<MCQQuiz
  title="From Perception to Action"
  questions={[
    {
      question: "What is the first stage in the end-to-end AI brain flow?",
      answers: [
        { text: "Control", correct: false },
        { text: "Planning", correct: false },
        { text: "Perception", correct: true },
        { text: "Feedback", correct: false }
      ],
      explanation: "The first stage is perception, where sensors gather environmental data."
    },
    {
      question: "What is the correct order of the AI brain flow?",
      answers: [
        { text: "Perception → Planning → Control → Feedback", correct: true },
        { text: "Control → Perception → Planning → Feedback", correct: false },
        { text: "Feedback → Perception → Planning → Control", correct: false },
        { text: "Planning → Perception → Control → Feedback", correct: false }
      ],
      explanation: "The correct flow is: Perception → Processing → Planning → Control → Feedback."
    },
    {
      question: "What is one function of the feedback stage?",
      answers: [
        { text: "It eliminates all processing", correct: false },
        { text: "It monitors results and adjusts", correct: true },
        { text: "It only collects data", correct: false },
        { text: "It makes all decisions", correct: false }
      ],
      explanation: "The feedback stage monitors results and adjusts the system based on outcomes."
    },
    {
      question: "What does the 'seeing-think-doing' mental model represent?",
      answers: [
        { text: "Only physical actions", correct: false },
        { text: "Perception-thinking-control stages", correct: true },
        { text: "Only sensor data", correct: false },
        { text: "Only actuator control", correct: false }
      ],
      explanation: "The seeing-think-doing model represents the three stages: perception (seeing), planning (thinking), and control (doing)."
    },
    {
      question: "What is one benefit of the end-to-end flow?",
      answers: [
        { text: "It makes robots slower", correct: false },
        { text: "It enables intelligent, adaptive behavior", correct: true },
        { text: "It eliminates all complexity", correct: false },
        { text: "It reduces robot capabilities", correct: false }
      ],
      explanation: "The end-to-end flow enables intelligent, adaptive behavior by creating a continuous loop of perception, planning, and action."
    }
  ]}
/>