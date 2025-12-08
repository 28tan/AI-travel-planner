class CurrencyRate:
    def __init__(self, tripId: str, baseCurrency: str, targetCurrency: str, rate: float, retrievedAt):
        self.tripId = tripId
        self.baseCurrency = baseCurrency
        self.targetCurrency = targetCurrency
        self.rate = rate
        self.retrievedAt = retrievedAt
