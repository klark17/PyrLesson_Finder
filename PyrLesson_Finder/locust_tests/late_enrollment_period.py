from locust import HttpLocust, TaskSet, task, TaskSequence, seq_task
import random

# TODO: make sure you discuss the differences between waitress and werkzeug in paper
# locust -f locustfile.py --no-web -c 1000 -r 100 --host=htps://127.0.0.1:5000
# locust -f locustfile.py --host=http://127.0.0.1:6543
# https://groups.google.com/forum/#!topic/pylons-discuss/kGNO3ifiacY
# https://stackoverflow.com/questions/55857058/how-to-find-the-cause-of-task-queue-depth-warnings-from-waitress
class UserBehavior(TaskSequence):
    user = None

    def on_start(self):
        self.user = str(random.randrange(21, 101))
        self.client.post("/auth/in", {"username":"Test" + self.user + "User", "password":"test" + self.user})

    @seq_task(1)
    def index(self):
        self.client.get("/")

    @seq_task(2)
    def profile(self):
        self.client.get("/profile")

    @seq_task(3)
    def search(self):
        self.client.get("/search")
        self.client.post("/search", {"location": "Town Pool"})

    @seq_task(4)
    def signup(self):
        self.client.post('/search/results/1/register_self')

    def on_stop(self):
        self.client.post("/auth/out", {"username":"Test" + self.user + "User", "password":"test" + self.user})


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000