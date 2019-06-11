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

def opticals(request):
    lines = []
    opticals = []

    with open('/pysensorproxy/sensorproxy/sensors/optical.py', 'r') as f:
        for line in f:
            lines.append(line)

    for i in range(len(lines)):
        if "@register_sensor" in lines[i]:
            optical = lines[i+1];
            result = re.search('class (.*)\(', optical)
            opticals.append(result.group(1))
    sensors = dict(opticals=opticals)
    return Response(json.dumps(sensors), content_type='application/json')


if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('sensorproxy_start', '/systemctl/start')
        config.add_route('sensorproxy_stop', '/systemctl/stop')
        config.add_route('opticals', '/opticals')
        config.add_view(sensorproxy_start, route_name="sensorproxy_start")
        config.add_view(sensorproxy_stop, route_name="sensorproxy_stop")
        config.add_view(opticals, route_name="opticals")
        app = config.make_wsgi_app()
    serve(app, host='0.0.0.0', port=6500)


