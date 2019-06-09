#!/usr/bin/env python

# WS server example

import os, re, json
import asyncio
import websockets


async def server(websocket, path):
    print(path)

    if path == '/opticals':
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
        await websocket.send(json.dumps(sensors))
    if path == '/systemd/start':
        os.system('sudo systemctl start sensorproxy')
        await websocket.send('Systemd started!')
    if path == '/systemd/stop':
        os.system('sudo systemctl stop sensorproxy')
        await websocket.send('Systemd stopped!')
    if path == '/journalctl':
        logs = os.popen('journalctl -u sensorproxy').read()
        await websocket.send(logs)
        # await websocket.send('Systemd stopped!')
        # name = await websocket.recv()
        # print(f"S< {name}")
    # greeting = f"{name}"

    # await websocket.send(greeting)
    # print(f"S> {greeting}")

start_server = websockets.serve(server, '0.0.0.0', 6550)
print('server running')
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
