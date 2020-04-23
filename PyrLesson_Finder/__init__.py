from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory, JSONSerializer
from pyramid.csrf import SessionCSRFStoragePolicy
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
                      authorization_policy=authorization_policy) as config:
        config.set_session_factory(factory)
        config.set_csrf_storage_policy(SessionCSRFStoragePolicy())
        # config.set_default_csrf_options(require_csrf=True)
        config.include('.models')
        config.include('pyramid_jinja2')
        config.include('.routes')
        config.scan()
        app = config.make_wsgi_app()
        return app
