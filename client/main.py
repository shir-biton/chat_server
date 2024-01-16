import asyncio
import os

import httpx

BASE_URL = os.getenv("SERVER_URL", "http://localhost:8000")


async def post_message(sender: str, message: str, room: str) -> dict:
    url = f"{BASE_URL}/message"
    data = {"sender": sender, "message": message, "room": room}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, follow_redirects=True)
        response.raise_for_status()
        return response.json()


async def get_messages(room: str) -> dict:
    url = f"{BASE_URL}/message/{room}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()


async def print_messages(room: str) -> None:
    while True:
        messages = await get_messages(room)
        if messages:
            print("Messages:")
            for msg in messages:
                print(f"{msg['sender']}: {msg['message']}")
        await asyncio.sleep(1)


async def chat_client(username: str, room: str) -> None:
    print_task = asyncio.create_task(print_messages(room))

    while True:
        message = input("Enter your message: ")
        if message.lower() == 'exit':
            break
        await post_message(username, message, room)

    print_task.cancel()


def main():
    username = input("Enter your username: ")
    room = input("Enter the room to connect to: ")

    asyncio.run(chat_client(username, room))


if __name__ == "__main__":
    main()
