# !/usr/bin/env python
#  coding=utf-8
import base64
import os
import re


""" Builder Creds"""


class BuilderCreds(object):
    def __init__(self, env_name = "test", creds_path=None):
        self.session = None
        self.username = None
        self.ldap_pwd = None
        self.local_pwd = None
        self.grafana_api_key = None

        creds_file = creds_path or os.path.join(os.path.expanduser("~"), ".python", "builder.creds")
        with open(creds_file) as f:
            lines = f.readlines()
        for l in lines:
            mu = re.search("^username=(.*)", l)
            mlp = re.search("^ldap_password=(.*)", l)
            mtp = re.search("^local_password=(.*)", l)
            grafana_api_key = re.search("^" + env_name + "_grafana_api_key=(.*)", l)

            if mu is not None:
                self.username = str(mu.group(1))
            elif mlp is not None:
                self.ldap_pwd = str(mlp.group(1))
            elif mtp is not None:
                self.local_pwd = str(mtp.group(1))
            elif grafana_api_key is not None:
                self.grafana_api_key = grafana_api_key.group(1)

    def get_username(self):
        return self.username

    def get_ldap_password(self):
        return self.ldap_pwd
