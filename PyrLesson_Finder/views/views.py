from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, forbidden_view_config, view_defaults
from pyramid.security import remember, forget
from sqlalchemy.exc import DBAPIError
from ..form import LoginForm, SignupForm
from ..models import User
from .. import security
# from ..security import check_password

db_err_msg = "Not Found"
# TODO: fix login, stating error User does not have password_hash
# TODO: refer to https://docs.pylonsproject.org/projects/pyramid/en/latest/tutorials/wiki2/authentication.html

@view_defaults(renderer='../templates/about.jinja2')
class Views:
    def __init__(self, request):
        self.request = request

    @property
    def current_user(self):
        session = self.request.session
        if 'counter' not in session:
            session['counter'] = security.get_user(self.request)
        return session['counter']

    @view_config(route_name='signup', renderer='../templates/signup.jinja2')
    def signup(self):
        user = User()
        form = SignupForm(self.request.POST)
        if self.request.method == 'POST' and form.validate():
            user.active = 1
            form.populate_obj(user)
            self.request.dbsession.add(user)
            return HTTPFound(location=self.request.route_url('login'))
        return {'title': 'Signup', 'form': form}

    @view_config(route_name='login', renderer='../templates/login.jinja2')
    def login(self):
        form = LoginForm(self.request.POST)
        login_url = self.request.route_url('login')
        referrer = self.request.url
        # if referrer == login_url:
        #     referrer = self.request.route_url('profile', user='')
        # came_from = self.request.params.get('came_from', referrer)
        next_url = self.request.params.get('next', self.request.referrer)
        if not next_url:
            next_url = self.request.route_url('profile', user='')
        message = ''
        login = ''
        if 'form.submitted' and self.request.params:
            login = self.request.params['username']
            password = self.request.params['password']
            user = self.request.dbsession.query(User).filter_by(username=login).first()
            if user is not None and user.check_password(password):
                next_url = self.request.route_url('profile',
                                                  first=user.fName,
                                                  last=user.lName,
                                                  username=user.username,
                                                  email=user.email
                                                  )
                headers = remember(self.request, user.id)
                return HTTPFound(location=next_url, headers=headers)
            message = 'Failed login'
        return dict(
            name='Login',
            message=message,
            url=self.request.application_url + '/login',
            # url=request.route_url('login'),
            # came_from=came_from,
            next_url=next_url,
            login=login,
            form=form
        )
            # if query.filter_by(username=form.username.data).scalar():
            #     user = query.filter_by(username=form.username.data).first()
            #     if user and user.password == form.password.data:
            #         return HTTPFound('/profile?fName=' + user.fName + '&lName=' + user.lName)
            #     else:
            #         return Response(db_err_msg, content_type='text/plain', status=500)
        # return {'title': 'Login', 'form': form}

    @view_config(route_name='logout')
    def logout(self):
        headers = forget(self.request)
        next_url = self.request.route_url('login')
        return HTTPFound(location=next_url, headers=headers)

    @view_config(route_name='search', renderer='../templates/search.jinja2')
    def search(self):
        return {'title' : 'Search Lessons'}

    @view_config(route_name='profile', renderer='../templates/profile.jinja2')
    def profile(self):
        print(self.request.session)
        first = self.request.matchdict['first']
        last = self.request.matchdict['last']
        username = self.request.matchdict['username']
        email = self.request.matchdict['email']
        return {'first': first, 'last': last, 'username': username, 'email': email}
        # if request.matchdict == None:
        #     print("it is none")
        # # print(request.matchdict.values())
        # fName = request.matchdict['fName']
        # lName = request.matchdict['lName']
        # user = request.params.get('user', 'No User')

    @forbidden_view_config()
    def forbidden_view(self):
        next_url = self.request.route_url('login', _query={'next': self.request.url})
        return HTTPFound(location=next_url)
