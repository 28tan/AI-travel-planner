class WeatherForecast:
    def __init__(self, tripId: str, date, tempHigh: float, tempLow: float,
                 condition: str, precipChance: float):
        self.tripId = tripId
        self.date = date
        self.tempHigh = tempHigh
        self.tempLow = tempLow
        self.condition = condition
        self.precipChance = precipChance
