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
    def __init__(self,id):
        pass

    def get_config(self):
        pass

    def module_runner(self, module):
        pass

    def store_module(self, data):
        pass
    
    def run(self):
        pass