from waitress import serve
from pyramid.config import Configurator 
from pyramid.response import Response, FileResponse
from pyramid.httpexceptions import exception_response

import os, re, json, subprocess

def sensorproxy_switch(request):
    if request.method == 'POST': 
        if 'state' in request.json:
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
                content_type='application/json'
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
"""
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
    return Response(json.dumps({
        'opticals': opticals
    }), charset='utf-8', content_type="application/json", headerlist=[
            ('Access-Control-Allow-Origin', '*'),
        ])
"""
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
            return Response(json.dumps(request.json), 
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
        # config.add_route('opticals', '/opticals')
        config.add_route('sensorproxy_yml', '/sensorproxy_yml')
        config.add_view(testpath, route_name='testpath')
        config.add_view(sensorproxy_switch, route_name='sensorproxy_switch')
        # config.add_view(opticals, route_name="opticals")
        config.add_view(sensorproxy_yml, route_name="sensorproxy_yml")
        app = config.make_wsgi_app()
    serve(app, host='0.0.0.0', port=6500)


