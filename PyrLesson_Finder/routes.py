def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    # config.add_route('home', '/')
    config.add_route('about', '/')
# from pyramid.response import Response
#
# def hello_world(request):
#     print('Incoming request')
#     return Response('<body><h1>Hello World!</h1></body>')