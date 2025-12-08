# Data Model: Core AI Travel Planner System

**Feature**: Core AI Travel Planner System
**Date**: 2025-12-06

## Entities

### User
Represents a registered traveler.
- **_id**: String (Google Subject ID) - Primary Key
- **email**: String (Fetched from Google, not stored permanently if privacy requires, but usually needed for UI) -> *Correction per Spec: Store only ID.*
- **preferences**: String (Free-text description, e.g., "I like museums and slow pace")
- **created_at**: DateTime
- **last_login**: DateTime

### Trip
Represents a travel plan.
- **_id**: ObjectId
- **user_id**: String (Foreign Key to User)
- **destination**: String
- **origin**: String
- **start_date**: Date
- **end_date**: Date
- **budget**: Number (Total amount in USD)
- **transportation_preference**: Enum (FLIGHT, DRIVE, BOTH)
- **status**: Enum (DRAFT, PLANNED, COMPLETED)
- **created_at**: DateTime

### Itinerary
Embedded within `Trip` (or separate collection if large, but embedding preferred for this scale).
- **trip_id**: ObjectId (if separate)
- **days**: Array of `ItineraryDay`

### ItineraryDay
- **day_number**: Integer
- **date**: Date
- **morning**: String (Activity description + Time range)
- **afternoon**: String (Activity description + Time range)
- **evening**: String (Activity description + Time range)
- **weather_summary**: String (Cached from OpenWeather)

### CachedData (Optional/Transient)
To avoid re-fetching external APIs constantly.
- **destination**: String
- **weather_data**: JSON
- **flight_options**: JSON (Outbound flights)
- **return_flight_options**: JSON (Return flights)
- **driving_options**: JSON (Driving route estimates)
- **poi_data**: JSON
- **expires_at**: DateTime

## API Contracts (Pydantic Models)

### Requests

**CreateTripRequest**
```json
{
  "origin": "New York, NY",
  "destination": "Tokyo, Japan",
  "start_date": "2025-05-01",
  "end_date": "2025-05-10",
  "budget": 3000,
  "transportation_preference": "FLIGHT"
}
```

**UpdatePreferencesRequest**
```json
{
  "preferences": "I enjoy historical sites and local food. Moderate pace."
}
```

### Responses

**TripSummaryResponse**
```json
{
  "trip_id": "507f1f77bcf86cd799439011",
  "weather_summary": "Mostly sunny, approx 20°C",
  "flight_options": [...],
  "return_flight_options": [...],
  "driving_options": {
     "distance_miles": 300,
     "duration_hours": 5.5,
     "fuel_cost_usd": 45.00,
     "google_maps_link": "https://..."
  },
  "poi_highlights": [...],
  "currency_rate": "1 USD = 145 JPY"
}
```

**ItineraryResponse**
```json
{
  "trip_id": "507f1f77bcf86cd799439011",
  "days": [
    {
      "day": 1,
      "morning": "Visit Senso-ji Temple (09:00-12:00)",
      "afternoon": "Lunch at Nakamise Street (12:00-14:00)",
      "evening": "Dinner in Shinjuku (18:00-20:00)"
    }
  ]
}
```
