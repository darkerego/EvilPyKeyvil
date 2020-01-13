#!/usr/bin/env python3

# WS server example
import asyncio
import time

import websockets


async def handle_msg(websocket, path=None):
    while True:
        try:
            data = await websocket.recv()
            print(f"{data}")
            time.sleep(0.0625)
        except websockets.exceptions.ConnectionClosedError:
            pass


start_server = websockets.serve(handle_msg, "localhost", 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
