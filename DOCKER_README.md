# Docker Setup & Local Development Guide

This guide explains how to run the AI Travel Planner application locally using Docker.

## Prerequisites

*   **Docker**: Ensure Docker Desktop (or Docker Engine) is installed and running.
*   **Git**: To clone the repository.

## Environment Configuration

Before running the application, you must configure the environment variables.

1.  Create a `.env` file in the root directory of the project.
2.  Copy the following template and fill in your actual API keys and secrets:

```env
# AI & LLM Services
OPENAI_API_KEY=your_openai_api_key_here

# Database
MONGODB_URI=your_mongodb_connection_string_here

# Authentication (Google OAuth)
GOOGLE_OAUTH_CLIENT_ID=your_google_client_id_here
GOOGLE_OAUTH_CLIENT_SECRET=your_google_client_secret_here

# External APIs
OPENWEATHER_API_KEY=your_openweather_api_key_here
AVIATIONSTACK_API_KEY=your_aviationstack_api_key_here
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
EXCHANGERATE_API_KEY=your_exchangerate_api_key_here
```

> **Security Warning**: Never commit your `.env` file to version control. It is already added to `.gitignore`.

## Running with Docker Compose

The project includes a `docker-compose.yml` file that orchestrates the Frontend (Next.js) and Backend (FastAPI) services.

### 1. Build and Start Services

Run the following command in the root directory:

```bash
docker-compose up --build
```

This command will:
*   Build the Docker images for the frontend and backend.
*   Start the containers.
*   Stream logs to your terminal.

### 2. Access the Application

Once the containers are running:

*   **Frontend**: Open [http://localhost:3000](http://localhost:3000) in your browser.
*   **Backend API Docs**: Open [http://localhost:8000/docs](http://localhost:8000/docs) to view the Swagger UI.

### 3. Stopping the Application

To stop the containers, press `Ctrl+C` in the terminal, or run:

```bash
docker-compose down
```

## Troubleshooting

*   **Port Conflicts**: Ensure ports `3000` (Frontend) and `8000` (Backend) are not in use by other applications.
*   **Database Connection**: If using a local MongoDB container (optional setup), ensure the `MONGODB_URI` points to `mongodb://mongo:27017/...`. If using Atlas, ensure your IP is whitelisted in MongoDB Atlas.
*   **Missing Keys**: If the app crashes on startup, verify that all required environment variables in `.env` are set.
