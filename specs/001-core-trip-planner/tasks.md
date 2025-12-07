# Tasks: Core AI Travel Planner System

**Feature Branch**: `001-core-trip-planner`
**Spec**: [spec.md](./spec.md)
**Plan**: [plan.md](./plan.md)

## Summary

Total Tasks: 41
- Setup & Foundational: 11
- US1 (Auth): 5
- US2 (Plan Trip): 12
- US3 (AI Itinerary): 4
- US4 (Manage Trips): 2
- US5 (Preferences): 2
- Polish & QA: 5

## Phase 1: Setup (Project Initialization)

**Goal**: Initialize the monorepo structure, Docker environment, and basic application shells.

- [x] T001 Create project directory structure (backend/app, frontend/src) per plan.md
- [x] T002 Create `docker-compose.yml` with Backend, Frontend, and MongoDB services
- [x] T003 [P] Initialize Backend: Create `backend/requirements.txt` and `backend/Dockerfile`
- [x] T004 [P] Initialize Frontend: Create `frontend/package.json` and `frontend/Dockerfile`
- [x] T005 [P] Create Backend entry point `backend/app/main.py` with health check endpoint
- [x] T006 [P] Create Frontend landing page `frontend/src/app/page.tsx`

## Phase 2: Foundational (Blocking Prerequisites)

**Goal**: Establish database connections, configuration management, and shared data structures.

- [x] T007 Implement Configuration management in `backend/app/core/config.py` (Env vars)
- [x] T008 Implement MongoDB connection client in `backend/app/core/database.py`
- [x] T009 Define shared Pydantic models (User, Trip, Itinerary) in `backend/app/models/`
- [x] T009a Implement Structured Logging in `backend/app/core/logging.py` (Constitution VI)
- [x] T009b Setup Pytest configuration and fixtures in `backend/tests/conftest.py` (Constitution IV)

## Phase 3: User Story 1 - User Authentication (P1)

**Goal**: Enable users to log in via Google OAuth and maintain a session.
**Independent Test**: User can click "Sign In", authenticate with Google, and see their session state persist.

- [x] T010 [US1] Implement `UserRepository` for user persistence in `backend/app/repositories/user_repository.py`
- [x] T011 [US1] Implement `AuthService` using authlib in `backend/app/services/auth_service.py`
- [x] T012 [US1] Create Auth API endpoints (`/auth/login`, `/auth/callback`) in `backend/app/controllers/auth_controller.py`
- [x] T013 [P] [US1] Implement Frontend Auth Context/Provider in `frontend/src/context/AuthContext.tsx`
- [x] T014 [P] [US1] Create Login page and protected route wrapper in `frontend/src/app/login/page.tsx`

## Phase 4: User Story 2 - Plan a Trip (P1)

**Goal**: Collect trip details and aggregate external data. Covers UC3 (Plan), UC4 (Weather), UC5 (Transport), UC6 (POIs), UC7 (Summary).
**Independent Test**: User can submit trip form and view a summary with real/mocked external data.

- [x] T015 [P] [US2] Implement `WeatherService` (OpenWeather) in `backend/app/services/weather_service.py`
- [x] T016 [P] [US2] Implement `FlightService` (Aviationstack) in `backend/app/services/flight_service.py`
- [x] T017 [P] [US2] Implement `PlacesService` (Google Maps/Places) in `backend/app/services/places_service.py`
- [x] T018 [US2] Implement `TripRepository` in `backend/app/repositories/trip_repository.py`
- [x] T019 [US2] Implement `TripService` to aggregate data from external services in `backend/app/services/trip_service.py`
- [x] T020 [US2] Create Trip API endpoints (`POST /trips`) in `backend/app/controllers/trip_controller.py`
- [x] T021 [P] [US2] Create Trip Input Form component in `frontend/src/components/TripForm.tsx`
- [x] T022 [P] [US2] Create Weather Forecast component (UC4) in `frontend/src/components/WeatherView.tsx`
- [x] T023 [P] [US2] Create Transportation Options component (UC5) in `frontend/src/components/TransportView.tsx`
- [x] T024 [P] [US2] Create POI List/Map component (UC6) in `frontend/src/components/POIView.tsx`
- [x] T025 [P] [US2] Create Trip Summary container (UC7) in `frontend/src/components/TripSummary.tsx`
- [x] T026 [US2] Integrate Form and Summary on Plan Page `frontend/src/app/plan/page.tsx`

## Phase 5: User Story 3 - Generate AI Itinerary (P1)

**Goal**: Generate a day-by-day itinerary using LangGraph and OpenAI. Covers UC8.
**Independent Test**: User can click "Generate" on a trip summary and receive a structured itinerary.

- [x] T027 [US3] Implement `OpenAIService` for LLM interaction `backend/app/services/openai_service.py`
- [x] T028 [US3] Create Itinerary Generation Endpoint `backend/app/controllers/itinerary_controller.py`
- [x] T029 [US3] Create Itinerary generation endpoint (`POST /trips/{id}/itinerary`) in `backend/app/controllers/itinerary_controller.py`
- [x] T030 [P] [US3] Create Itinerary View component in `frontend/src/components/ItineraryView.tsx`

## Phase 6: User Story 4 - Manage Saved Trips (P2)

**Goal**: View and delete previously saved trips. Covers UC9.
**Independent Test**: User can view a list of trips and delete one.

- [x] T031 [US4] Create User Trips endpoint (`GET /trips`) in `backend/app/controllers/trip_controller.py`
- [x] T032 [P] [US4] Create Trips List component in `frontend/src/components/TripList.tsx`

## Phase 7: User Story 5 - Manage Preferences (P2)

**Goal**: Save and apply user travel preferences. Covers UC2.
**Independent Test**: User can update profile preferences and see them applied to new trip forms.

- [x] T033 [US5] Create User Preferences endpoint (`PUT /users/me/preferences`) in `backend/app/controllers/user_controller.py`
- [x] T034 [P] [US5] Create Profile page with Preferences form in `frontend/src/app/profile/page.tsx`

## Phase 8: Polish & Cross-Cutting Concerns

**Goal**: Ensure reliability, user experience quality, and compliance with Constitution.

- [x] T035 Implement Circuit Breaker pattern for external services in `backend/app/core/resilience.py`
- [x] T036 Polish UI (Loading states, Error toasts, Responsive layout) across all pages
- [x] T037 Write Unit Tests for Backend Services (Auth, Trip, Weather) (Constitution IV)

## Phase 9: Refinements & Workflow Updates

**Goal**: Improve UX with Draft/Confirm workflows and UI modernization.

- [x] T042 Implement "Draft" status for Trips and "Confirm" workflow (Plan Page)
- [x] T043 Implement "Preview" mode for Itinerary Generation (Trip Details)
- [x] T044 Update Home Page and Navbar UI for better engagement and auth state reflection
- [x] T038 Write Integration Tests for API Endpoints (Constitution IV)
- [x] T039 Perform Basic Load Test (Locust/k6) to verify SC-001/SC-002

## Phase 9: Enhancements & Refinements (Post-MVP)

**Goal**: Improve user experience and system robustness based on feedback.

- [x] T040 Enhance Transport Options: Add Driving Routes and Return Flights support
- [x] T041 Improve Flight Search Robustness: Add IATA country mappings and fallback logic
- [x] T042 Redesign Home Page: Modern UI with Hero section and Feature grid
- [x] T043 Update Navigation: Unified dynamic navbar for logged-in/out states
- [x] T044 Remove Local MongoDB: Migrate fully to MongoDB Atlas for cloud storage
- [x] T045 Implement Real Currency Service: Integrate `open.er-api.com` for live rates
- [x] T046 Restore Flight Mock Fallback: Handle API rate limits (429) gracefully

## Dependencies

1. **Setup & Foundational** must be completed first.
2. **US1 (Auth)** is required for all other stories (User ID needed for Trips).
3. **US2 (Plan)** is required for US3 (Itinerary needs Trip data).
4. **US3 (Itinerary)** depends on US2.
5. **US4 (Manage)** depends on US2 (need trips to manage).
6. **US5 (Preferences)** depends on US1 (need user to have preferences).

## Parallel Execution Opportunities

- **Frontend vs Backend**: Within each User Story, frontend components (marked [P]) can be built in parallel with backend services once the API contract (openapi.yaml) is agreed upon.
- **External Services**: Weather, Flight, and Places services (T015, T016, T017) can be implemented in parallel.
- **US4 & US5**: Can be executed in parallel after US1 and US2 are complete.

## Implementation Strategy

1. **MVP Scope**: Focus on US1, US2, and US3 first. This delivers the core "AI Travel Planner" value.
2. **Mocking**: For US2, initially mock the external API responses to avoid rate limits/costs during development.
3. **Incremental Delivery**: Deploy the Setup/Foundational layer first, then feature by feature.
