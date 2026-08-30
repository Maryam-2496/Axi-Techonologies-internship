from locust import HttpUser, task, between

class BackendUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def check_health(self):
        self.client.get("/healthz")

    @task(2)
    def check_ready(self):
        self.client.get("/readyz")

    @task(1)
    def login(self):
        self.client.post("/auth/login", json={
            "email": "test15@example.com",
            "password": "password123"
        })