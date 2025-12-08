# Research: Core AI Travel Planner System

**Feature**: Core AI Travel Planner System
**Date**: 2025-12-06

## 1. LangGraph Integration
**Decision**: Use `LangGraph` with a stateful graph architecture.
**Rationale**: LangGraph allows for cyclic graphs, which are essential for the "refinement" loop where the AI might need to fetch more data (e.g., weather, POIs) before finalizing the itinerary.
**Structure**:
- **State**: `TripState` containing user inputs, fetched data (weather, flights), and the draft itinerary.
- **Nodes**: `fetch_data`, `generate_draft`, `refine_itinerary`.
- **Edges**: Conditional logic to check if data is sufficient.

## 2. Google OAuth for FastAPI
**Decision**: Use `authlib` with `starlette.middleware.sessions.SessionMiddleware`.
**Rationale**: `authlib` provides a high-level abstraction for OAuth 2.0 and OIDC, integrating seamlessly with FastAPI. It handles the token exchange and user info fetching securely.
**Alternatives**: `fastapi-sso` (less flexible), manual implementation (security risk).

## 3. MongoDB Schema Design
**Decision**: Use embedding for `Itinerary` within `Trip` documents.
**Rationale**: An itinerary is tightly coupled to a trip. Access patterns usually involve fetching the trip and its itinerary together.
**Schema**:
- `User`: `_id` (Google Subject ID), `preferences` (Text).
- `Trip`: `_id`, `user_id`, `destination`, `dates`, `budget`, `itinerary` (Embedded Array of Days).

## 4. External API Resilience
**Decision**: Implement a `Circuit Breaker` pattern with `tenacity` for retries.
**Rationale**: External APIs (OpenWeather, Aviationstack) can be flaky. `tenacity` allows for exponential backoff retries. If all retries fail, the service should return a "partial" result (e.g., trip plan without weather) rather than 500 error.

## 5. Frontend State Management
**Decision**: React Context API + SWR (Stale-While-Revalidate).
**Rationale**: The app state is relatively simple (User Session, Current Trip). Redux is overkill. SWR handles data fetching, caching, and revalidation efficiently for the dashboard.
