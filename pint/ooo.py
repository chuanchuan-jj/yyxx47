from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def join_group(self):
        self.client.post("/api/join", json={"goods_id": 1})