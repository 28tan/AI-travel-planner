<!--
SYNC IMPACT REPORT
Version change: 1.1.0 → 1.2.0
List of modified principles:
- Added: VIII. Containerization & Local Development (Mandating Docker/Docker Compose for local dev)
Added sections: None
Removed sections: None
Templates requiring updates:
- .specify/templates/plan-template.md (✅ compatible)
- .specify/templates/spec-template.md (✅ compatible)
- .specify/templates/tasks-template.md (✅ compatible)
Follow-up TODOs:
- Create DOCKER_README.md (✅ created)
-->

# AI Travel Planner Constitution

## Core Principles

### I. Security & Secret Management
**Rationale**: The application handles sensitive user authentication (Google OAuth) and utilizes multiple paid external API keys. Leaking these credentials would result in financial loss and security breaches.
**Rule**: All API keys, secrets, and database credentials MUST be stored in environment variables and accessed via configuration services. They MUST NEVER be committed to the source code. OAuth flows MUST follow standard security protocols. All data traffic MUST be encrypted using HTTPS and TLS.

### II. Service-Repository Architecture
**Rationale**: To maintain a clean separation of concerns as defined in the project's maintainability requirements.
**Rule**: The system MUST follow a strict separation of concerns:
1.  **Controllers**: Handle HTTP request/response translation.
2.  **Services**: Contain business logic (e.g., `AuthService`, `TripService`).
3.  **AI Agents**: Encapsulate AI reasoning (e.g., `AITravelAgent`).
4.  **Repositories**: Handle data access (e.g., `UserRepository`, `TripRepository`).

### III. AI-First Design
**Rationale**: The core value proposition is the AI-generated travel itinerary. The AI logic is central to the user experience.
**Rule**: AI interactions (via LangGraph/OpenAI) MUST be encapsulated in dedicated services. Prompts and AI workflows should be treated as first-class citizens, versioned, and designed for determinism where possible.

### IV. Comprehensive Testing
**Rationale**: To ensure reliability across the complex interplay of AI, external APIs, and user data.
**Rule**: Both Frontend and Backend MUST have respective test cases. Unit tests are required for all services. Integration tests are required for critical paths, using mocks for external APIs to prevent excessive costs.

### V. External Service Resilience
**Rationale**: The application relies on multiple third-party APIs (OpenWeather, Aviationstack, Google Maps, Exchange Rate).
**Rule**: Interactions with external APIs MUST be designed with resilience. This includes implementing error handling, retries (default: 3 attempts), and graceful degradation (e.g., showing partial results) when services are unavailable.

### VI. Observability
**Rationale**: To facilitate troubleshooting and testing in a distributed system environment.
**Rule**: Basic logging MUST be implemented in both Backend and Frontend components to track system behavior, API failures, and AI agent performance.

### VII. Performance & Scalability
**Rationale**: The system must support 100+ active users and auto-scale on Google Cloud Run.
**Rule**: The backend MUST be stateless to support auto-scaling. Trip planning requests MUST complete within 60 seconds (target 30-60s). Long-running operations MUST provide progress feedback (e.g., progress bar) to the user.

### VIII. Containerization & Local Development
**Rationale**: To ensure consistent development environments across different machines and simplify deployment to container-based platforms (like Cloud Run).
**Rule**: The application MUST be fully containerized using Docker. A `docker-compose.yml` file MUST be provided to spin up the entire stack (Frontend, Backend) locally with a single command.

## Governance

### Amendment Process
This constitution is the supreme governance document for the AI Travel Planner project. Amendments may be proposed by any contributor but require a Pull Request with a clear rationale.
- **Major Version Bump (X.0.0)**: Required for removing or fundamentally changing a Core Principle.
- **Minor Version Bump (0.X.0)**: Required for adding new principles or significant sections.
- **Patch Version Bump (0.0.X)**: For clarifications, typos, or non-semantic updates.

### Compliance
All code contributions, architectural decisions, and feature implementations MUST comply with these principles. Code reviews MUST explicitly verify alignment with the Constitution.

**Version**: 1.2.0 | **Ratified**: 2025-12-06 | **Last Amended**: 2025-12-06
