from flask import Flask, request
import requests
import threading
import time
import random

app = Flask(__name__)

servers = [
    {"url": "http://127.0.0.1:5001", "status": True, "connections": 0},
    {"url": "http://127.0.0.1:5002", "status": True, "connections": 0},
    {"url": "http://127.0.0.1:5003", "status": True, "connections": 0}
]

index = 0

def check_servers():
    while True:
        for server in servers:
            try:
                response = requests.get(server["url"], timeout=2)

                if response.status_code == 200:
                    server["status"] = True
                else:
                    server["status"] = False

            except:
                server["status"] = False

        time.sleep(5)


threading.Thread(target=check_servers, daemon=True).start()

def healthy_servers():
    available = []

    for server in servers:
        if server["status"]:
            available.append(server)

    return available

def round_robin():
    global index

    available = healthy_servers()

    if len(available) == 0:
        return None

    server = available[index]

    index = (index + 1) % len(available)

    return server

def least_connections():
    available = healthy_servers()

    if len(available) == 0:
        return None

    server = available[0]

    for s in available:
        if s["connections"] < server["connections"]:
            server = s

    return server


def random_server():
    available = healthy_servers()

    if len(available) == 0:
        return None

    return random.choice(available)


@app.route("/")
def balance():

    algo = request.args.get("algo", "round")

    if algo == "least":
        server = least_connections()

    elif algo == "random":
        server = random_server()

    else:
        server = round_robin()

    if server is None:
        return "No active servers"

    try:
        server["connections"] += 1

        response = requests.get(server["url"])

        return response.text

    except:
        server["status"] = False
        return "Server is down"

    finally:
        server["connections"] -= 1


app.run(port=8000)