import asyncio
import websockets
import subprocess
import select

async def worker():
  uri = "ws://192.168.4.1:6550/journalctl"
  async with websockets.connect(uri) as websocket:
    logs = subprocess.Popen(['sudo','journalctl','-fu','sensorproxy'], stdout=subprocess.PIPE)
    p = select.poll()
    p.register(logs.stdout)
    if p.poll(100):
      for line in iter(logs.stdout.readline,''):
        await websocket.send(line.strip().decode('utf-8'))

asyncio.get_event_loop().run_until_complete(worker())