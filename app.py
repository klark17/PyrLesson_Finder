from waitress import serve
from pyramid.config import Configurator
from pyramid.response import Response

# TODO: Get the python app.py command to work
def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('about', '/')
    config.add_route('signup', '/signup')
    config.add_route('login', '/login')
    config.add_route('search', '/search')
    config.add_route('profile', '/profile')


def main(global_config, **settings):
    with Configurator(settings=settings) as config:
        config.include('PyrLesson_Finder.models')
        config.include('pyramid_jinja2')
        config.include('PyrLesson_Finder.routes.includeme')
        config.scan()
        app = config.make_wsgi_app()
    return app
    serve(app, host='0.0.0.0', port=6543)