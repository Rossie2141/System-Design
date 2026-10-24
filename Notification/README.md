# Real-Time Notification System using Python

A simple Python project demonstrating three client-server communication techniques: **Short Polling, Long Polling, and WebSockets**, implemented using FastAPI and asynchronous programming.

## Overview

This project implements a real-time notification system using three different approaches to understand how clients receive updates from a server, how HTTP connections behave, and how asynchronous communication improves efficiency.

## Tech Stack

- **Python** — Backend and client implementation
- **FastAPI** — REST APIs and WebSocket endpoints
- **Uvicorn** — ASGI server
- **HTTPX** — HTTP clients for short and long polling
- **WebSockets** — Persistent, bidirectional communication
- **asyncio** — Asynchronous execution and concurrency

## Project Structure

```text
Notification/
├── server/
│   └── main.py
├── clients/
│   ├── short_polling.py
│   ├── long_polling.py
│   └── websocket_client.py
├── requirements.txt
└── README.md
```

## Communication Methods

| Feature | Short Polling | Long Polling | WebSockets |
|---|---|---|---|
| Connection | Repeated HTTP requests | Held-open HTTP requests | Persistent connection |
| Updates | Fixed intervals | When data arrives or timeout occurs | Server pushes instantly |
| Latency | Depends on polling interval | Low | Low |
| Resource usage | Frequent requests | Waiting connections | Persistent connections |
| Use cases | Status checks | Notifications | Chat, live dashboards |

### 1. Short Polling
The client sends HTTP requests every 3 seconds to check for new notifications, even when no new data is available.

### 2. Long Polling
The server holds an HTTP request open for up to 30 seconds until a notification arrives. The client sends another request after receiving a response.

Uses `asyncio.Condition` to notify multiple waiting clients efficiently.

### 3. WebSockets
The client establishes a persistent, bidirectional connection with the server. Notifications are pushed to all connected WebSocket clients without repeated HTTP requests.

## Getting Started

**1. Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

**2. Create and activate a virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies**

```bash
pip install fastapi "uvicorn[standard]" httpx websockets
```

**4. Start the FastAPI server**

```bash
uvicorn server.main:app --reload
```

**5. Run a client in a separate terminal**

Short polling:
```bash
python3 clients/short_polling.py
```

Long polling:
```bash
python3 clients/long_polling.py
```

WebSocket:
```bash
python3 clients/websocket_client.py
```

**6. Generate a notification**

```bash
curl -X POST "http://127.0.0.1:8000/notify?message=Order%20placed"
```

The running clients receive the notification according to their communication method.

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Server health check |
| `/notify` | POST | Create and broadcast a notification |
| `/notifications` | GET | Retrieve notifications for short polling |
| `/long-poll` | GET | Wait for notifications or timeout |
| `/ws` | WebSocket | Persistent real-time communication |

API documentation: `http://127.0.0.1:8000/docs`

## Key Learnings

- HTTP request-response lifecycle
- Short polling vs. long polling
- WebSocket handshake and persistent connections
- Asynchronous programming using `asyncio`
- Broadcasting notifications to multiple clients
- Connection management and timeout handling
- Trade-offs between network traffic, latency, and scalability

## Limitations

This is a learning-focused implementation. Notifications and WebSocket connections are stored in memory. The application does not currently implement persistent storage, authentication, automatic reconnection, or recovery of missed WebSocket messages.

## Future Improvements

- Automatic WebSocket reconnection
- Redis Pub/Sub for multi-instance broadcasting
- Persistent notification storage
- Browser-based real-time dashboard
- Performance testing and benchmarking

---

**Purpose:** To explore and compare real-time communication techniques through hands-on Python implementations.