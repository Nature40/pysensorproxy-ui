#!/usr/bin/env python

# WS client example

import asyncio
import websockets

async def hello():
    async with websockets.connect('ws://localhost:8765/systemd/stop') as websocket:
        # name = input("What's your name? ")
        # await websocket.send('HI SERVER!')
        # print(f"C> {name}")
        result = await websocket.recv()
        print(f"{result}")

asyncio.get_event_loop().run_until_complete(hello())