import asyncio
import json
import os

import websockets

BASE_WS_URL = f"ws://{os.getenv('SERVER_HOST', '127.0.0.1')}:{os.getenv('SERVER_PORT', 8000)}/ws"


async def send_message(data: dict, websocket) -> None:
    await websocket.send(json.dumps(data))


async def print_messages(chat_connection_url: str) -> None:
    async with websockets.connect(chat_connection_url) as websocket:
        while True:
            try:
                message = await websocket.recv()
                print(message)
            except websockets.ConnectionClosed:
                print("WebSocket connection closed.")
                break


async def chat_client(username: str, room: str) -> None:
    chat_connection_url = f"{BASE_WS_URL}/{room}/{username}"
    receive_task = asyncio.create_task(print_messages(chat_connection_url))

    async with websockets.connect(chat_connection_url) as websocket:
        while True:
            try:
                message = input("Enter your message: (write exit to quite")
                if message.lower() == 'exit':
                    break
                data = {"sender": username, "message": message, "room": room}
                await send_message(data=data, websocket=websocket)
                await asyncio.sleep(1)
            except websockets.ConnectionClosed:
                print("WebSocket connection closed.")
                break

    receive_task.cancel()


def main():
    username = input("Enter your username: ")
    room = input("Enter the room to connect to: ")

    asyncio.run(chat_client(username, room))


if __name__ == "__main__":
    main()
