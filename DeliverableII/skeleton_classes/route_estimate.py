class RouteEstimate:
    def __init__(self, tripId: str, mode: str, durationMinutes: int, distanceKm: float):
        self.tripId = tripId
        self.mode = mode
        self.durationMinutes = durationMinutes
        self.distanceKm = distanceKm
