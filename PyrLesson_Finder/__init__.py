from waitress import serve
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.response import Response
from .security import groupfinder

#
# def main(global_config, **settings):
#     """ This function returns a Pyramid WSGI application.
#     """
#     with Configurator(settings=settings) as config:
#         config.include('pyramid_jinja2')
#         config.include('.models')
#         config.include('.routes')
#
#         # Security policies
#         authn_policy = AuthTktAuthenticationPolicy(
#             settings['PyrLesson_Finder.secret'], callback=groupfinder,
#             hashalg='sha512')
#         authz_policy = ACLAuthorizationPolicy()
#         config.set_authentication_policy(authn_policy)
#         config.set_authorization_policy(authz_policy)
#
#         config.scan()
#     return config.make_wsgi_app()

# def main(global_config, **settings):
#     with Configurator(settings=settings) as config:
#         config.include('PyrLesson_Finder.models')
#         config.include('pyramid_jinja2')
#         config.include('PyrLesson_Finder.routes')
#         config.scan()
#         app = config.make_wsgi_app()
#     serve(app, host='0.0.0.0', port=6543)
