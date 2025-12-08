from .location import Location
from .route_estimate import RouteEstimate

class PlacesService:
    def geocode(self, destination: str) -> Location:
        pass

    def getPointsOfInterest(self, placeId: str) -> list:
        pass

    def estimateRoute(self, origin: str, dest: str) -> RouteEstimate:
        pass
