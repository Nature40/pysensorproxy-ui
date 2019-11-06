import tornado.ioloop
import tornado.web
import tornado.websocket

from sensorproxy.sensors import *
from inspect import * 

import os, json, datetime, subprocess

class MainHandler(tornado.web.RequestHandler):
  def get(self):
    res = subprocess.Popen(['cat','/pysensorproxy-ui/index.html'], stdout=subprocess.PIPE)
    res.wait()
    self.set_header("Access-Control-Allow-Origin", "*")
    self.write((res.communicate()[0]).decode('utf-8'))

class YamlEditHandler(tornado.web.RequestHandler):
  def get(self):
    res = subprocess.Popen(['cat','/boot/sensorproxy.yml'], stdout=subprocess.PIPE)
    res.wait()
    self.set_header("Access-Control-Allow-Origin", "*")
    self.write({
      'body': (res.communicate()[0]).decode('utf-8'),
      'status': res.returncode
    })
  def post(self):
    payload = json.loads(self.request.body.decode("utf-8"))
    if 'body' in payload: 
      # os.chmod("/boot/sensorproxy.yml", stat.S_IWOTH)
      f = open("/boot/sensorproxy.yml", "w+")
      f.write(payload['body'])
      self.write({
        'status': 0,
        'message': 'File successfully overwritten!' 
      })
    else:
      self.write({
        'status': -1,
        'message': "key 'body' is missing"
      })

class SensorsDetailsHandler(tornado.web.RequestHandler):
  def get(self):
    sensors = {}

    for sensor in base.classes:
      # print(sensor)
      sensors[sensor] = {}
      sensor_dict = base.classes[sensor].__dict__
      for method in sensor_dict:
        if isfunction(sensor_dict[method]):
          args = getfullargspec(sensor_dict[method]).annotations
          sensors[sensor][method] = {}
          # print(method)
          # print(getfullargspec(base.classes[sensor].__dict__[method]).annotations)
          for arg_name in args:
            arg = args[arg_name]
            if type(arg) is list:
              sensors[sensor][method][arg_name] = arg[0].__name__ 
            else:   
              sensors[sensor][method][arg_name] = arg.__name__  
                  # print(argument)
                  # print(arguments[argument].__name__
    self.set_header("Access-Control-Allow-Origin", "*")
    self.write({
      'sensors': sensors
    })

class SensorSwitchHandler(tornado.web.RequestHandler):
  def post(self): 
    payload = json.loads(self.request.body.decode("utf-8"))
    if 'state' in payload:
      switch = payload['state']
      res = subprocess.Popen(
        ['sudo', 'systemctl', switch, 'sensorproxy'], 
        stdout=subprocess.PIPE
      )
      res.wait()
      self.set_header("Access-Control-Allow-Origin", "*")
      self.write({
        'status': res.returncode,
        'message': ('sensorproxy '+
          ('started' 
            if switch == 'start' 
              else 'stopped' 
            if switch == 'stop' 
              else 'restarted'
          ) +'!'
        ), 
      })
    else: 
      self.write({
        'status':-1,
        'message':"key 'state' is missing"
      })

class SimpleWebSocket(tornado.websocket.WebSocketHandler):
  connections = set()

  def check_origin(self, origin):
    return True

  def open(self):
    now = datetime.datetime.now()
    self.write_message(now.strftime('\n-- Logs begin at %a %Y-%m-%d %H:%M:%S CET. --\n'))
    self.connections.add(self)

  def on_message(self, message):
    [client.write_message(message) for client in self.connections]

  def on_close(self):
    self.connections.remove(self)
 
def make_app():
  return tornado.web.Application(
    handlers=[
      (r"/", MainHandler),
      (r"/logs", MainHandler),
      (r"/sensors", SensorsDetailsHandler),
      (r"/yml/sensorproxy", YamlEditHandler),
      (r"/systemctl/switch", SensorSwitchHandler),
      (r"/js/(.*\.js)", tornado.web.StaticFileHandler,{"path": os.path.join(os.path.dirname(__file__), 'assets/js') }),
      (r"/css/(.*\.css)", tornado.web.StaticFileHandler,{"path": os.path.join(os.path.dirname(__file__), 'assets/css') }),
      (r"/journalctl", SimpleWebSocket)
    ])

if __name__ == "__main__":
  app = make_app()
  app.listen(6550, '192.168.4.1')
  tornado.ioloop.IOLoop.current().start()