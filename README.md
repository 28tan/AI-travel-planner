# AI Travel Planner

An AI-powered travel planning application that generates personalized itineraries, provides real-time weather and flight information, and allows users to manage their trips.

## Features

*   **AI Itinerary Generation**: Uses LangGraph and OpenAI to create detailed day-by-day travel plans.
*   **Real-Time Data**: Integrates with OpenWeatherMap, Aviationstack, and Google Places for up-to-date information.
*   **User Authentication**: Secure Google OAuth login.
*   **Trip Management**: Save, view, and delete trips.
*   **Currency Conversion**: Real-time exchange rates.
*   **Responsive UI**: Modern interface built with Next.js and Tailwind CSS.

## Tech Stack

*   **Backend**: Python (FastAPI), LangGraph, MongoDB (Motor)
*   **Frontend**: TypeScript, Next.js, React, Tailwind CSS
*   **Infrastructure**: Docker, Docker Compose

## Prerequisites

*   [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
*   A MongoDB Atlas account and connection string.
*   API Keys for:
    *   OpenAI
    *   OpenWeatherMap
    *   Aviationstack
    *   Google Maps Platform (Places API)
    *   Google OAuth (Client ID & Secret)

## Setup Instructions

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd AI-travel-planner
    ```

2.  **Configure Environment Variables:**
    Create a `.env` file in the root directory (or copy `.env.example` if available) and fill in your credentials:

    ```env
    # Backend
    PROJECT_NAME="AI Travel Planner"
    MONGODB_URL="mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority"
    DB_NAME="travel_planner"
    
    # Auth
    SECRET_KEY="your_secret_key"
    GOOGLE_CLIENT_ID="your_google_client_id"
    GOOGLE_CLIENT_SECRET="your_google_client_secret"
    
    # AI & APIs
    OPENAI_API_KEY="your_openai_key"
    OPENWEATHER_API_KEY="your_openweather_key"
    AVIATIONSTACK_API_KEY="your_aviationstack_key"
    GOOGLE_MAPS_API_KEY="your_google_maps_key"
    
    # Frontend
    NEXT_PUBLIC_API_URL="http://localhost:8000"
    ```

3.  **Run with Docker Compose:**
    ```bash
    docker-compose up -d --build
    ```

4.  **Access the Application:**
    *   **Frontend**: [http://localhost:3000](http://localhost:3000)
    *   **Backend API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

## Development

*   **Backend Logs**: `docker-compose logs -f backend`
*   **Frontend Logs**: `docker-compose logs -f frontend`
*   **Rebuild a specific service**: `docker-compose up -d --build <service_name>`

## Testing

To run backend tests:
```bash
docker-compose exec backend pytest
```
