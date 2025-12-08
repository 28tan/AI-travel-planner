# Quickstart: Core AI Travel Planner

**Feature**: Core AI Travel Planner System
**Branch**: `001-core-trip-planner`

## Prerequisites
- Docker & Docker Compose
- Git
- Valid `.env` file (see `DOCKER_README.md`)

## Running Locally

1. **Clone & Switch Branch**
   ```bash
   git checkout 001-core-trip-planner
   ```

2. **Configure Environment**
   Ensure your `.env` file is populated with:
   - `OPENAI_API_KEY`
   - `MONGODB_URI`
   - `GOOGLE_OAUTH_CLIENT_ID` / `SECRET`
   - `OPENWEATHER_API_KEY`
   - `AVIATIONSTACK_API_KEY`
   - `GOOGLE_MAPS_API_KEY`

3. **Start Services**
   ```bash
   docker-compose up --build
   ```

4. **Access Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/docs

## Testing

### Backend Tests
```bash
docker-compose exec backend pytest
```

### Frontend Tests
```bash
docker-compose exec frontend npm test
```
