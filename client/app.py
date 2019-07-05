from waitress import serve
from pyramid.config import Configurator
from pyramid.response import Response, FileResponse
from pyramid.static import static_view
import os

here = os.path.dirname(__file__)
 
def index(request):
    app = os.path.join(here, 'src', 'index.html')
    return FileResponse(app, content_type='text/html')

def notfound_view(request):
    print('NOT FOUND: %s' % request.url)
    app = os.path.join(here, 'src', 'index.html')
    return FileResponse(app, content_type='text/html')

def favicon_view(request):
    icon = os.path.join(here, 'src', 'favicon.ico')
    return FileResponse(icon, request=request)

if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('index', '/')
        config.add_route('favicon', '/favicon.ico')
        config.add_notfound_view(notfound_view)
        config.add_static_view(name='js', path='/pysensorproxy-ui/client/src/js')
        config.add_static_view(name='css', path='/pysensorproxy-ui/client/src/css')
        # config.add_static_view(name='static', path='src/app.js')
        config.add_view(index, route_name='index')
        config.add_view(favicon_view, route_name='favicon')
        app = config.make_wsgi_app()
    serve(app, host='0.0.0.0', port=800)
