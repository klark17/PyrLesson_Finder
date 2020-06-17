from locust import HttpUser, SequentialTaskSet, task, between, TaskSet
import re
import datetime
from datetime import date, time
import random
import pdb

# locust -f locustfile.py --no-web -c 1000 -r 100 --host=htps://127.0.0.1:5000
# locust -f enrollment_period.py --host=http://127.0.0.1:6543
# https://groups.google.com/forum/#!topic/pylons-discuss/kGNO3ifiacY
# https://stackoverflow.com/questions/55857058/how-to-find-the-cause-of-task-queue-depth-warnings-from-waitress

class NewUserBehavior(SequentialTaskSet):
    id = None
    username = None
    password = None

    @task
    def home(self):
        self.id = str(random.randrange(1, 501))
        self.client.get("/")

    @task
    def start_authorized_user(self):
        pdb.set_trace()
        self.client.get('/login')
        self.username = 'Test' + self.id + 'User'
        self.password = 'thi5IztesT' + self.id
        self.client.post("http://127.0.0.1:6543/auth/in",
                         {"username": self.username,
                          "password": self.password,
                          "submit": "Login"})

    def on_stop(self):
        self.client.post("http://localhost:6543/auth/out")


class WebsiteUser(HttpUser):
    tasks = {
        NewUserBehavior
    }
    wait_time = between(3.0, 10.5)
