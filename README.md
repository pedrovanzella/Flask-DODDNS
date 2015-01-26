===============
Flask-DODDNS
===============

A Dynamic DNS updater for the Digital Ocean v2 API in Flask

*Status*: Working


## Quickstart Guide
* Edit doddns.py to use a APIv2 token
* Change username and password
* Add a domain name to Digital Ocean's Control panel (a subdomain works too)
* Run doddns.py on a VPS. Preferably, do so as a service. Don't forget to `pip install < requirements.txt`
* You might want to use nginx as a proxy, although that's not necessary
* Now point your home router's ddns settings to your VPS. It should monitor the
response `Updated IP %IP%`.
