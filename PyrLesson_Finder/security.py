from pyramid.security import Allow, Everyone, Authenticated
from pyramid.authentication import AuthTktAuthenticationPolicy
from .models import User

class UserFactory(object):
    __acl__ = [(Allow, Everyone, 'read'),
               (Allow, Authenticated, 'view'),
               (Allow, Authenticated, 'edit'), ]

    def __init__(self, request):
        pass


class MyAuthPolicy(AuthTktAuthenticationPolicy):
    def authenticated_userid(self, request):
        user = request.user
        if user is not None:
            return user.id


def get_user(request):
    user_id = request.unauthenticated_userid
    if user_id is not None:
        user = request.dbsession.query(User).get(user_id)
        return user


def includeme(config):
    settings = config.get_settings()
    auth_policy = MyAuthPolicy(settings['PyrLesson_Finder.secret'], hashalg='sha512')
    config.set_authentication_policy(auth_policy)
    config.add_request_method(get_user, 'user', reify=True)
