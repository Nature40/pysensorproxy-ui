from waitress import serve
from pyramid.config import Configurator 
from pyramid.response import Response, FileResponse
from pyramid.httpexceptions import exception_response

from sensorproxy.sensors import *
from inspect import * 

import os, re, json, subprocess

def sensorproxy_switch(request):
    if request.method == 'POST': 
        if 'state' in json.dumps(request.json):
            switch = request.json['state']
            res = subprocess.Popen(['sudo', 'systemctl', switch, 'sensorproxy'], stdout=subprocess.PIPE)
            res.wait()
            return Response(json.dumps({
                    'status': res.returncode,
                    'message': (
                        'sensorproxy '+
                            ('started' if switch == 'start' else 'stopped' if switch == 'stop' else 'restarted')
                        +'!'
                    ), 
                }), 
                charset='utf-8', 
                content_type='application/json',
                headerlist=[
                    ('Access-Control-Allow-Origin', '*'),
                ]
            )    
        else:
            return Response(json.dumps({
                    'status':-1,
                    'message':"key 'state' is missing"
                }), 
                charset='utf-8', 
                content_type='application/json'
            )
    else: 
        return Response(json.dumps({
                'status': 501,
                'message':'Invalid Method'
            }), 
            status_code=501, 
            charset='utf-8', 
            content_type='application/json'
        )

def list_of_sensors(request):
    if request.method == 'GET':
        sensors = {}

        for sensor in base.classes:
            # print(sensor)
            sensors[sensor] = {}
            for method in base.classes[sensor].__dict__:
                if isfunction(base.classes[sensor].__dict__[method]):
                    arguments = getfullargspec(base.classes[sensor].__dict__[method]).annotations
                    sensors[sensor][method] = {}
                    # print(method)
                    # print(getfullargspec(base.classes[sensor].__dict__[method]).annotations)
                    for argument in arguments:
                        sensors[sensor][method][argument] = arguments[argument].__name__
                        # print(argument)
                        # print(arguments[argument].__name__)

        return Response(json.dumps({
            'sensors': sensors
            }), 
            charset='utf-8', 
            content_type='application/json',
            headerlist=[
                ('Access-Control-Allow-Origin', '*'),
            ]
        )    
    else: 
        return Response(json.dumps({
                'status': 501,
                'message':'Invalid Method'
            }), 
            status_code=501, 
            charset='utf-8', 
            content_type='application/json'
        )

def sensorproxy_yml(request): 
    if request.method == 'GET':
        res = subprocess.Popen(['cat','/boot/sensorproxy.yml'], stdout=subprocess.PIPE)
        res.wait()
        return Response(json.dumps({
                # 'body': "{}".format(res.communicate()[0]),
                'body': (res.communicate()[0]).decode('utf-8'),
                'status': res.returncode
            }), 
            charset='utf-8', 
            headerlist=[
                ('Access-Control-Allow-Origin', '*'),
            ]
        )  
    elif request.method == 'POST':
        if 'body' in request.json:
            f = open("/boot/sensorproxy.yml", "w+")
            f.write(request.json['body'])
            f.close()
            return Response(json.dumps({
                'status': 0,
                'message': 'File successfully overwritten!' 
            }), 
                charset='utf-8', 
                content_type='application/json', 
                headerlist=[
                    ('Access-Control-Allow-Origin', '*')
                ]
            )
        else:
            return Response(json.dumps({
                    'status': -1,
                    'message': "key 'body' is missing"
                }), 
                charset='utf-8', 
                content_type='application/json'
            )
    else:  
        return Response(json.dumps({
                'status': 501,
                'message':'Invalid Method'
            }), 
            status_code=501, 
            charset='utf-8', 
            content_type='application/json'
        )
        
def testpath(request): 
    if request.method == 'GET':
        return Response(json.dumps({
                'method': 'GET',
                'status': 0
            }), 
            charset='utf-8', 
            content_type='application/json'
        )  
    elif request.method == 'POST':
        return Response(json.dumps({
                'method': 'POST',
                'status': 0
            }), 
            charset='utf-8', 
            content_type='application/json'
        )  
    else: 
        return Response(json.dumps({
                'method': request.method,
                'status': 0
            }), 
            charset='utf-8', 
            content_type='application/json'
        )  


if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('testpath', '/testpath')
        config.add_route('sensorproxy_switch', '/systemctl/switch')
        config.add_route('list_of_sensors', '/sensors')
        config.add_route('sensorproxy_yml', '/yml/sensorproxy')
        config.add_view(testpath, route_name='testpath')
        config.add_view(sensorproxy_switch, route_name='sensorproxy_switch')
        config.add_view(list_of_sensors, route_name="list_of_sensors")
        config.add_view(sensorproxy_yml, route_name="sensorproxy_yml")
        app = config.make_wsgi_app()
    serve(app, host='0.0.0.0', port=6500)


