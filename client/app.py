from waitress import serve
from pyramid.config import Configurator
from pyramid.response import Response, FileResponse

import os

here = os.path.dirname(__file__)

def index(request):
    app = os.path.join(here, 'src', 'index.html')
    return FileResponse(app, content_type='text/html')

def appjs(request):
    print(f'app.js {request.url}')
    app = os.path.join(here, 'src', 'app.js')
    return FileResponse(app, content_type='text/javascript')

def vuecomponents(request):
    print(f'components.js {request.url}')
    components = os.path.join(here, 'src', 'components.js')
    return FileResponse(components, content_type='text/javascript')

def notfound(request):
    print(f'NOT FOUND: {request.url}')
    app = os.path.join(here, 'src', 'index.html')
    return FileResponse(app, content_type='text/html')


if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('index', '/')
        config.add_route('appjs', '/app.js')
        config.add_route('vuecomponents', '/components.js')
        config.add_notfound_view(notfound)
        # config.add_static_view(name='static', path='src/app.js')
        config.add_view(appjs, route_name='appjs')
        config.add_view(vuecomponents, route_name='vuecomponents')
        config.add_view(index, route_name='index')
        app = config.make_wsgi_app()
    serve(app, host='10.0.2.15', port=80)