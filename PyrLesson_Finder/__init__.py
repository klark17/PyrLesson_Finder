from pyramid.config import Configurator
# from PyrLesson_Finder import routes

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        config.include('pyramid_jinja2')
        config.include('.models')
        config.include('.routes')
        config.scan()
    return config.make_wsgi_app()

# def main(global_config, **settings):
#     with Configurator(settings=settings) as config:
#         config.include('PyrLesson_Finder.models')
#         config.include('pyramid_jinja2')
#         config.include('PyrLesson_Finder.routes')
#         config.scan()
#         app = config.make_wsgi_app()
