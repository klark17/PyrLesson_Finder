from locust import HttpLocust, TaskSet, task

class UserBehavior(TaskSet):
    def on_start(self):
        self.client.post("/auth/in", {"username":"Test1User", "password":"test"})

    @task(2)
    def index(self):
        self.client.get("/")

    @task(1)
    def profile(self):
        self.client.get("/profile/1")

    def on_stop(self):
        self.client.post("/auth/out", {"username":"Test1User", "password":"test"})


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000