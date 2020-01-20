from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, forbidden_view_config
from pyramid.security import remember, forget
from sqlalchemy.exc import DBAPIError
from ..form import LoginForm, SignupForm
from ..models import User
# from ..security import check_password

db_err_msg = "Not Found"
# TODO: fix login, stating error User does not have password_hash
# TODO: refer to https://docs.pylonsproject.org/projects/pyramid/en/latest/tutorials/wiki2/authentication.html

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
    form = LoginForm(request.POST)
    next_url = request.params.get('next', request.referrer)
    if not next_url:
        next_url = request.route_url('login')
    message = ''
    login = ''
    if 'form.submitted' and request.params:
        login = request.params['username']
        password = request.params['password']
        user = request.dbsession.query(User).filter_by(username=login).first()
        if user is not None and user.check_password(password):
            headers = remember(request, user.id)
            return HTTPFound(location=next_url, headers=headers)
        message = 'Failed login'
    return dict(
        message=message,
        url=request.route_url('login'),
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
def logout(request):
    headers = forget(request)
    next_url = request.route_url('login')
    return HTTPFound(location=next_url, headers=headers)


@view_config(route_name='search', renderer='../templates/search.jinja2')
def search(request):
    return {'title' : 'Search Lessons'}


@view_config(route_name='profile', renderer='../templates/profile.jinja2')
def profile(request):
    fName = request.matchdict['fName']
    lName = request.matchdict['lName']
    # user = request.params.get('user', 'No User')
    return {'fName': fName, 'lName': lName}

@forbidden_view_config()
def forbidden_view(request):
    next_url = request.route_url('login', _query={'next': request.url})
    return HTTPFound(location=next_url)
