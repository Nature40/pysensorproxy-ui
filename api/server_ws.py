import tornado.ioloop
import tornado.web
import tornado.websocket

import datetime


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
  return tornado.web.Application([
    (r"/journalctl", SimpleWebSocket)
  ])
 
if __name__ == "__main__":
  app = make_app()
  app.listen(6550, '192.168.4.1')
  tornado.ioloop.IOLoop.current().start()