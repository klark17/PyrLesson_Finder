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

# sets a hash of params to search for
def search_params(response):
    # year = random.randrange(2020, 2021)
    # month = random.randrange(1, 13)
    # day = random.randrange(1, 29)
    # startDate = date(year, month, day)
    # startTime = random.randrange(7, 19)
    day_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    params = {"level": random.randrange(1, 7),
              "location": "Recreation Center " + str(random.randrange(1, 31)),
              "day": day_of_week[random.randrange(0, len(day_of_week))]}
    return params


# sets a set of params to signup with Lesson Finder
def signup_params(num):
    id = str(num + 1)
    year = random.randrange(1960, 2001)
    month = random.randrange(1, 13)
    day = random.randrange(1, 29)
    params = {"fName": "Test" + id,
              "lName": "User",
              "email": "test" + id + "user@mail.com",
              "birthday": datetime.date(year, month, day),
              "username": "Test" + id + "User",
              "password": "thi5IztesT" + id}

    return(params)

# finds a random lesson on the page to signup for
def find_lesson_id(resp, pattern):
    result = re.search(pattern, resp.text)
    if result:
        lesson = str(result.group(0))
        return lesson
    else:
        return False


class ExistingUserBehavior(SequentialTaskSet):

    id = str(random.randrange(1, 501))
    username = None
    password = None

    def on_start(self):
        print("Starting existing user...")
        response = self.client.get('/login')
        self.username = 'Test' + self.id + 'User'
        self.password = 'thi5IztesT' + self.id
        self.client.post('/auth/in', {'username': self.username,
                                           'password': self.password})

    @task
    def profile(self):
        self.client.request("get", "/profile", auth=(self.username, self.password))


    @task
    def successful_register(self):
        get_search = self.client.get("/search")
        response = self.client.post("/search/results", search_params(get_search))
        register_self = random.randrange(1, 3)
        if register_self == 1:
            link = find_lesson_id(response, 'http://127.0.0.1:6543/search/results/\d*/register_self')
            self.client.request("post", link, auth=(self.username, self.password))
        else:
            link = find_lesson_id(response, 'http://127.0.0.1:6543/search/results/\d*/register')
            response = self.client.request("get", link, auth=(self.username, self.password))
            self.client.request("post",
                                link,
                                params={
                                "fName": "Dependent " + self.id,
                                "lName": "User",
                                "contactEmail": ""},
                               auth=(self.username, self.password))

    @task
    def index(self):
        self.client.get("/")

    def on_stop(self):
        self.client.post("/auth/out", {"username":self.username, "password":self.password})


class NewUserBehavior(SequentialTaskSet):
    id = str(random.randrange(501, 1001))
    username = None
    password = None

    @task
    def home(self):
        print("Starting new user...")
        self.client.get("/")

    @task
    def failed_register(self):
        get_search = self.client.get("/search")
        response = self.client.post("/search", search_params(get_search))
        link = find_lesson_id(response, 'http://127.0.0.1:6543/search/results/\d*/register_self')
        self.client.request("post", link)

    @task
    def signup(self):
        self.client.get("/signup")
        self.client.post("/signup", signup_params(int(self.id)))

    @task
    def start_authorized_user(self):
        self.client.get('/login')
        self.username = 'Test' + self.id + 'User'
        self.password = 'thi5IztesT' + self.id
        self.client.post('/auth/in', {'username': self.username,
                                           'password': self.password})

    @task
    def profile(self):
        self.client.request("get", "/profile", auth=(self.username, self.password))

    @task
    def successful_register(self):
        get_search = self.client.get("/search")
        response = self.client.post("/search", search_params(get_search))
        link = find_lesson_id(response, 'http://127.0.0.1:6543/search/results/\d*/register_self')
        if link:
            self.client.request("post", link, auth=(self.username, self.password))

    def on_stop(self):
        self.client.post("/auth/out", {"username":self.username, "password":self.password})


class RandomBehavior(TaskSet):
    id = str(random.randrange(1, 501))
    username = None
    password = None

    def on_start(self):
        self.client.get('/login')
        self.username = 'Test' + self.id + 'User'
        self.password = 'thi5IztesT' + self.id
        self.client.post('/auth/in', {'username': self.username,
                                           'password': self.password})

    @task
    def edit_username(self):
        self.client.request("get", "/profile", auth=(self.username, self.password))
        edit_link = "http://127.0.0.1:6543/profile/" + self.id + "/edit"
        response = self.client.get(edit_link)
        self.client.post(edit_link, {'username': self.username + "Changed"})

    @task
    def register_self(self):
        get_search = self.client.get("/search")
        response = self.client.post("/search", search_params(get_search))
        link = find_lesson_id(response, 'http://127.0.0.1:6543/search/results/\d*/register_self')
        if link:
            self.client.request("post", link, auth=(self.username, self.password))

    @task
    def register_dep(self):
        get_search = self.client.get("/search")
        response = self.client.post("/search/results", search_params(get_search))
        link = find_lesson_id(response, 'http://127.0.0.1:6543/search/results/\d*/register')
        response = self.client.request("get", link, auth=(self.username, self.password))
        if response.code == 200:
            self.client.request("post",
                                link,
                                params={
                                "fName": "Dependent " + self.id,
                                "lName": "User",
                                "contactEmail": ""},
                               auth=(self.username, self.password))

    @task
    def remove_lesson(self):
        profile_resp = self.client.request("get", "/profile", auth=(self.username, self.password))
        lesson_link = find_lesson_id(profile_resp, 'http://127.0.0.1:6543/lesson/info/\d*')
        if lesson_link:
            lesson_info = self.client.get(lesson_link)
            unregister_link = find_lesson_id(lesson_info, 'http://127.0.0.1:6543/lesson/\d*/unregister/')
            self.client.post(unregister_link)
        else:
            pass

    @task
    def update_dependent(self):
        profile_resp = self.client.request("get", "/profile", auth=(self.username, self.password))
        lesson_link = find_lesson_id(profile_resp, 'http://127.0.0.1:6543/lesson/\d*/dep_info/\d*')
        if lesson_link:
            lesson_info = self.client.get(lesson_link)
            edit_info_link = find_lesson_id(lesson_info, 'http://127.0.0.1:6543/lesson/edit/\d*')
            edit_page = self.client.get(edit_info_link)
            new_email = "change" + self.id + "email@mail.com"
            new_phone = "203-123-45" + self.id
            self.client.post(edit_page, {'contactEmail': new_email,
                                  'contactNum': new_phone})
        else:
            pass

    @task
    def delete_dependent(self):
        profile_resp = self.client.request("get", "/profile", auth=(self.username, self.password))
        delete_link = find_lesson_id(profile_resp, 'http://127.0.0.1:6543/remove_dep/\d*')
        if delete_link:
            self.client.request("post",
                                delete_link,
                                auth=(self.username, self.password))
        else:
            pass

    def on_stop(self):
        self.client.post("/auth/out", {"username":self.username, "password":self.password})


class WebsiteUser(HttpUser):
    tasks = {
        NewUserBehavior: 1,
        ExistingUserBehavior: 10,
        RandomBehavior: 1
    }
    wait_time = between(3.0, 10.5)
