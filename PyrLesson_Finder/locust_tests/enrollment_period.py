from locust import HttpUser, SequentialTaskSet, task, between, TaskSet
import re
import datetime
import random

# sets a hash of params to search for
def search_params(response):
    day_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    params = {"level": random.randrange(1, 7),
              "location": "Recreation Center " + str(random.randrange(1, 31)),
              "day": day_of_week[random.randrange(0, len(day_of_week))]}
    return params


# sets a set of params to signup with Lesson Finder
def signup_params(num):
    year = random.randrange(1960, 2001)
    month = random.randrange(1, 13)
    day = random.randrange(1, 29)
    fName = "Test" + num
    email = "test" + num + "user@mail.com"
    username = "Test" + num + "User"
    password = "thi5IztesT" + num
    params = {"fName": fName,
              "lName": "User",
              "email": email,
              "birthday": datetime.date(year, month, day),
              "username": username,
              "password": password}

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

    @task
    def user_login(self):
        response = self.client.get('/login')
        self.username = 'Test' + self.id + 'User'
        self.password = 'thi5IztesT' + self.id
        self.client.post("http://127.0.0.1:6543/auth/in",
                         {"username": self.username,
                          "password": self.password,
                          "submit": "Login"})

    @task
    def successful_register(self):
        get_search = self.client.get("/search")
        response = self.client.post("/search/results", search_params(get_search))
        register_self = random.randrange(1, 3)
        self_reg_link = find_lesson_id(response, 'http://127.0.0.1:6543/search/results/\d*/register_self')
        if (register_self == 1) and self_reg_link:
            self.client.request("post", self_reg_link, auth=(self.username, self.password))
        else:
            dep_link = find_lesson_id(response, 'http://127.0.0.1:6543/search/results/\d*/register')
            if dep_link:
                response = self.client.get(dep_link, auth=(self.username, self.password))
                dep_reg = find_lesson_id(response, 'http://127.0.0.1:6543/search/results/\d*/register_dep/')
                if dep_reg:
                    fName = "Dependent" + self.id
                    email = "test" + self.id + "user@mail.com"
                    self.client.request("post",
                                        dep_reg,
                                        data={"fName": fName,
                                              "lName": "User",
                                              "contactEmail": email,
                                              "contactNum": ""},
                                        auth=(self.username, self.password))

    @task
    def index(self):
        self.client.get("http://localhost:6543/")

    def on_stop(self):
        self.client.post("http://localhost:6543/auth/out")


class NewUserBehavior(SequentialTaskSet):
    id = str(random.randrange(1, 501))
    username = None
    password = None

    @task
    def home(self):
        self.client.get("/")

    @task
    def failed_register(self):
        get_search = self.client.get("/search")
        response = self.client.post("/search/results", search_params(get_search))
        link = find_lesson_id(response, 'http://127.0.0.1:6543/search/results/\d*/register_self')
        if link:
            self.client.post(link)

    @task
    def signup(self):
        self.client.get("/signup")
        self.client.post("/signup", signup_params(self.id))

    @task
    def start_authorized_user(self):
        self.client.get('/login')
        self.username = 'Test' + self.id + 'User'
        self.password = 'thi5IztesT' + self.id
        self.client.post("http://127.0.0.1:6543/auth/in",
                         {"username": self.username,
                          "password": self.password,
                          "submit": "Login"})

    @task
    def successful_register(self):
        get_search = self.client.get("/search")
        response = self.client.post("/search", search_params(get_search))
        link = find_lesson_id(response, 'http://127.0.0.1:6543/search/results/\d*/register_self')
        if link:
            self.client.post(link, auth=(self.username, self.password))

    def on_stop(self):
        self.client.post("http://localhost:6543/auth/out")


class RandomBehavior(TaskSet):
    id = str(random.randrange(1, 501))
    username = None
    password = None
    profile_path = None

    def on_start(self):
        self.client.get('/login')
        self.username = 'Test' + self.id + 'User'
        self.password = 'thi5IztesT' + self.id
        self.profile_path = "http://127.0.0.1:6543/profile/" + self.id
        self.client.post("http://127.0.0.1:6543/auth/in",
                         {"username": self.username,
                          "password": self.password,
                          "submit": "Login"})

    @task
    def edit_username(self):
        edit_link = "http://127.0.0.1:6543/profile/" + self.id + "/edit"
        self.client.get(edit_link)
        self.client.request("post",
                            edit_link,
                            data={'username': self.username + "Changed"},
                            auth=(self.username, self.password))

    @task
    def register_self(self):
        get_search = self.client.get("/search")
        response = self.client.post("/search", search_params(get_search))
        link = find_lesson_id(response, 'http://127.0.0.1:6543/search/results/\d*/register_self')
        if link:
            self.client.post(link, auth=(self.username, self.password))

    @task
    def register_dep(self):
        get_search = self.client.get("/search")
        response = self.client.post("/search/results", search_params(get_search))
        dep_link = find_lesson_id(response, 'http://127.0.0.1:6543/search/results/\d*/register')
        if dep_link:
            response = self.client.get(dep_link, auth=(self.username, self.password))
            dep_reg = find_lesson_id(response, 'http://127.0.0.1:6543/search/results/\d*/register_dep/')
            if dep_reg:
                fName = "Dependent" + self.id
                email = "test" + self.id + "user@mail.com"
                self.client.request("post",
                                    dep_reg,
                                    data={"fName": fName,
                                        "lName": "User",
                                        "contactEmail": email,
                                        "contactNum": ""},
                                    auth=(self.username, self.password))

    @task
    def remove_lesson(self):
        profile_resp = self.client.request("get", self.profile_path)
        lesson_link = find_lesson_id(profile_resp, 'http://127.0.0.1:6543/lesson/info/\d*')
        if lesson_link:
            lesson_info = self.client.get(lesson_link)
            unregister_self = find_lesson_id(lesson_info, 'http://127.0.0.1:6543/lesson/\d*/unregister/')
            if unregister_self:
                self.client.post(unregister_self)
        else:
            pass

    @task
    def remove_dep_lesson(self):
        profile_resp = self.client.request("get", self.profile_path)
        lesson_link = find_lesson_id(profile_resp, 'http://127.0.0.1:6543/lesson/\d*/dep_info/\d*')
        if lesson_link:
            lesson_info = self.client.get(lesson_link)
            unregister_dep = find_lesson_id(lesson_info, 'http://127.0.0.1:6543/lesson/\d*/unregister/\d*/')
            if unregister_dep:
                self.client.post(unregister_dep)
        else:
            pass

    @task
    def update_dependent(self):
        profile_resp = self.client.request("get", self.profile_path)
        lesson_link = find_lesson_id(profile_resp, 'http://127.0.0.1:6543/lesson/\d*/dep_info/\d*')
        if lesson_link:
            lesson_info = self.client.get(lesson_link)
            edit_info_link = find_lesson_id(lesson_info, 'http://127.0.0.1:6543/lesson/edit/\d*')
            self.client.get(edit_info_link, auth=(self.username, self.password))
            new_email = "change" + self.id + "email@mail.com"
            new_phone = "203-123-45" + self.id
            self.client.request("post",
                                edit_info_link,
                                data={"contactEmail": new_email,
                                      "contactNum": new_phone},
                                auth=(self.username, self.password))
        else:
            pass

    @task
    def delete_dependent(self):
        profile_resp = self.client.request("get", self.profile_path, auth=(self.username, self.password))
        delete_link = find_lesson_id(profile_resp, 'http://127.0.0.1:6543/remove_dep/\d*')
        if delete_link:
            self.client.request("post",
                                delete_link,
                                auth=(self.username, self.password))
        else:
            pass

    def on_stop(self):
        self.client.post("http://localhost:6543/auth/out")


class WebsiteUser(HttpUser):
    tasks = {
        NewUserBehavior: 1,
		ExistingUserBehavior: 10,
		RandomBehavior: 1
    }
    wait_time = between(3.0, 10.5)
