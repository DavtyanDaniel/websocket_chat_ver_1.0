"""this module is implemented for server part."""

import asyncio
import websockets
from aioconsole import ainput, aprint

user_websocket = {}


async def main_1(websocket, path):
    """This is driver code for server"""
    try:
        # Asking for nickname
        await ask_for_nickname(websocket)
        while True:
            # Listing all connected users to the client
            await list_the_connected_users(websocket)
            message = await websocket.recv()
            # If client wants to enter group chat
            if message == f'{user_websocket[websocket]}: GROUP':
                await websocket.send("You are connected to group chat, feel free to chat!\n"
                                     "if you want to change room write 'CHANGE ROOM' command")
                await broadcaster_and_receiver(websocket, 'group')
            else:
                # As we know the nickname of the user we have to know his websocket
                # With the code below we do that
                for socket, nick in user_websocket.items():
                    nick_and_message = message.split(':')  # splitting the nickname and message
                    if nick == nick_and_message[1].strip():
                        await websocket.send(f"You are connected to {nick}")
                        message = await broadcaster_and_receiver(websocket, 'private', socket)
                        if message == f'{user_websocket[websocket]}: CHANGE ROOM':
                            break
    except websockets.exceptions.ConnectionClosedOK:
        del user_websocket[websocket]


async def broadcaster_and_receiver(websocket, group_or_private, second_client_websocket=None):
    """
    The function is broadcasting with broadcast_for_group_chat and sender_for_two_clients functions
    :param websocket: is a current user
    :param group_or_private: is string that user chooses if he wants to broadcast to group or private
    :param second_client_websocket: if we choose private, the param represents the second client
    :return: message
    """
    while True:
        message = await websocket.recv()
        if message == f'{user_websocket[websocket]}: CHANGE ROOM':
            break
        if group_or_private == 'group':
            await broadcast_for_group_chat(message)
        if group_or_private == 'private':
            await sender_for_two_clients(second_client_websocket, message)
    return message


async def ask_for_nickname(websocket):
    """
    Functions asking for nickname from client
    """
    await websocket.send('Please write your nickname')
    await aprint(">>> send")
    name = await websocket.recv()
    user_websocket.update({websocket: name})
    await aprint(f"<<< {name} {websocket}")
    await websocket.send('thanks')


async def list_the_connected_users(websocket):
    """
    Function is sending to the client list of current connected users
    """
    await websocket.send('Here are nicknames of connected users,'
                         'please select with whom you want to connect\n')
    for values in user_websocket.values():
        await websocket.send(f" {values}\n")
    await websocket.send('or enter group chat, typing \'GROUP\'')


async def broadcast_for_group_chat(message):
    """Broadcaster for group chat"""
    for websocket in user_websocket.keys():
        await websocket.send(message)


async def sender_for_two_clients(websocket, message):
    """Broadcaster for 2 clients"""
    await websocket.send(message + ' [Private message]')


async def main():
    """Websocket driver code"""
    async with websockets.serve(main_1, "localhost", 8777):
        await asyncio.Future()

asyncio.run(main())
