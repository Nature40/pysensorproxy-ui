#!/usr/bin/env python

# WS server example

import os
import asyncio
import websockets

async def server(websocket, path):

	print(path)

	if path == '/systemd/start':
		await websocket.send('Systemd started!')
	if path == '/systemd/stop':
		await websocket.send('Systemd stopped!')
	if path == '/journalctl':
		logs = os.popen('journalctl').read()
		await websocket.send(logs)
		# await websocket.send('Systemd stopped!')
		# name = await websocket.recv()
		# print(f"S< {name}")
    # greeting = f"{name}"

    # await websocket.send(greeting)
    # print(f"S> {greeting}")

start_server = websockets.serve(server, '10.0.2.15', 6550)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()