from pyramid.security import Allow, Everyone, Authenticated


# TODO: read this -- https://docs.pylonsproject.org/projects/pyramid/en/latest/narr/security.html#creating-your-own-authentication-policy
class UserFactory(object):
    __acl__ = [(Allow, Everyone, 'read'),
               (Allow, Authenticated, 'view'),
               (Allow, Authenticated, 'edit'), ]

    def __init__(self, request):
        pass