#!/usr/bin/env python

import os, re, json, subprocess, select
import asyncio
import websockets


async def server(websocket, path):
    if path == '/journalctl':
        print('[INFO] request has reached the path')
        logs = subprocess.Popen(['sudo','journalctl','-fu','sensorproxy'], stdout=subprocess.PIPE)
        p = select.poll()
        p.register(logs.stdout)
        if p.poll(100):
            for line in iter(logs.stdout.readline,''):
                await websocket.send(line.strip().decode('utf-8'))

start_server = websockets.serve(server, '192.168.4.1', 6550)
print('[INFO] Server is Running')
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
