from locust import HttpUser, task, between

class TravelPlannerUser(HttpUser):
    wait_time = between(1, 3)

    @task(1)
    def health_check(self):
        self.client.get("/health")

    @task(2)
    def plan_trip_attempt(self):
        # This will likely return 401 without auth, but tests the endpoint reachability
        self.client.post("/trips/", json={
            "origin": "New York",
            "destination": "London",
            "start_date": "2023-06-01",
            "end_date": "2023-06-10",
            "budget": 2000.0,
            "transportation_preference": "FLIGHT"
        })

