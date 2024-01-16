import os
import threading
import time

import httpx

BASE_URL = os.getenv("SERVER_URL", "http://localhost:8000")


def post_message(username: str, message: str) -> dict:
    url = f"{BASE_URL}/message"
    data = {"username": username, "message": message}

    with httpx.Client() as client:
        response = client.post(url, json=data, follow_redirects=True)
        response.raise_for_status()
        return response.json()


def get_messages(username: str) -> dict:
    url = f"{BASE_URL}/message/{username}"

    with httpx.Client() as client:
        response = client.get(url)
        response.raise_for_status()
        return response.json()


def print_messages(username: str) -> None:
    while True:
        messages = get_messages(username)
        if messages:
            print("Messages:")
            for msg in messages:
                print(f"{msg['username']}: {msg['message']}")
        time.sleep(1)


def chat_client(username: str) -> None:
    print_thread = threading.Thread(target=print_messages, args=(username,), daemon=True)
    print_thread.start()

    while True:
        message = input("Enter your message (type 'exit' to quit): ")
        if message.lower() == 'exit':
            break
        post_message(username, message)


def main():
    while True:
        username = input("Enter your username (type 'exit' to quit): ")
        if username.lower() == 'exit':
            break
        threading.Thread(target=chat_client, args=(username,), daemon=True).start()


if __name__ == "__main__":
    main()
