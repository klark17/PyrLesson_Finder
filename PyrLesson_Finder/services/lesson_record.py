from ..models.db_models import Lesson
from ..form import levels
from sqlalchemy import or_


# use this to get search results instead
class LessonService(object):
    @classmethod
    def get_lessons(cls, request):
        level_choice = dict(levels).get(request.POST.get('level'))
        lessons = request.dbsession.query(Lesson).filter(or_(Lesson.location == request.POST.get('location'),
                                                             Lesson.startDate == request.POST.get('startDate'),
                                                             Lesson.startTime == request.POST.get('startTime'),
                                                             Lesson.day == request.POST.get('day'),
                                                             Lesson.level == level_choice)).all()
        return lessons


    @classmethod
    def get_by_id(cls, request):
        lesson_id = int(request.matchdict['lesson_id'])
        lesson = request.dbsession.query(Lesson).get(lesson_id)
        return lesson
