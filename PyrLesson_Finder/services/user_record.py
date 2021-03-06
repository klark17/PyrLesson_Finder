from ..models.db_models import User

# use this to get search results instead
class UserService(object):
    @classmethod
    def by_id(cls, _id, request):
        query = request.dbsession.query(User)
        return query.get(_id)

    @classmethod
    def by_username(cls, username, request):
        return request.dbsession.query(User).filter(User.username == username).first()

    @classmethod
    def by_email(cls, email, request):
        return request.dbsession.query(User).filter(User.email == email).first()
