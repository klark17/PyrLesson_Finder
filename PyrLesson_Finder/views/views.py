from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound, HTTPForbidden
from pyramid.view import view_config, forbidden_view_config, view_defaults
from pyramid.security import remember, forget
from ..services.user_record import UserService
from ..services.lesson_record import LessonService
from ..services.dependent_record import DependentService
from ..form import LoginForm, SignupForm, SearchForm, RegistrationForm, UpdateUsernameForm, EditRegistrationForm, levels
from ..models import User, Participant
import pdb
from .. import security
# from ..security import check_password

db_err_msg = "Not Found"

# TODO: add edit_registration for dependents
# TODO: change this for security purposes
#  https://docs.pylonsproject.org/projects/pyramid_cookbook/en/latest/auth/user_object.html
def get_user(request, user):
    if user:
        current_user = request.dbsession.query(User).get(user)
        return current_user
    else:
        raise HTTPForbidden


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
        request.session.flash('User Created!')
        return HTTPFound(location=request.route_url('login'))
    return {'title': 'Signup', 'form': form}


@view_config(route_name='login', renderer='../templates/login.jinja2')
def login(request):
    form = LoginForm(request.POST)
    return {'title': 'Login', 'form': form}


# TODO: check if time for session
@view_config(route_name='auth', match_param='action=in', renderer='string',
             request_method='POST')
@view_config(route_name='auth', match_param='action=out', renderer='string')
def sign_in_out(request):
    username = request.POST.get('username')
    if username:
        user = UserService.by_username(username, request=request)
        if user and user.check_password(request.POST.get('password')):
            headers = remember(request, user.id)
        else:
            headers = forget(request)
    else:
        headers = forget(request)
    return HTTPFound(location=request.route_url('about'), headers=headers)


@view_config(route_name='search', renderer='../templates/search_lessons.jinja2')
def search(request):
    form = SearchForm(request.POST)
    return {'title': 'Search Lessons', 'form': form}


@view_config(route_name='results', renderer='../templates/search_results.jinja2')
def results(request):
    lessons = LessonService.get_lessons(request)
    if len(lessons) == 0:
        return HTTPFound(location=request.route_url('search'))
    else:
        return {'title': 'Results', 'results': lessons}


@view_config(route_name='profile', renderer='../templates/profile.jinja2', permission='view')
def profile(request):
    user = get_user(request, request.authenticated_userid)
    return {'title': 'Profile', 'user': user}


@view_config(route_name='lesson_info', renderer='../templates/lesson_info.jinja2', permission='view')
def lesson_info(request):
    lesson = LessonService.get_by_id(request)
    return {'title': 'Information', 'lesson': lesson}


@view_config(route_name='dep_lesson_info', renderer='../templates/dep_lesson_info.jinja2', permission='view')
def dep_lesson_info(request):
    lesson = LessonService.get_by_id(request)
    return {'title': 'Information', 'lesson': lesson, 'dependent': request.matchdict['dep_id']}


@view_config(route_name='edit_profile', renderer='../templates/edit_username.jinja2', permission='view')
def edit_profile(request):
    form = UpdateUsernameForm(request.POST)
    user = get_user(request, request.authenticated_userid)
    if request.method == 'POST' and form.validate():
        user.username = form.username.data
        return HTTPFound(location=request.route_url('profile', id=request.authenticated_userid))
    return {'title': 'Edit Information', 'user': user, 'form': form}


@view_config(route_name='edit_registration', renderer='../templates/edit_registration.jinja2', permission='view')
def edit_registration(request):
    form = EditRegistrationForm(request.POST)
    dep = DependentService.get_by_id(request)
    if request.method == 'POST' and form.validate():
        update_registration_helper(form, dep)
        # flash(f'Registration updated successfully.', 'success')
        return HTTPFound(location=request.route_url('profile', id=request.authenticated_userid))
    return {'title': 'Edit Dependent Information', 'dep': dep, 'form': form}


def update_registration_helper(form, dep):
    if form.contactNum.data:
        dep.contactNum = form.contactNum.data
    if form.contactEmail.data:
        dep.contactEmail = form.contactEmail.data
    # db.session.commit()

@view_config(route_name='register', renderer='../templates/register.jinja2', permission='view')
def register(request):
    form = RegistrationForm(request.POST)
    lesson = LessonService.get_by_id(request)
    return {'title': 'Register', 'form': form, 'lesson': lesson}


# TODO: look into the commit() method
@view_config(route_name='register_dep', renderer='string', permission='view')
def register_dep(request):
    lesson = LessonService.get_by_id(request)
    user = get_user(request, request.authenticated_userid)
    dependents = user.dependents
    print(dependents)
    dependent = Participant(fName=request.POST.get('fName'), lName=request.POST.get('lName'),
                            contactNum=request.POST.get('contactNum'),
                            contactEmail=request.POST.get('contactEmail'))
    if not dependents:
        user.dependents.append(dependent)
        dependent.lessons.append(lesson)
        request.dbsession.add(dependent)
        return HTTPFound(location=request.route_url('profile', id=request.authenticated_userid))
    elif dependents:
        exists = False
        for dep in dependents:
            if dep.fName == dependent.fName and dep.lName == dependent.lName:
                exists = True
                existingDep = dep
                break
        if exists == True:
            existingDep.lessons.append(lesson)
            return HTTPFound(location=request.route_url('profile', id=request.authenticated_userid))
        else:
            user.dependents.append(dependent)
            dependent.lessons.append(lesson)
            request.dbsession.add(dependent)
            return HTTPFound(location=request.route_url('profile', id=request.authenticated_userid))


@view_config(route_name='register_yourself', renderer='string', permission='view')
def register_yourself(request):
    lesson = LessonService.get_by_id(request)
    user = get_user(request, request.authenticated_userid)
    user.lessons.append(lesson)
    return HTTPFound(location=request.route_url('profile', id=request.authenticated_userid))


@view_config(route_name='unregister_self', renderer='string', permission='view')
def unregister_self(request):
    lesson = LessonService.get_by_id(request)
    current_user = get_user(request, request.authenticated_userid)
    for user in lesson.selfParticipant.all():
        if current_user.id == user.id:
            lesson.selfParticipant.remove(user)
            return HTTPFound(location=request.route_url('profile', id=request.authenticated_userid))
        else:
            continue
    return HTTPFound(location=request.route_url('lesson_info', id=int(request.matchdict['lesson_id'])))


@forbidden_view_config()
def forbidden_view(request):
    next_url = request.route_url('login', _query={'next': request.url})
    return HTTPFound(location=next_url)
