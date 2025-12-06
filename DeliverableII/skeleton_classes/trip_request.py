from .preference import Preference

class TripRequest:
    def __init__(self, origin: str, destination: str, startDate, endDate,
                 budget: float, preferences: Preference,
                 transportMode: str, homeCurrency: str, destinationCurrency: str):
        self.origin = origin
        self.destination = destination
        self.startDate = startDate
        self.endDate = endDate
        self.budget = budget
        self.preferences = preferences
        self.transportMode = transportMode
        self.homeCurrency = homeCurrency
        self.destinationCurrency = destinationCurrency
