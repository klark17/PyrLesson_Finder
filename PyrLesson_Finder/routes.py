def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('about', '/')
    config.add_route('signup', '/signup')
    config.add_route('login', '/login')
    config.add_route('auth', '/auth/{action}')
    config.add_route('search', '/search')
    config.add_route('results', '/search/results')
    config.add_route('register', '/search/results/{id}/register', factory='PyrLesson_Finder.security.UserFactory')
    config.add_route('profile', '/profile/{id}', factory='PyrLesson_Finder.security.UserFactory')
    config.add_route('edit_profile', '/profile/{id:\d+}/{action}', factory='PyrLesson_Finder.security.UserFactory')
    config.add_route('lesson_info', '/lesson/info/{lesson_id}', factory='PyrLesson_Finder.security.UserFactory')
    config.add_route('dep_lesson_info', '/lesson/dep_info/{lesson_id}', factory='PyrLesson_Finder.security.UserFactory')

