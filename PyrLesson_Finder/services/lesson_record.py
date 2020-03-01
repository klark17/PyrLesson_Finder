import sqlalchemy as sa
# from paginate_sqlalchemy import SqlalchemyOrmPage #<- provides pagination
from ..models.db_models import Lesson
from ..form import levels
from sqlalchemy import or_


# use this to get search results instead
class LessonService(object):
    @classmethod
    def get_lessons(cls, request):
        level_choice = dict(levels).get(request.POST.get('level'))
        lessons = request.dbsession.query(Lesson).filter(or_(Lesson.location == request.POST.get('location'),
                                                             Lesson.organizationId == request.POST.get(
                                                                 'organizationId'),
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


    @classmethod
    def get_paginator(cls, request, page=1):
        query = request.dbsession.query(Lesson)
        query = query.order_by(sa.desc(Lesson.created))
        query_params = request.GET.mixed()

        def url_maker(link_page):
            # replace page param with values generated by paginator
            query_params['page'] = link_page
            return request.current_route_url(_query=query_params)

        return SqlalchemyOrmPage(query, page, items_per_page=5,
                                 url_maker=url_maker)