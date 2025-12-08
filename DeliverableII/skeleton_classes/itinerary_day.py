class ItineraryDay:
    def __init__(self, itineraryId: str, dayNumber: int, date,
                 weatherSummary: str, activities: list, notes: str):
        self.itineraryId = itineraryId
        self.dayNumber = dayNumber
        self.date = date
        self.weatherSummary = weatherSummary
        self.activities = activities
        self.notes = notes
