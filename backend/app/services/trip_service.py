import asyncio
from typing import Optional, List
from app.services.weather_service import WeatherService
from app.services.flight_service import FlightService
from app.services.places_service import PlacesService
from app.services.route_service import RouteService
from app.services.currency_service import CurrencyService
from app.repositories.trip_repository import TripRepository
from app.models.api import CreateTripRequest, TripSummaryResponse
from app.models.trip import Trip, TripStatus, TransportationPreference

class TripService:
    def __init__(self):
        self.weather_service = WeatherService()
        self.flight_service = FlightService()
        self.places_service = PlacesService()
        self.route_service = RouteService()
        self.currency_service = CurrencyService()
        self.trip_repo = TripRepository()

    async def create_trip_plan(self, user_id: str, request: CreateTripRequest) -> TripSummaryResponse:
        # 1. Geocode Destination
        dest_coords = await self.places_service.geocode(request.destination)
        origin_coords = await self.places_service.geocode(request.origin) # For flight search if needed
        
        lat, lon = (0, 0)
        if dest_coords:
            lat, lon = dest_coords['lat'], dest_coords['lng']

        # 2. Parallel Fetch of External Data
        weather_task = self.weather_service.get_forecast(lat, lon, request.start_date, request.end_date)
        
        # For flights, we need IATA codes. Geocoding gives coords. 
        # Real implementation would need Airport lookup. 
        # For MVP, we might skip or mock IATA lookup or use city names if API supports.
        # Aviationstack needs IATA. We'll skip or mock for now if we don't have IATA.
        if request.transportation_preference in [TransportationPreference.FLIGHT, TransportationPreference.BOTH]:
            origin_iata = self.flight_service.get_iata_code(request.origin)
            dest_iata = self.flight_service.get_iata_code(request.destination)
            flight_task = self.flight_service.search_flights(origin_iata, dest_iata)
            return_flight_task = self.flight_service.search_flights(dest_iata, origin_iata)
        else:
            flight_task = asyncio.sleep(0, result=None)
            return_flight_task = asyncio.sleep(0, result=None)
        
        poi_task = self.places_service.search_nearby(lat, lon, request.trip_preferences)

        if request.transportation_preference in [TransportationPreference.DRIVE, TransportationPreference.BOTH]:
            driving_task = self.route_service.get_driving_estimate(request.origin, request.destination)
        else:
            driving_task = asyncio.sleep(0, result=None)

        origin_country_task = self.places_service.get_country(request.origin)
        dest_country_task = self.places_service.get_country(request.destination)

        weather, flights, return_flights, pois, driving, origin_country, dest_country = await asyncio.gather(
            weather_task, flight_task, return_flight_task, poi_task, driving_task, origin_country_task, dest_country_task
        )
        
        # Determine currency rate
        origin_currency = self.currency_service.get_currency_code(origin_country)
        dest_currency = self.currency_service.get_currency_code(dest_country)
        currency_rate = await self.currency_service.get_exchange_rate(origin_currency, dest_currency)

        # 3. Create Trip in DB (Draft)
        trip = Trip(
            user_id=user_id,
            origin=request.origin,
            destination=request.destination,
            start_date=request.start_date,
            end_date=request.end_date,
            budget=request.budget,
            transportation_preference=request.transportation_preference,
            trip_preferences=request.trip_preferences,
            status=TripStatus.DRAFT,
            weather_summary=weather,
            flight_options=flights,
            return_flight_options=return_flights,
            driving_options=driving,
            poi_highlights=pois,
            currency_rate=currency_rate
        )
        saved_trip = await self.trip_repo.create_trip(trip)

        # 4. Construct Response
        return TripSummaryResponse(
            trip_id=saved_trip.id,
            weather_summary=weather,
            flight_options=flights,
            return_flight_options=return_flights,
            driving_options=driving,
            poi_highlights=pois,
            currency_rate=currency_rate
        )

    async def get_user_trips(self, user_id: str) -> list[Trip]:
        return await self.trip_repo.get_user_trips(user_id)

    async def confirm_trip(self, trip_id: str, user_id: str) -> bool:
        trip = await self.trip_repo.get_trip(trip_id)
        if trip and trip.user_id == user_id:
            return await self.trip_repo.update_trip_status(trip_id, TripStatus.PLANNED)
        return False

    async def get_trip(self, trip_id: str, user_id: str) -> Optional[Trip]:
        trip = await self.trip_repo.get_trip(trip_id)
        if trip and trip.user_id == user_id:
            # Refresh data on read
            return await self._refresh_trip_data(trip)
        return None

    async def _refresh_trip_data(self, trip: Trip) -> Trip:
        # 1. Geocode (needed for weather/places)
        dest_coords = await self.places_service.geocode(trip.destination)
        lat, lon = (0, 0)
        if dest_coords:
            lat, lon = dest_coords['lat'], dest_coords['lng']

        # 2. Fetch fresh data
        weather_task = self.weather_service.get_forecast(lat, lon)
        # Re-fetch flights (using mock IATA for now as per create_trip)
        flight_task = asyncio.sleep(0, result=None)
        return_flight_task = asyncio.sleep(0, result=None)
        if trip.transportation_preference in [TransportationPreference.FLIGHT, TransportationPreference.BOTH]:
            origin_iata = self.flight_service.get_iata_code(trip.origin)
            dest_iata = self.flight_service.get_iata_code(trip.destination)
            flight_task = self.flight_service.search_flights(origin_iata, dest_iata)
            return_flight_task = self.flight_service.search_flights(dest_iata, origin_iata)
        
        driving_task = asyncio.sleep(0, result=None)
        if trip.transportation_preference in [TransportationPreference.DRIVE, TransportationPreference.BOTH]:
            driving_task = self.route_service.get_driving_estimate(trip.origin, trip.destination)

        weather, flights, return_flights, driving = await asyncio.gather(weather_task, flight_task, return_flight_task, driving_task)

        # 3. Update Trip object
        trip.weather_summary = weather
        trip.flight_options = flights
        trip.return_flight_options = return_flights
        trip.driving_options = driving
        
        # 4. Save to DB
        await self.trip_repo.update_trip(trip.id, {
            "weather_summary": weather,
            "flight_options": flights,
            "return_flight_options": return_flights,
            "driving_options": driving
        })
        
        return trip

    async def delete_trip(self, trip_id: str, user_id: str) -> bool:
        return await self.trip_repo.delete_trip(trip_id, user_id)
