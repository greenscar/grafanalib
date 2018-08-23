### NOTE: To push a dashboard to test grafana, you must currently use the following URL
###    pipenv run python3 generate_grafana_dashboard.py -u http://ts1mtick-04.m3.ebay.com:8888 -hl nfs_inode_usage
### For prod grafana, you can use the load balancer:
###    pipenv run python3 generate_grafana_dashboard.py -u https://prod-grafana.m3.ebay.com -hl nfs_inode_usage

from grafanalib.dynamic.generator import Generator
from grafanalib.grafana import Grafana
import argparse
import pdb
import sys
import re
import pprint
import colorama
import json
grafana_url = {}
grafana_url['test'] = "http://ts1mtick-04.m3.ebay.com:3000"
grafana_url['prod'] = "https://prod-grafana.m3.ebay.com"
parser = argparse.ArgumentParser(description="Create Page Hierarchy")
#parser.add_argument('-u', '--url', help='Grafana URL (https://prod-grafana.m3.ebay.com or https://test-grafana.m3.ebay.com', type=str, required=True)
parser.add_argument('--env', help='InfluxDB instance to query', type=str, default='test', choices=['test', 'prod'])
parser.add_argument('-hl', '--hosts', help='CSV Host List', type=str, required=True)
args = parser.parse_args()
host_list = args.hosts.split(',')
grafana = Grafana(env_name = args.env, grafana_url = grafana_url[args.env])
mygen = Generator()


for a_servername in host_list:

    if re.match('^build_node_ios$', a_servername):
        templatename = "build_node_ios.dashboard"
        grafana_tags = ["osx", "ios"]
        database = "build_ios"
    elif re.match('.*mongo', a_servername):
        templatename = "mongo.dashboard"
        grafana_tags = ["ubuntu", "mongo", "docker"]
        database = "telegraf"
    elif re.match('build_node_ios_comparison', a_servername):
        templatename = "build_node_ios_comparison.dashboard"
        grafana_tags = ["osx", "ios"]
        database = "build_ios"
    elif re.match('build_node_andr', a_servername):
        templatename = "build_node_andr.dashboard"
        grafana_tags = ["ubuntu", "andr"]
        database = "jenkins-andr"

    elif re.match('ps1minfluxdb-02', a_servername):
        templatename = "influxdb.dashboard"
        grafana_tags = ["linux", "influxdb"]
        database = "telegraf"
    elif re.match('^\w+s1.*', a_servername):
        templatename = "server.dashboard"
        grafana_tags = ["linux", "android"]
        database = "telegraf"
    elif re.match('^\w+s1.*', a_servername):
        templatename = "build_node_andr.dashboard"
        grafana_tags = ["linux", "android"]
        database = "build_andr"
    elif re.match('^pp1mi92-03', a_servername):
        templatename = "build_node_ios.dashboard"
        grafana_tags = ["osx", "ios"]
        database = "telegraf"
    elif re.match('^\w+p1.*', a_servername):
        templatename = "build_node_ios.dashboard"
        grafana_tags = ["osx", "ios"]
        database = "build_ios"
    elif re.match('^\w+m1.*', a_servername):
        templatename = "build_node_ios.dashboard"
        grafana_tags = ["osx", "ios"]
        database = "build_ios"
    elif re.match('ebay-ubuntu1604', a_servername):
        templatename = "build_node_andr_gpu.dashboard"
        grafana_tags = ["jamestest"]
        database = "build_andr"
    elif re.match('nfs_disk_usage', a_servername):
        templatename = "nfs_disk_usage.dashboard"
        grafana_tags = ["nfs_disk_usage"]
        database = "telegraf"
    elif re.match('nfs_inode_usage', a_servername):
        templatename = "nfs_inode_usage.dashboard"
        grafana_tags = ["nfs_inode_usage"]
        database = "telegraf"
    else:
        print(a_servername + " does not match our templates currently.")
        sys.exit()

    j2_args = {
        "servername": a_servername,
        "database": database,
        "grafana_tags": grafana_tags
    }

    print("#####################################################################")
    print("#####################################################################")
    print("Generating Dashboard")
    print(templatename)
    print(j2_args)
    print("#####################################################################")

    json_body = mygen.generate_server_dashboard(templatename, j2_args, grafana_tags, output_dir=None)

    grafana.push_dashboard(json_body)

    print("#####################################################################")
    print("#####################################################################")
    print("Done")
    print(templatename)
    print(j2_args)
    print("#####################################################################")
