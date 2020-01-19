from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from pyramid.security import remember, forget
from sqlalchemy.exc import DBAPIError
from ..form import LoginForm, SignupForm
from ..models import User
from ..security import USERS, check_password

db_err_msg = "Not Found"


@view_config(route_name='signup', renderer='../templates/signup.jinja2')
def signup(request):
    user = User()
    form = SignupForm(request.POST)
    if request.method == 'POST' and form.validate():
        user.active = 1
        form.populate_obj(user)
        request.dbsession.add(user)
        return HTTPFound(location=request.route_url('login'))
    return {'title': 'Signup', 'form': form}


@view_config(route_name='login', renderer='../templates/login.jinja2')
def login(request):
    user = User()
    form = LoginForm(request.POST)
    login_url = request.route_url('login')
    referrer = request.route.url
    if referrer == login_url:
        referrer = '/'
    came_from = request.params.get('came_from', referrer)
    message = ''
    login = ''
    password = ''
    if request.method == 'POST' and form.validate():
        query = request.dbsession.query(User)
        if query.filter_by(username=form.username.data).scalar():
            user = query.filter_by(username=form.username.data).first()
            if user and user.password == form.password.data:
                return HTTPFound('/profile?fName=' + user.fName + '&lName=' + user.lName)
            else:
                return Response(db_err_msg, content_type='text/plain', status=500)
    return {'title': 'Login', 'form': form}


@view_config(route_name='search', renderer='../templates/search.jinja2')
def search(request):
    return {'title' : 'Search Lessons'}


@view_config(route_name='profile', renderer='../templates/profile.jinja2')
def profile(request):
    fName = request.matchdict['fName']
    lName = request.matchdict['lName']
    # user = request.params.get('user', 'No User')
    return {'fName': fName, 'lName': lName}
