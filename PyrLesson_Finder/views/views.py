from pyramid.response import Response
from pyramid.view import view_config


@view_config(route_name='signup', renderer='../templates/signup.jinja2')
def signup(request):
    return {}


@view_config(route_name='login', renderer='../templates/login.jinja2')
def login(request):
    return {}


@view_config(route_name='search', renderer='../templates/search.jinja2')
def search(request):
    return {}

# First view, available at http://localhost:6543/
# @view_config(route_name='home')
# def home(request):
#     return Response('<body>Visit <a href="/howdy">hello</a></body>')
#
#
# # /howdy
# @view_config(route_name='hello')
# def hello(request):
#     return Response('<body>Go back <a href="/">home</a></body>')