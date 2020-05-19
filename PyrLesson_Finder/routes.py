def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('about', '/')
    config.add_route('signup', '/signup')
    config.add_route('login', '/login')
    config.add_route('auth', '/auth/{action}')
    config.add_route('search', '/search')
    config.add_route('results', '/search/results')
    config.add_route('register', '/search/results/{lesson_id}/register', factory='PyrLesson_Finder.security.UserFactory')
    config.add_route('register_yourself', '/search/results/{lesson_id}/register_self', factory='PyrLesson_Finder.security.UserFactory')
    config.add_route('register_dep', '/search/results/{lesson_id}/register_dep/', factory='PyrLesson_Finder.security.UserFactory')
    config.add_route('profile', '/profile', factory='PyrLesson_Finder.security.UserFactory')
    config.add_route('edit_profile', '/profile/{id}/edit', factory='PyrLesson_Finder.security.UserFactory')
    config.add_route('change', '/profile/change/{id}', factory='PyrLesson_Finder.security.UserFactory')
    config.add_route('lesson_info', '/lesson/info/{lesson_id}', factory='PyrLesson_Finder.security.UserFactory')
    config.add_route('dep_lesson_info', '/lesson/{lesson_id}/dep_info/{dep_id}', factory='PyrLesson_Finder.security.UserFactory')
    config.add_route('edit_registration', '/lesson/edit/{dep_id}', factory='PyrLesson_Finder.security.UserFactory')
    config.add_route('unregister_self', '/lesson/{lesson_id}/unregister/', factory='PyrLesson_Finder.security.UserFactory')
    config.add_route('unregister_dep', '/lesson/{lesson_id}/unregister/{dep_id}/', factory='PyrLesson_Finder.security.UserFactory')


