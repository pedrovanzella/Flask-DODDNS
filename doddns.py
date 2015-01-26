#!/usr/bin/python

from flask import Flask
from flask.ext.httpauth import HTTPBasicAuth
import requests

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


@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None


def get(url):
    url = 'https://api.digitalocean.com/v2' + url
    headers = {'Authorization': "Bearer %s" % API_TOKEN}
    resp = requests.get(url, headers=headers, timeout=60)
    return resp.json()


def put(url, params={}):
    url = 'https://api.digitalocean.com/v2' + url
    headers = {'Authorization': "Bearer %s" % API_TOKEN}
    resp = requests.put(url, headers=headers, params=params, timeout=60)
    return resp.json()


def all_records(domain):
    json = get('/domains/%s/records/' % DOMAIN)
    return json['domain_records']


def find_a_record_id(records):
    for record in records:
        if record['type'] == "A":
            return record["id"]


def edit_record(domain, record_id, ip):
    params = {}
    params['data'] = ip
    put('/domains/%s/records/%s' % (domain, record_id), params=params)


@app.route("/<ip>")
@auth.login_required
def update_ip(ip):
    return "Updating IP %s" % ip
    records = all_records(DOMAIN)
    record = find_a_record_id(records)
    # Currently doesn't work because DO won't let me change a record's IP
    edit_record(DOMAIN, record, ip)


if __name__ == "__main__":
    app.run(port=8000)
