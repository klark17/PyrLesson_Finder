from ..models.db_models import Participant

# use this to get search results instead
class DependentService(object):

    @classmethod
    def get_by_id(cls, request):
        dep_id = int(request.matchdict['dep_id'])
        dependent = request.dbsession.query(Participant).get(dep_id)
        return dependent
