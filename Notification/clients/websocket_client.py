
import asyncio
import json

import websockets

SERVER_URL = "ws://127.0.0.1:8000/ws"


async def main():
    print("Connecting to WebSocket server...")

    try:
        async with websockets.connect(SERVER_URL) as websocket:
            print("WebSocket connected successfully!")

            # Send an initial message to the server
            await websocket.send("Hello from Python client")

            print("Waiting for notifications...\n")

            while True:
                message = await websocket.recv()

                notification = json.loads(message)

                print("-----------------------------")
                print("NEW NOTIFICATION")
                print(f"ID: {notification['id']}")
                print(f"Message: {notification['message']}")
                print(f"Time: {notification['timestamp']}")
                print("-----------------------------")

    except websockets.exceptions.ConnectionClosed:
        print("WebSocket connection closed")

    except OSError as error:
        print(f"Connection error: {error}")


if __name__ == "__main__":
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        print("\nWebSocket client stopped")
