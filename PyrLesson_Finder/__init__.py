from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory, JSONSerializer
from .session import JSONSerializerWithPickleFallback


def main(global_config, **settings):
    serializer = JSONSerializerWithPickleFallback
    factory = SignedCookieSessionFactory('jfagfjslfasdf',
                                         secure=True,
                                         httponly=True,
                                         serializer=serializer)
    authentication_policy = AuthTktAuthenticationPolicy('PyrLesson_Finder.secret')
    authorization_policy = ACLAuthorizationPolicy()
    with Configurator(settings=settings,
                      authentication_policy=authentication_policy,
                      authorization_policy=authorization_policy,
                      session_factory=factory) as config:
        config.include('.models')
        config.include('pyramid_debugtoolbar')
        config.include('pyramid_jinja2')
        config.include('.routes')
        config.scan()
        app = config.make_wsgi_app()
        return app
