import os
import json
import httpx
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.model = "gpt-3.5-turbo"  # Or gpt-4 if available/preferred

    async def generate_itinerary(self, trip_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates a day-by-day itinerary based on the trip context.
        
        trip_context should include:
        - destination
        - start_date, end_date
        - budget
        - travelers
        - interests (preferences)
        - weather_forecast (summary)
        - flight_info (arrival/departure times)
        """
        if not self.api_key:
            logger.warning("OPENAI_API_KEY not found. Returning mock itinerary.")
            return self._get_mock_itinerary(trip_context)

        prompt = self._construct_prompt(trip_context)
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    self.api_url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "messages": [
                            {"role": "system", "content": "You are an expert travel agent. Generate a detailed day-by-day itinerary in JSON format."},
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.7,
                        "response_format": { "type": "json_object" }
                    }
                )
                
                if response.status_code != 200:
                    logger.error(f"OpenAI API error: {response.text}")
                    return self._get_mock_itinerary(trip_context)
                
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                
                # Clean up markdown code blocks if present
                if content.startswith("```json"):
                    content = content[7:]
                if content.startswith("```"):
                    content = content[3:]
                if content.endswith("```"):
                    content = content[:-3]
                content = content.strip()
                
                try:
                    itinerary_json = json.loads(content)
                    
                    # Ensure critical fields exist
                    if "personal_travel_tip" not in itinerary_json:
                        dest = trip_context.get("destination", "your destination")
                        itinerary_json["personal_travel_tip"] = f"Don't forget to check the local weather forecast for {dest} before heading out each morning!"
                        
                    return itinerary_json
                except json.JSONDecodeError:
                    logger.error("Failed to parse OpenAI response as JSON")
                    return self._get_mock_itinerary(trip_context)

        except Exception as e:
            logger.error(f"Error calling OpenAI service: {str(e)}")
            return self._get_mock_itinerary(trip_context)

    def _construct_prompt(self, context: Dict[str, Any]) -> str:
        destination = context.get("destination", "Unknown")
        start_date = context.get("start_date")
        end_date = context.get("end_date")
        budget = context.get("budget", "Medium")
        weather_summary = context.get("weather_summary", "Weather information unavailable")
        
        # Calculate duration
        duration_str = ""
        try:
            if start_date and end_date:
                start = datetime.strptime(str(start_date), "%Y-%m-%d")
                end = datetime.strptime(str(end_date), "%Y-%m-%d")
                days = (end - start).days + 1
                duration_str = f"The trip is for {days} days."
        except Exception as e:
            logger.warning(f"Could not calculate duration: {e}")

        # Combine user profile preferences and trip-specific preferences
        # Note: In the controller, we might need to fetch user preferences if not embedded in trip
        # But for now, let's assume 'trip_preferences' is passed in context if available
        trip_prefs = context.get("trip_preferences", "")
        
        prompt = f"""
        Create a detailed itinerary for a trip to {destination} from {start_date} to {end_date}.
        {duration_str}
        Budget: {budget}
        Specific Trip Preferences: {trip_prefs}
        Weather Forecast: {weather_summary}
        
        Please provide the response in the following JSON structure:
        {{
            "trip_title": "Trip to {destination}",
            "summary": "A brief summary of the trip...",
            "personal_travel_tip": "A personalized travel tip based on the weather and preferences...",
            "days": [
                {{
                    "day_number": 1,
                    "date": "YYYY-MM-DD",
                    "theme": "Arrival and Exploration",
                    "weather_note": "Brief note on how weather affects this day's plan",
                    "rationale": "Why these activities were chosen for this day (e.g. 'Perfect sunny weather for outdoor walking' or 'Indoor museums chosen due to rain')",
                    "activities": [
                        {{
                            "time": "Morning",
                            "description": "Detailed description (2-3 sentences) of what to do, what to see, and why it's interesting.",
                            "location": "Precise Location Name for Maps",
                            "reason": "Why this fits the preferences/weather",
                            "cost_estimate": "Estimated cost range (e.g. $10-20, Free, $50+)"
                        }}
                    ]
                }}
            ]
        }}
        
        IMPORTANT:
        1. Generate an itinerary for EXACTLY the number of days specified ({duration_str}).
        2. Use the Weather Forecast to plan appropriate activities (e.g., indoor museums for rain, outdoor parks for sun).
        3. If the weather is bad, explicitly mention how the plan accounts for it in the 'weather_note'.
        4. The 'personal_travel_tip' MUST be unique and specific. DO NOT give generic advice like "check opening hours" or "wear comfortable shoes". Give a hidden gem, a local custom, or a specific dish to try based on the user's preferences.
        5. Ensure the activities align with the 'Specific Trip Preferences'.
        6. Provide DETAILED descriptions for each activity. Avoid one-liners. Explain what makes the place special.
        7. The 'rationale' field for each day is CRITICAL. Explain the logic behind the day's plan.
        8. For 'cost_estimate', provide a realistic price range in the local currency or USD (e.g., '$15-25', 'Free', '€30-40'). Do NOT use vague terms like 'Medium' or 'Low'.
        """
        return prompt


    def _get_mock_itinerary(self, context: Dict[str, Any]) -> Dict[str, Any]:
        destination = context.get("destination", "Paris")
        return {
            "trip_title": f"Trip to {destination}",
            "summary": f"A perfectly planned trip to {destination} tailored to your preferences. Enjoy a mix of cultural highlights, local cuisine, and relaxation.",
            "personal_travel_tip": "Try the local street food near the main square, it's a hidden gem!",
            "days": [
                {
                    "day_number": 1,
                    "date": context.get("start_date", "2023-01-01"),
                    "theme": "Arrival & First Impressions",
                    "weather_note": "Mild weather expected, perfect for a light walk.",
                    "rationale": "Since it's your first day, we've kept the schedule light to allow for check-in and recovery from travel, while still giving you a taste of the city.",
                    "activities": [
                        {
                            "time": "Morning",
                            "description": "Arrive at the airport and take a private transfer to your hotel. Freshen up and get settled.",
                            "location": "Airport/Hotel",
                            "reason": "Essential logistics.",
                            "cost_estimate": "$50-80"
                        },
                        {
                            "time": "Afternoon",
                            "description": f"Take a leisurely stroll around the {destination} City Center. Admire the architecture and soak in the atmosphere.",
                            "location": f"{destination} City Center",
                            "reason": "Great way to orient yourself without too much exertion.",
                            "cost_estimate": "Free"
                        },
                        {
                            "time": "Evening",
                            "description": "Enjoy a welcome dinner at a highly-rated local bistro known for its traditional dishes.",
                            "location": "Local Bistro",
                            "reason": "Experience local cuisine immediately.",
                            "cost_estimate": "$40-70"
                        }
                    ]
                },
                {
                    "day_number": 2,
                    "date": "2023-01-02", # Ideally calculate next day
                    "theme": "Cultural Deep Dive",
                    "weather_note": "Sunny skies forecast, ideal for sightseeing.",
                    "rationale": "With good weather, it's the perfect day to hit the major outdoor landmarks and museums.",
                    "activities": [
                        {
                            "time": "Morning",
                            "description": "Visit the iconic main landmarks of the city. Beat the crowds by arriving early.",
                            "location": "Main Square",
                            "reason": "Must-see attraction.",
                            "cost_estimate": "$15-25"
                        },
                        {
                            "time": "Afternoon",
                            "description": "Explore the National Museum to understand the history and culture of the region.",
                            "location": "National Museum",
                            "reason": "Aligns with cultural interests.",
                            "cost_estimate": "$20-30"
                        }
                    ]
                }
            ]
        }
