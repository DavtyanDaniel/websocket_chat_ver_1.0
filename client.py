"""This module is implementation of client part"""

import websockets
import asyncio
from aioconsole import ainput, aprint

uri = "ws://localhost:8777"

nickname = input('Please write your nickname? ')


async def receiver(websocket):
    """listener for client"""
    global nickname
    while True:
        message = await websocket.recv()
        if message == 'Please write your nickname':
            await websocket.send(nickname)
        else:
            await aprint(message)


async def write(websocket):
    """Writer for client"""
    global nickname
    while True:
        message = f'{nickname}: {await ainput()}'
        await websocket.send(message)


async def main():
    """Driver code for client module"""
    async with websockets.connect(uri) as websocket:
        task1 = asyncio.create_task(receiver(websocket))
        task2 = asyncio.create_task(write(websocket))
        await task1
        await task2

asyncio.run(main())
