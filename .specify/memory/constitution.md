<!--
Sync Impact Report:
Version change: 2.0.0 → 3.0.0
List of modified principles:
- Source Fidelity and Truthfulness → Clean Separation of Frontend and Backend
- Core Educational Mission → Spec-First Development Before Implementation
- Audience Awareness → Modular, Testable, API-First Backend
- Clarity Over Cleverness → Explainable and Reproducible AI Features
- AI-Native Writing Principles → Simplicity and Clarity Over Premature Optimization
- Emotional and Motivational Resonance → AI Behavior Grounded in Textbook Content
Added sections: New principles supporting future extensions (auth, personalization, multilingual content)
Removed sections: Previous educational-focused principles
Templates requiring updates: ⚠ pending - .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
Follow-up TODOs: None
-->

# Physical AI & Humanoid Robotics AI-Native Textbook Platform Constitution

## Core Principles

### Clean Separation of Frontend and Backend
The Docusaurus frontend and FastAPI backend must remain in completely separate directories with no intermingling of concerns. The frontend must interact with the backend exclusively through well-defined API endpoints. No shared code, assets, or configurations between frontend and backend unless explicitly designed as shared libraries. This separation enables independent development, testing, and deployment cycles.

### Spec-First Development Before Implementation
All features must be fully specified in formal API contracts, data models, and behavioral requirements before any implementation begins. Specifications must include: API schemas, expected inputs/outputs, error handling, performance requirements, and integration points. Implementation teams must validate their work against these specifications before merging. This ensures predictable development and reduces rework.

### Modular, Testable, API-First Backend
The FastAPI backend must be architected as independent, loosely-coupled modules that can be tested in isolation. Each module must expose well-documented RESTful APIs with comprehensive OpenAPI schemas. Backend services must follow clean architecture principles with clear separation between controllers, services, and data access layers. All functionality must be thoroughly unit-tested and integration-tested.

### Explainable and Reproducible AI Features
All AI behaviors in the RAG system must be transparent, traceable, and reproducible. The system must provide clear attribution showing which textbook content informed each AI response. AI decision-making processes must be logged and auditable. Results must be deterministic for identical inputs, with randomness explicitly controlled through seed values where appropriate. Users must understand how and why the AI reached conclusions.

### Simplicity and Clarity Over Premature Optimization
Backend implementations must prioritize clean, readable, and maintainable code over performance optimizations unless profiling indicates bottlenecks. Features should be implemented with the simplest viable approach that meets requirements. Complexity should only be introduced when justified by measurable performance needs or functional requirements. Code must be self-documenting through clear naming and structure.

### AI Behavior Grounded in Textbook Content
All AI responses must be strictly grounded in the provided textbook content and related course materials. The RAG system must not generate hallucinated facts, fabricated examples, or speculative information not present in the source materials. AI responses must include citations or references to specific textbook sections when providing answers. The system must explicitly indicate when requested information is not available in the knowledge base.

### Support for Future Extensions
The backend architecture must accommodate planned extensions: user authentication systems, personalized learning experiences, and multilingual content delivery. APIs must be designed with extensibility in mind, allowing new features to be added without breaking existing functionality. Authentication and authorization must be planned from the start, even if initially disabled. Internationalization support must be built in from the foundation.

## Governance
This constitution overrides all other architectural, development, or operational preferences and must be followed by all contributors, AI agents, and automated systems involved in this project. All PRs and code reviews must verify compliance with these principles. Amendments require documentation, approval, and migration planning. The backend and frontend directories must remain completely independent with clearly defined API contracts governing their interaction.

**Version**: 3.0.0 | **Ratified**: 2025-06-13 | **Last Amended**: 2025-12-19