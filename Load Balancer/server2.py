from flask import Flask

app=Flask(__name__)

@app.route('/')
def home():
    return "Hello, World! from server 2"



app.run(port=5002)