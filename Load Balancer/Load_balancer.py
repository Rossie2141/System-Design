from flask import Flask
import requests

app=Flask(__name__)

servers=[
    "http://127.0.0.1:5001",
    "http://127.0.0.1:5002",
    "http://127.0.0.1:5003"
]

index=0

def get_server():
    global index

    server=servers[index]
    index=(index+1)%len(servers)

    return server

@app.route("/")
def balance():

    server=get_server()
    response=requests.get(server)

    return response.text

app.run(port=8000)