import requests
import colorama
import pdb
import pprint
import sys
import jinja2
import json
from grafanalib.grafana_dashboard import GrafanaDashboard
from grafanalib.session import Session
from utils.builder_creds import BuilderCreds

class Grafana(object):
    session = None
    dashboards = {}

    def __init__(self, env_name="test", grafana_url = "http://ts1mtick-04.m3.ebay.com:3000"):
        self = self
        self.url = grafana_url
        self.session = Session(self.url)
        self.dashboards = {}
        self.creds = BuilderCreds(env_name = env_name)
        print("##################################")
        print("GRAFANA URL: " + self.url)


    def load_dashboards(self):
        headers = {'Accept': 'application/json, text/plain, */*', 'Content-Type': 'application/json'}
        response = requests.get(self.url + "/api/search?query=&starred=false", headers=headers, cookies = self.session.get_cookies())
        if response.status_code != 200:

            print(colorama.Style.BRIGHT + colorama.Fore.RED + colorama.Back.WHITE +
                  "ERROR TALKING TO GRAFANA TO LOAD DASHBOARDS: ")
            pprint.pprint(response.__dict__)
            print(colorama.Style.RESET_ALL)
            sys.exit()
        response_body = response.json()
        for r in response_body:
            d = GrafanaDashboard()
            d.tags = r['tags']
            d.type = r['type']
            d.title = r['title']
            d.uri = r['uri']
            d.isStarred = r['isStarred']
            d.id = r['id']
            self.dashboards[d.id] = d

    def delete_dashboard(self, title):
        url = self.url + "/api/dashboards/db/" + title.encode('utf8').replace(".", "-")
        headers = {'Accept': 'application/json, text/plain, */*', 'Content-Type': 'application/json'}
        response = requests.delete(url, headers=headers, cookies = self.session.get_cookies())
        if response.status_code != 200:
            print(colorama.Style.BRIGHT + colorama.Fore.RED + colorama.Back.WHITE +
                  "ERROR TALKING TO GRAFANA TO DELETE DASHBOARD: ")
            pprint.pprint(response.__dict__)
            print(colorama.Style.RESET_ALL)
            sys.exit()
        else:
            print(colorama.Style.BRIGHT + colorama.Fore.GREEN + colorama.Back.WHITE +
                  title + " DASHBOARD DELETED." + colorama.Style.RESET_ALL)

    def push_dashboard(self, body):
        target_url = self.url + "/api/dashboards/db"
        print(target_url)
        headers = {'Authorization': 'Bearer ' + str(self.creds.grafana_api_key), 'Content-Type': 'application/json'}
        utf8_body = body
        response = requests.post(target_url, headers=headers, data=utf8_body)
        if response.status_code != 200:
            print(colorama.Style.BRIGHT + colorama.Fore.RED + colorama.Back.WHITE +
                  "ERROR PUSHING DASHBOARD TO GRAFANA: ")
            pprint.pprint(response.__dict__)
            print(colorama.Style.RESET_ALL)
            sys.exit()
        else:
            print(colorama.Style.BRIGHT + colorama.Fore.GREEN + colorama.Back.WHITE +
                  "DASHBOARD CREATED." + colorama.Style.RESET_ALL)
 
        
                
    def push_release_dashboards(self, release_num):
        # SET VARS
        template_vars = {
                         "release_num": release_num
                         }
        target_url = self.url + "/api/dashboards/db"
        headers = {'Authorization': 'Bearer ' + str(self.creds.grafana_api_key), 'Content-Type': 'application/json'}
        # PUSH Build Overview page
        j2_env = jinja2.Environment(loader=jinja2.PackageLoader('grafanalib', 'templates'))
        template = j2_env.get_template('nightly_build_status.json.j2')
        utf8_body = template.render(template_vars)
        response = requests.post(target_url, headers=headers, data=utf8_body) #data=json.dumps(utf8_body)) #
        if response.status_code != 200:
            print(colorama.Style.BRIGHT + colorama.Fore.RED + colorama.Back.WHITE +
                  "ERROR PUSHING DASHBOARD TO GRAFANA: ")
            pprint.pprint(response.__dict__)
            print(colorama.Style.RESET_ALL)
            sys.exit()
        else:
            print(colorama.Style.BRIGHT + colorama.Fore.GREEN + colorama.Back.WHITE +
                  release_num + " Build Overview DASHBOARD CREATED." + colorama.Style.RESET_ALL)

    
        # PUSH Android Status page
        j2_env = jinja2.Environment(loader=jinja2.PackageLoader('grafanalib', 'templates'))
        template = j2_env.get_template('android_builds.json.j2')
        utf8_body = template.render(template_vars)
        response = requests.post(target_url, headers=headers, data=utf8_body)
        if response.status_code != 200:
            print(colorama.Style.BRIGHT + colorama.Fore.RED + colorama.Back.WHITE +
                  "ERROR PUSHING DASHBOARD TO GRAFANA: ")
            pprint.pprint(response.__dict__)
            print(colorama.Style.RESET_ALL)
            sys.exit()
        else:
            print(colorama.Style.BRIGHT + colorama.Fore.GREEN + colorama.Back.WHITE +
                  release_num + " Android Build DASHBOARD PUSHED." + colorama.Style.RESET_ALL)

        
        # PUSH iOS Status page
        j2_env = jinja2.Environment(loader=jinja2.PackageLoader('grafanalib', 'templates'))
        template = j2_env.get_template('ios_builds.json.j2')
        utf8_body = template.render(template_vars)
        response = requests.post(target_url, headers=headers, data=utf8_body)
        if response.status_code != 200:
            print(colorama.Style.BRIGHT + colorama.Fore.RED + colorama.Back.WHITE +
                  "ERROR PUSHING DASHBOARD TO GRAFANA: ")
            pprint.pprint(response.__dict__)
            print(colorama.Style.RESET_ALL)
            sys.exit()
        else:
            print(colorama.Style.BRIGHT + colorama.Fore.GREEN + colorama.Back.WHITE +
                  release_num + " iOS Build DASHBOARD CREATED." + colorama.Style.RESET_ALL)
    
