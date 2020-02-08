from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, forbidden_view_config, view_defaults
from pyramid.security import remember, forget
from sqlalchemy.exc import DBAPIError
from ..services.user_record import UserService
from ..form import LoginForm, SignupForm, SearchForm
from ..models import User
from .. import security
# from ..security import check_password

db_err_msg = "Not Found"


# TODO: change this for security purposes
#  https://docs.pylonsproject.org/projects/pyramid_cookbook/en/latest/auth/user_object.html
def get_user(request, user):
    current_user = request.dbsession.query(User).filter(User.username==user).first()
    if current_user:
        return current_user
    else:
        return None


@view_config(route_name='signup', renderer='../templates/signup.jinja2')
def signup(request):
    form = SignupForm(request.POST)
    if request.method == 'POST' and form.validate():
        new_user = User(active=True,
                        fName=form.fName.data,
                        lName=form.lName.data,
                        email=form.email.data,
                        birthday=form.birthday.data,
                        username=form.username.data)
        new_user.set_password(form.password.data)
        new_user.active = 1
        request.dbsession.add(new_user)
        return HTTPFound(location=request.route_url('login'))
    return {'title': 'Signup', 'form': form}


@view_config(route_name='login', renderer='../templates/login.jinja2')
def login(request):
    form = LoginForm(request.POST)
    return {'title': 'Login', 'form': form}


@view_config(route_name='auth', match_param='action=in', renderer='string',
             request_method='POST')
@view_config(route_name='auth', match_param='action=out', renderer='string')
def sign_in_out(request):
    username = request.POST.get('username')
    if username:
        user = UserService.by_name(username, request=request)
        if user and user.check_password(request.POST.get('password')):
            headers = remember(request, user.username)
        else:
            headers = forget(request)
    else:
        headers = forget(request)
    return HTTPFound(location=request.route_url('about'), headers=headers)


@view_config(route_name='search', renderer='../templates/search_lessons.jinja2')
def search(request):
    form = SearchForm(request.POST)
    return {'title': 'Search Lessons', 'form': form}


@view_config(route_name='profile', renderer='../templates/profile.jinja2', permission='view')
def profile(request):
    user = get_user(request, request.authenticated_userid)
    return {'title': 'Profile', 'user': user}
    # if request.matchdict == None:
    #     print("it is none")
    # # print(request.matchdict.values())
    # fName = request.matchdict['fName']
    # lName = request.matchdict['lName']
    # user = request.params.get('user', 'No User')


@view_config(route_name='lesson_info', renderer='../templates/lesson_info.jinja2', permission='view')
def lesson_info(request):
    return{}


@view_config(route_name='dep_lesson_info', renderer='../templates/dep_lesson_info.jinja2', permission='view')
def dep_lesson_info(request):
    return{}


@view_config(route_name='edit_profile', renderer='')
def edit_profile(request):
    return{}


@forbidden_view_config()
def forbidden_view(request):
    next_url = request.route_url('login', _query={'next': request.url})
    return HTTPFound(location=next_url)
