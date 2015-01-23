#!/usr/bin/python

from flask import Flask
from flask.ext.httpauth import HTTPBasicAuth
from dopy.manager import DoManager

app = Flask(__name__)
auth = HTTPBasicAuth()

# IMPORTANT CHANGE THIS
USERNAME = "user"
PASSWORD = "password"
API_TOKEN = "token"
DOMAIN = "sub.domain.com"

users = {
    USERNAME: PASSWORD
}

do = DoManager(None, API_TOKEN, api_version=2)


@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None


def find_a_record_id(domain):
    for record in domain:
        if record['type'] == "A":
            return record["id"]


@app.route("/<ip>")
@auth.login_required
def update_ip(ip):
    return "Updating IP %s" % ip
    domain = do.all_domain_records(DOMAIN)
    a_record_id = find_a_record_id(domain)
    # Currently doesn't work because DO won't let me change a record's IP
    do.edit_domain_record(DOMAIN, a_record_id, "A", ip)


if __name__ == "__main__":
    app.run(port=8000)
