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


# Taken from dopy https://github.com/devo-ps/dopy/blob/master/dopy/manager.py
def request(self, path, params={}, method='GET'):
    if not path.startswith('/'):
        path = '/' + path
        url = "https://api.digitalocean.com/v2" + path

    headers = {'Authorization': "Bearer %s" % API_TOKEN}
    resp = self.request_v2(url, params=params, headers=headers, method=method)

    return resp


def request_v2(self, url, headers={}, params={}, method='GET'):
    try:
        if method == 'POST':
            resp = requests.post(url, params=params, headers=headers, timeout=60)
            json = resp.json()
        elif method == 'DELETE':
            resp = requests.delete(url, headers=headers, timeout=60)
            json = {'status': resp.status_code }
        elif method == 'PUT':
            resp = requests.put(url, headers=headers, params=params, timeout=60)
            json = resp.json()
        elif method == 'GET':
            resp = requests.get(url, headers=headers, params=params, timeout=60)
            json = resp.json()
        else:
            print 'Unsupported method %s' % method

    except ValueError:  # requests.models.json.JSONDecodeError
        raise ValueError("The API server doesn't respond with a valid json")
    except requests.RequestException as e:  # errors from requests
        raise RuntimeError(e)

        if resp.status_code != requests.codes.ok:
            if json:
                if 'error_message' in json:
                    print json['message']
                elif 'message' in json:
                    print json['message']
            # The JSON reponse is bad
            resp.raise_for_status()

        if json.get('id') == 'not_found':
            print json['message']

        return json


def all_records(domain):
    return ""


def find_a_record_id(records):
    for record in records:
        if record['type'] == "A":
            return record["id"]


def edit_record(domain, record_id, ip):
    pass


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
