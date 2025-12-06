class Trip:
    def __init__(self, tripId: str, userId: str, origin: str, destination: str,
                 startDate, endDate, budget: float, homeCurrency: str,
                 destinationCurrency: str, createdAt, status: str,
                 planSummary: str):
        self.tripId = tripId
        self.userId = userId
        self.origin = origin
        self.destination = destination
        self.startDate = startDate
        self.endDate = endDate
        self.budget = budget
        self.homeCurrency = homeCurrency
        self.destinationCurrency = destinationCurrency
        self.createdAt = createdAt
        self.status = status
        self.planSummary = planSummary
