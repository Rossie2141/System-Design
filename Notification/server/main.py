
import asyncio
from datetime import datetime, timezone

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

# Shared in-memory notification storage
notifications = []

# Used by long-polling clients
notification_condition = asyncio.Condition()

# Active WebSocket connections
connected_clients: set[WebSocket] = set()


@app.get("/")
async def home():
    return {"message": "Notification server is running"}


# ---------------------------------
# Create a notification
# ---------------------------------
@app.post("/notify")
async def create_notification(message: str):
    async with notification_condition:
        notification = {
            "id": len(notifications) + 1,
            "message": message,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        notifications.append(notification)

        # Wake all waiting long-polling clients
        notification_condition.notify_all()

    # Push notification to WebSocket clients
    await broadcast_notification(notification)

    return notification


# ---------------------------------
# Short polling
# ---------------------------------
@app.get("/notifications")
async def get_notifications():
    return {"notifications": notifications}


# ---------------------------------
# Long polling
# ---------------------------------
@app.get("/long-poll")
async def long_poll(last_seen_id: int = 0):
    async with notification_condition:
        try:
            await asyncio.wait_for(
                notification_condition.wait_for(
                    lambda: any(
                        n["id"] > last_seen_id
                        for n in notifications
                    )
                ),
                timeout=30
            )

        except asyncio.TimeoutError:
            return {
                "notifications": [],
                "status": "timeout"
            }

        new_notifications = [
            n for n in notifications
            if n["id"] > last_seen_id
        ]

        return {
            "notifications": new_notifications,
            "status": "success"
        }


# ---------------------------------
# WebSocket connection
# ---------------------------------
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    connected_clients.add(websocket)

    print(
        f"WebSocket connected. "
        f"Active clients: {len(connected_clients)}"
    )

    try:
        while True:
            message = await websocket.receive_text()
            print(f"Message from client: {message}")

    except WebSocketDisconnect:
        print("WebSocket client disconnected")

    finally:
        connected_clients.discard(websocket)

        print(
            f"Active WebSocket clients: "
            f"{len(connected_clients)}"
        )


# ---------------------------------
# Broadcast to all WebSocket clients
# ---------------------------------
async def broadcast_notification(notification):
    for client in list(connected_clients):
        try:
            await client.send_json(notification)

        except Exception as error:
            print(f"Broadcast failed: {error}")
            connected_clients.discard(client)
