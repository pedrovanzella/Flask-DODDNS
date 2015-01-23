#!/usr/bin/python

from flask import Flask
from flask.ext.httpauth import HTTPBasicAuth
from dopy.manager import DoManager

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    # IMPORTANT CHANGE THIS USERNAME AND PASSWORD
    "user": "password"
}

do = DoManager(None, 'api_token', api_version=2)


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
