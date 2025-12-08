from .trip import Trip
from .preference import Preference
from .itinerary import Itinerary

class TripRepository:
    def saveTrip(self, trip: Trip, prefs: Preference, itinerary: Itinerary, days: list):
        pass

    def findTripsByUser(self, userId: str) -> list:
        pass

    def findTripWithDetails(self, tripId: str, userId: str) -> Trip:
        pass

    def deleteTrip(self, userId: str, tripId: str):
        pass
