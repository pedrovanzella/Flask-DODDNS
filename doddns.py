#!/usr/bin/python

from flask import Flask
from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    # IMPORTANT CHANGE THIS USERNAME AND PASSWORD
    "user": "password"
}


@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None


@app.route("/<ip>")
@auth.login_required
def update_ip(ip):
    return "Updating IP %s" % ip


if __name__ == "__main__":
    app.run(port=8000)
