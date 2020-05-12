from locust import HttpLocust, TaskSet, task
# import resource
# resource.setrlimit(resource.RLIMIT_NOFILE, (10240, 9223372036854775807))

# locust -f locustfile.py --no-web -c 1000 -r 100 --host=htps://127.0.0.1:5000
# locust -f locustfile.py --host=http://127.0.0.1:6543
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