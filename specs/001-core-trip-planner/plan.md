# Implementation Plan: Core AI Travel Planner System

**Branch**: `001-core-trip-planner` | **Date**: 2025-12-06 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-core-trip-planner/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement the core AI Travel Planner system, including user authentication via Google OAuth, trip planning with external API aggregation (Weather, Flights, POIs), and AI-driven itinerary generation using LangGraph. The system will be containerized with Docker and follow a strict Service-Repository architecture.

**Key Enhancements (Post-MVP):**
- **Multi-Modal Transport**: Support for driving route estimates (distance, fuel cost) alongside flight search.
- **Round-Trip Flights**: Separate handling for outbound and return flight options.
- **Robust Search**: Enhanced IATA mapping for countries and major cities, with fallback logic for flight data.
- **Real-Time Currency**: Integration with `open.er-api.com` for live exchange rates.
- **Modern UI**: Redesigned landing page and dynamic navigation.

## Technical Context

**Language/Version**: Python 3.10+ (Backend), Node.js 18+ (Frontend)
**Primary Dependencies**: FastAPI, LangGraph, Motor (MongoDB), React, Next.js, Tailwind CSS
**Storage**: MongoDB Atlas (Cloud)
**Testing**: Pytest (Backend), Jest/React Testing Library (Frontend)
**Target Platform**: Google Cloud Run (Backend), Vercel (Frontend) - Local: Docker Compose
**Project Type**: Web application (Frontend + Backend)
**Performance Goals**: Trip plan generation < 60s, Support 100+ concurrent users
**Constraints**: HTTPS/TLS required, Stateless backend, Environment variables for secrets
**Scale/Scope**: Core MVP features (Auth, Plan, Itinerary, Manage Trips)
**Resilience Strategy**: Real APIs used by default. Circuit breakers and Mock Data fallbacks implemented for rate-limited services (e.g., Aviationstack).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **I. Security**: Secrets in env vars, HTTPS required.
- [x] **II. Architecture**: Service-Repository pattern enforced.
- [x] **III. AI-First**: Dedicated `AITravelAgent` service.
- [x] **IV. Testing**: Unit/Integration tests required.
- [x] **V. Resilience**: Retries for external APIs.
- [x] **VI. Observability**: Logging required.
- [x] **VII. Performance**: <60s response, stateless backend.
- [x] **VIII. Docker**: `docker-compose.yml` required.

## Project Structure

### Documentation (this feature)

```text
specs/001-core-trip-planner/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── controllers/     # API Routes
│   ├── services/        # Business Logic (Auth, Trip, Weather, etc.)
│   ├── repositories/    # Data Access (User, Trip)
│   ├── models/          # Pydantic Models & DB Schemas
│   ├── ai/              # LangGraph Agent & Prompts
│   └── core/            # Config, Logging, Exceptions
├── tests/
│   ├── unit/
│   └── integration/
├── Dockerfile
└── requirements.txt

frontend/
├── src/
│   ├── app/             # Next.js Pages
│   ├── components/      # Reusable UI Components
│   ├── services/        # API Client
│   └── types/           # TypeScript Interfaces
├── tests/
├── Dockerfile
└── package.json

docker-compose.yml
```

**Structure Decision**: Standard Monorepo with separate `backend` (FastAPI) and `frontend` (Next.js) directories, orchestrated via Docker Compose.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |

## Workflow Refinements

**Trip Creation (Draft Mode)**:
- Trips are initially created with `status="draft"`.
- Draft trips are not visible on the main dashboard.
- Users must explicitly "Save" (Confirm) a trip to change its status to `planned` and make it persistent.
- Users can "Discard" a draft trip, which deletes it permanently.

**Itinerary Generation (Preview Mode)**:
- Itineraries generated via AI are initially returned in "Preview" mode (not saved to DB).
- The frontend displays the generated itinerary with "Save" and "Discard" options.
- "Save" persists the itinerary to the Trip document.
- "Discard" clears the preview without modifying the database.
