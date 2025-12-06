class FlightOption:
    def __init__(self, tripId: str, carrier: str, flightNumber: str,
                 departureTime, arrivalTime, price: float):
        self.tripId = tripId
        self.carrier = carrier
        self.flightNumber = flightNumber
        self.departureTime = departureTime
        self.arrivalTime = arrivalTime
        self.price = price
