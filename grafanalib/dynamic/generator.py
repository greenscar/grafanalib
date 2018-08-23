"""Generate JSON Grafana dashboards.
Originally pulled from https://github.com/weaveworks/grafanalib
Apache License - https://github.com/weaveworks/grafanalib/blob/master/LICENSE"""

import argparse
import json
import os
import sys
import pdb
import jinja2
from pprint import pprint
from grafanalib.dynamic.dashboard import Dashboard
import imp

DASHBOARD_TEMPLATE_DIR = "./templates"
DASHBOARD_SUFFIX = '.dashboard.py'


class Generator(object):

    def load_dashboard(self, path):
        module = imp.load_source('dashboard', path)
        marker = object()
        dashboard = getattr(module, 'dashboard', marker)
        if dashboard is marker:
            raise DashboardError(
                "Dashboard definition {} does not define 'dashboard'".format(path))
        return(dashboard.auto_panel_ids())

    def write_dashboard(self, dashboard, stream, j2_args=None, tags=None, to_push_via_rest=False):
        if tags is not None:
            dashboard.set_tags(tags)
        dashboard_text = json.dumps(
            dashboard.to_json_data(to_push_via_rest=to_push_via_rest),
            # stream,
            sort_keys=True,
            indent=2,
            cls=DashboardEncoder
        )

        if j2_args is not None:
            j2env = jinja2.Environment()
            j2template = j2env.from_string(dashboard_text)
            # import pprint
            # pprint.pprint(j2template)
            dashboard_text = j2template.render(j2_args)

        stream.write(dashboard_text)
        stream.write('\n')
        return(dashboard_text)

    def print_dashboard(self, dashboard, j2_args=None, tags=None, to_push_via_rest=False):
        return(self.write_dashboard(dashboard, j2_args=j2_args, tags=tags, to_push_via_rest=to_push_via_rest, stream=sys.stdout))

    
    def write_dashboards(self, paths):
        for path in paths:
            dashboard = self.load_dashboard(path)
            with open(self.get_json_path(path), 'w') as json_file:
                self.write_dashboard(dashboard, json_file)
    

    def get_json_path(self, path):
        assert path.endswith(DASHBOARD_SUFFIX)
        return '{}.json'.format(path[:-len(DASHBOARD_SUFFIX)])
    

    def dashboard_path(self, path):
        abspath = os.path.abspath(path)
        if not abspath.endswith(DASHBOARD_SUFFIX):
            raise argparse.ArgumentTypeError(
                'Dashboard file {} does not end with {}'.format(
                    path, DASHBOARD_SUFFIX))
        return abspath

    def generate_server_dashboard(self, templatename, j2_args, tags, output_dir=None):
        try:
            my_path = os.path.abspath(os.path.dirname(__file__))
            file_path = os.path.join(my_path, DASHBOARD_TEMPLATE_DIR, templatename)
            dashboard = self.load_dashboard(file_path)
            # dashboard
            if not output_dir:
                return(self.print_dashboard(dashboard, j2_args=j2_args, tags=tags, to_push_via_rest=True))
            else:
                with open(output_dir, 'w') as output:
                    self.write_dashboard(dashboard, j2_args, tags, output)
        except DashboardError as e:
            sys.stderr.write('ERROR: {}\n'.format(e))
            return 1


class DashboardEncoder(json.JSONEncoder):
    """Encode dashboard objects."""

    def default(self, obj):
        to_json_data = getattr(obj, 'to_json_data', None)
        if to_json_data:
            return to_json_data()
        return json.JSONEncoder.default(self, obj)

class DashboardError(Exception):
    """Raised when there is something wrong with a dashboard."""





