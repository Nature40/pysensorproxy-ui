from waitress import serve
from pyramid.config import Configurator
from pyramid.response import Response, FileResponse

import os

here = os.path.dirname(__file__)

def index(request):
    app = os.path.join(here, 'src', 'index.html')
    return FileResponse(app, content_type='text/html')

def app_js(request):
    print('app.js %s' % request.url)
    app = os.path.join(here, 'src', 'app.js')
    return FileResponse(app, content_type='text/javascript')

def components_js(request):
    print('components.js %s' % request.url)
    components = os.path.join(here, 'src', 'components.js')
    return FileResponse(components, content_type='text/javascript')

def app_css(request):
    print('app.css %s' % request.url)
    stylesheet = os.path.join(here, 'src', 'app.css')
    return FileResponse(stylesheet, content_type='text/css')

def notfound(request):
    print('NOT FOUND: %s' % request.url)
    app = os.path.join(here, 'src', 'index.html')
    return FileResponse(app, content_type='text/html')


if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('index', '/')
        config.add_route('app_js', '/app.js')
        config.add_route('components_js', '/components.js')
        config.add_route('app_css', '/app.css')
        config.add_notfound_view(notfound)
        # config.add_static_view(name='static', path='src/app.js')
        config.add_view(app_js, route_name='app_js')
        config.add_view(components_js, route_name='components_js')
        config.add_view(app_css, route_name='app_css')
        config.add_view(index, route_name='index')
        app = config.make_wsgi_app()
    serve(app, host='0.0.0.0', port=80)