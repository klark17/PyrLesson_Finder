from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory, JSONSerializer
from .session import JSONSerializerWithPickleFallback
from .security import MyAuthPolicy


def main(global_config, **settings):
    serializer = JSONSerializer
    factory = SignedCookieSessionFactory('randomstring',
                                         secure=True,
                                         httponly=True,
                                         serializer=serializer)
    authorization_policy = ACLAuthorizationPolicy()
    with Configurator(settings=settings,
                      authorization_policy=authorization_policy,
                      session_factory=factory) as config:
        config.include('.security')
        config.include('.models')
        config.include('pyramid_jinja2')
        config.include('.routes')
        config.scan()
        app = config.make_wsgi_app()
        return app
