from flask import Flask

app=Flask(__name__)

@app.route('/')
def home():
    return "Hello, World! from server 3"



app.run(port=5003)