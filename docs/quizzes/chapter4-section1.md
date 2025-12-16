---
title: Chapter 4 Section 1 Quiz - The Brain of a Physical AI System
sidebar_label: Chapter 4 Section 1 Quiz
---

import MCQQuiz from '@site/src/components/MCQQuiz';

# Chapter 4 Section 1 Quiz: The Brain of a Physical AI System

<MCQQuiz
  title="The Brain of a Physical AI System"
  questions={[
    {
      question: "What is the main difference between control logic and intelligence in robotics?",
      answers: [
        { text: "Control logic is for sensors, intelligence is for actuators", correct: false },
        { text: "Control logic is low-level and rule-based, intelligence is high-level and decision-making", correct: true },
        { text: "Control logic is for hardware, intelligence is for software", correct: false },
        { text: "Control logic is faster, intelligence is slower", correct: false }
      ],
      explanation: "Control logic is low-level and rule-based, executing direct commands, while intelligence is high-level and handles decision-making."
    },
    {
      question: "What is one function of the AI brain?",
      answers: [
        { text: "Only physical movement", correct: false },
        { text: "Coordination of perception, planning, and control", correct: true },
        { text: "Only sensor data collection", correct: false },
        { text: "Only actuator control", correct: false }
      ],
      explanation: "The AI brain coordinates perception, planning, and control to create intelligent robot behavior."
    },
    {
      question: "Where do learning and decision-making primarily occur in a robot?",
      answers: [
        { text: "In the actuators", correct: false },
        { text: "In the sensors", correct: false },
        { text: "In the AI brain", correct: true },
        { text: "In the power supply", correct: false }
      ],
      explanation: "Learning and decision-making primarily occur in the AI brain, which processes information and makes decisions."
    },
    {
      question: "What is one component of the AI brain?",
      answers: [
        { text: "Only physical actuators", correct: false },
        { text: "Machine Learning Models", correct: true },
        { text: "Only mechanical parts", correct: false },
        { text: "Only electrical circuits", correct: false }
      ],
      explanation: "The AI brain includes machine learning models, planning algorithms, and behavior controllers."
    },
    {
      question: "What does sensor fusion do in the AI brain?",
      answers: [
        { text: "It eliminates the need for sensors", correct: false },
        { text: "It combines data from multiple sensors", correct: true },
        { text: "It makes sensors more expensive", correct: false },
        { text: "It reduces sensor capabilities", correct: false }
      ],
      explanation: "Sensor fusion combines data from multiple sensors to create a more complete picture of the environment."
    }
  ]}
/>