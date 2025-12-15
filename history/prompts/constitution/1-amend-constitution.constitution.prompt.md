---
id: 1
title: Amend Constitution
stage: constitution
date: '2025-12-15'
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: ecomw
command: /sp.constitution
labels:
  - constitution
  - governance
  - physical-ai
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests: []
---

# Constitution Amendment Record

## Original Prompt

```
/sp.constitution

This project is an AI-native technical textbook titled:
"Physical-AI-Humanoid-Robotics-Future"

The constitution defines the non-negotiable principles that govern all content creation, assessments, agent usage, and implementation decisions in this repository.

### 1. Source Fidelity and Truthfulness
- All factual claims must be grounded strictly in the provided course documents and officially documented technologies.
- Never invent hardware capabilities, software features, benchmarks, timelines, or outcomes.
- If information is missing or unclear in the source, explicitly state uncertainty instead of guessing.
- Preserve the original intent, scope, and promises of the Physical-AI-Humanoid-Robotics-Future course 100%.

### 2. Core Educational Mission
- The primary goal is to bridge digital AI systems with embodied intelligence in the physical world.
- Every chapter must help the reader understand how intelligence moves from models to machines.
- Content must always connect theory to real-world robotic systems, simulations, or deployment contexts.
- Avoid purely abstract discussions unless they directly support physical execution.

### 3. Audience Awareness
- The target audience is AI learners who understand programming and basic AI concepts but are new to robotics.
- Assume familiarity with Python and AI fundamentals.
- Reduce intimidation and build confidence.
- Teach as a calm, experienced mentor guiding a motivated junior engineer.

### 4. Clarity Over Cleverness
- Prefer simple language over complex jargon.
- Explain "why" before "how" in every major section.
- Introduce mental models before tools, APIs, or commands.
- Avoid hype, marketing language, or exaggerated claims.

### 5. AI-Native Writing Principles
- Structure content for both human readers and AI agents.
- Use clear headings, focused sections, and isolated concepts to support Retrieval-Augmented Generation.
- Each section should answer one core question.
- Avoid mixing multiple major concepts in a single section.

### 6. Emotional and Motivational Resonance
- Reinforce why Physical AI matters for the future of work and human-robot collaboration.
- Inspire curiosity, responsibility, and long-term skill building.
- Emphasize systems thinking and real-world impact over novelty.

### 7. Consistency Across Chapters
- Use consistent terminology throughout the book.
- Build progressively on previously introduced concepts.
- Keep hardware, software stacks, and architectural assumptions aligned.

### 8. Tool and Platform Discipline
- ROS 2, Gazebo, Unity, NVIDIA Isaac, and Vision-Language-Action must be presented as parts of one integrated humanoid system.
- Avoid isolated tool tutorials.
- Always explain how each tool maps to the robot's nervous system, brain, or body.

### 9. Structured Assessment as a Core Feature
- Learning assessment is mandatory, not optional.
- Every subsection must end with a short formative quiz of exactly 5 multiple-choice questions.
- Every main section must end with a comprehensive quiz of exactly 10 multiple-choice questions.

### 10. Quiz Design Standards
- All quiz questions must be directly answerable from the immediately preceding content.
- Questions must test understanding, not memorization.
- Avoid trick questions or ambiguous wording.
- Each question must have exactly one correct answer.

### 11. Interactive Answer Reveal Requirement
- Quiz answers must not be immediately visible.
- Each quiz must include a clearly labeled "Reveal Answers" button.
- Answer reveals should match modern learning platforms such as Coursera, Udemy, and Cisco.
- When answers are revealed, include brief explanations explaining why the answer is correct.

### 12. Pedagogical Flow Control
- Quizzes must reinforce key ideas before the learner moves forward.
- Do not introduce new concepts inside quizzes.
- Use quizzes to surface misunderstandings early.

### 13. Agent-Oriented Content Development
- AI agents must be used intentionally and explicitly, not implicitly.
- Each agent must have a clearly defined role such as:
  - Content Author
  - Technical Reviewer
  - Quiz Generator
  - Pedagogy Reviewer
  - RAG Optimization Agent
- No agent may operate outside its defined responsibility.

### 14. Reusable Agent Skills
- Repetitive intellectual tasks must be abstracted into reusable agent skills.
- Examples include:
  - Generating MCQs from a section
  - Validating factual consistency against source material
  - Converting content into RAG-friendly chunks
  - Creating learner-friendly explanations
- Skills must be reusable across chapters and not hardcoded to a single section.

### 15. MCP Server Usage Guidelines
- MCP servers must be used where external knowledge, tools, or structured validation is required.
- MCP usage must be:
  - Explicit
  - Justified
  - Limited to well-defined tasks
- MCP servers must never introduce new facts that are not present in the source documents.
- MCP servers should support verification, retrieval, formatting, or orchestration, not creative invention.

### 16. Agent Governance and Safety
- Agents must follow this constitution at all times.
- If an agent encounters ambiguity, it must request clarification instead of making assumptions.
- Agents must prefer correctness over completeness.
- Any output that violates source fidelity must be rejected or revised.

### 17. No Scope Creep
- Do not expand beyond the defined course modules and learning outcomes.
- Advanced topics or future directions must be explicitly labeled as optional or exploratory.
- The book must remain teachable within the defined course timeline.

### 18. Review and Self-Audit Requirement
- Before finalizing any chapter, quiz, or agent-generated output, review it against this constitution.
- Explicitly check for invented facts, unclear assumptions, or misalignment with learning outcomes.
- When in doubt, prioritize correctness, clarity, and learner comprehension over completeness.

This constitution overrides all other stylistic, generative, or tool-specific preferences and must be followed by all AI agents, skills, MCP servers, and contributors involved in this project.
```

## Response Summary

Updated the project constitution to reflect the new book name "Physical-AI-Humanoid-Robotics-Future". The constitution file has been updated with the new name in the title and throughout the document where references to the book name appear.

## Outcome

The constitution file at `.specify/memory/constitution.md` has been successfully updated with the new book name "Physical-AI-Humanoid-Robotics-Future". The corresponding PHR file has also been updated to reflect this change.

## Files Modified

- `.specify/memory/constitution.md` - Updated with new book name
- `history/prompts/constitution/1-amend-constitution.constitution.prompt.md` - Updated with new book name in prompt
## Response Summary

Updated the project constitution to reflect the specific requirements for the "Physical AI & Humanoid Robotics" textbook project. The new constitution includes 18 detailed principles covering source fidelity, educational mission, audience awareness, clarity, AI-native writing, emotional resonance, consistency, tool discipline, assessment standards, quiz design, pedagogical flow, agent governance, and more. The version was bumped from 1.0.0 to 2.0.0 to reflect the significant changes in principles and governance.

## Outcome

The constitution file at `.specify/memory/constitution.md` has been successfully updated with the new principles for the Physical AI & Humanoid Robotics textbook project. The file now properly reflects the specific educational and technical requirements of the project, with clear guidelines for content creation, assessment, and agent usage.

## Files Modified

- `.specify/memory/constitution.md` - Updated with 18 specific principles for the Physical AI & Humanoid Robotics project