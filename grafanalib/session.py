import logging
import sys

import requests

from utils.builder_creds import BuilderCreds


class Session(object):
    cfg = None
    login_url = None
    logout_url = None

    def __init__(self, grafana_url):
        self.creds = BuilderCreds()
        self.cookies = None
        self.login_url = grafana_url + "/login"

    def login(self):
        data = {
            "user": self.creds.username,
            "password": self.creds.get_tool_password(),
        }
        headers = {'Accept': 'application/json, text/plain, */*', 'Content-Type': 'application/json'}
        response = requests.post(self.login_url, json=data, headers=headers, verify=False)
        if response.status_code != 200:
            print(response.__dict__)
            raise(requests.ConnectionError)
        if "grafana_remember" not in response.cookies:
            logging.exception("No cookie returned")
            sys.exit("Invalid username / password. Did not get a cookie returned.")
            
        self.cookies = response.cookies

    def get_cookies(self):
        if self.cookies is None:
            self.login()
        return self.cookies
