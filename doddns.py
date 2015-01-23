from flask import Flask
from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()


@app.route("/")
def hello():
    return "Hello, World"


if __name__ == "__main__":
    app.run(port=8000)
