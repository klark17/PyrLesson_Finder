from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory, JSONSerializer
from pyramid.csrf import SessionCSRFStoragePolicy
from .session import JSONSerializerWithPickleFallback
from .security import MyAuthPolicy


def main(global_config, **settings):
    serializer = JSONSerializer
    factory = SignedCookieSessionFactory('jfagfjslfasdf',
                                         secure=True,
                                         httponly=True,
                                         serializer=serializer)
    authorization_policy = ACLAuthorizationPolicy()
    with Configurator(settings=settings,
                      authorization_policy=authorization_policy,
                      session_factory=factory) as config:
        # config.set_csrf_storage_policy(SessionCSRFStoragePolicy())
        # config.set_default_csrf_options(require_csrf=True)
        config.include('.security')
        config.include('.models')
        config.include('pyramid_jinja2')
        config.include('.routes')
        config.scan()
        app = config.make_wsgi_app()
        return app
