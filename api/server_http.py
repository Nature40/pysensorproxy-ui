from waitress import serve
from pyramid.config import Configurator 
from pyramid.response import Response, FileResponse

import os

def sensorproxy_start(request):
    #os.system('sudo systemctl start sensorproxy')
    return Response('sensorproxy started!')

def sensorproxy_stop(request):
    #os.system('sudo systemctl stop sensorproxy')
    return Response('sensorproxy stopped!')

if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('sensorproxy_start', '/systemctl/start')
        config.add_route('sensorproxy_stop', '/systemctl/stop')
        config.add_view(sensorproxy_start, route_name="sensorproxy_start")
        config.add_view(sensorproxy_stop, route_name="sensorproxy_stop")
        app = config.make_wsgi_app()
    serve(app, host='0.0.0.0', port=6500)


