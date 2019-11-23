def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('about', '/')
    config.add_route('signup', '/signup')
    config.add_route('login', '/login')
    config.add_route('search', '/search')
    config.add_route('profile', '/profile')
# from pyramid.response import Response
#
# def hello_world(request):
#     print('Incoming request')
#     return Response('<body><h1>Hello World!</h1></body>')