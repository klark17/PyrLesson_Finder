from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, forbidden_view_config, view_defaults
from pyramid.security import remember, forget
from sqlalchemy.exc import DBAPIError
from ..services.user_record import UserService
from ..form import LoginForm, SignupForm
from ..models import User
from .. import security
# from ..security import check_password

db_err_msg = "Not Found"


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
        # if query.filter_by(username=form.username.data).scalar():
        #     user = query.filter_by(username=form.username.data).first()
        #     if user and user.password == form.password.data:
        #         return HTTPFound('/profile?fName=' + user.fName + '&lName=' + user.lName)
        #     else:
        #         return Response(db_err_msg, content_type='text/plain', status=500)


@view_config(route_name='auth', match_param='action=in', renderer='string',
             request_method='POST')
@view_config(route_name='auth', match_param='action=out', renderer='string')
def sign_in_out(request):
    username = request.POST.get('username')
    if username:
        user = UserService.by_name(username, request=request)
        if user and user.verify_password(request.POST.get('password')):
            headers = remember(request, user.name)
        else:
            headers = forget(request)
    else:
        headers = forget(request)
    return HTTPFound(location=request.route_url('home'), headers=headers)


@view_config(route_name='search', renderer='../templates/search.jinja2')
def search(request):
    return {'title' : 'Search Lessons'}


@view_config(route_name='profile', renderer='../templates/profile.jinja2', permission='view')
def profile(request):
    return {'title': 'Profile'}
    # if request.matchdict == None:
    #     print("it is none")
    # # print(request.matchdict.values())
    # fName = request.matchdict['fName']
    # lName = request.matchdict['lName']
    # user = request.params.get('user', 'No User')


@view_config(route_name='edit_profile', renderer='')
def edit_profile(request):
    return{}


@forbidden_view_config()
def forbidden_view(request):
    next_url = request.route_url('login', _query={'next': request.url})
    return HTTPFound(location=next_url)
