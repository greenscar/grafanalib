import pprint
import json
import re
import sys
import pdb
import requests
import logging
import time

class GrafanaDashboard(object):
    
    
    
    def __init__(self):
        self = self
        self.tags = []
        self.type = None
        self.title = None
        self.uri = None
        self.isStarred = False
        self.id = None