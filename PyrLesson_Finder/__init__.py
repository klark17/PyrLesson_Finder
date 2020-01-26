from waitress import serve
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.session import SignedCookieSessionFactory, JSONSerializer
# from .security import groupfinder
from .session import JSONSerializerWithPickleFallback


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    # with Configurator(settings=settings) as config:
    #     config.include('pyramid_jinja2')
    #     config.include('.models')
    #     config.include('.routes')
    #
    #     # Security policies
    #     authn_policy = AuthTktAuthenticationPolicy(
    #         settings['PyrLesson_Finder.secret'], callback=groupfinder,
    #         hashalg='sha512')
    #     authz_policy = ACLAuthorizationPolicy()
    #     config.set_authentication_policy(authn_policy)
    #     config.set_authorization_policy(authz_policy)
    #
    #     config.scan()
    # return config.make_wsgi_app()


def main(global_config, **settings):
    serializer = JSONSerializerWithPickleFallback
    factory = SignedCookieSessionFactory('jfagfjslfasdf',
                                         secure=True,
                                         httponly=True,
                                         serializer=serializer)
    with Configurator(settings=settings) as config:
        config.set_session_factory(factory)
        config.include('.models')
        config.include('pyramid_jinja2')
        config.include('.routes')
        config.include('.security')
        config.scan()
        app = config.make_wsgi_app()
        return app
    # serve(app, host='0.0.0.0', port=6543)
