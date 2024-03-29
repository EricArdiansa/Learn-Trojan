import sqlite3, os

def history():
   import operator
   from collections import OrderedDict
#import matplotlib.pyplot as plt

   def parse(url):
           try:
                   parsed_url_components = url.split('//')
                   sublevel_split = parsed_url_components[1].split('/', 1)
                   domain = sublevel_split[0].replace("www.", "")
                   return domain
           except IndexError:
                   print("URL format error!")

   def analyze(results):
      b=open("chrome1.txt","w")
      for site, count in sites_count_sorted.items():
         #print site, count
         b.write(site + "\n")
#path to user's history database (Chrome)
      b.close()

   data_path = os.path.expanduser('~')+"\AppData\Local\Google\Chrome\User Data\Default"
   files = os.listdir(data_path)
   history_db = os.path.join(data_path, 'history')
#querying the db
   c = sqlite3.connect(history_db)
   cursor = c.cursor()
   select_statement = "SELECT urls.url, urls.visit_count FROM urls, visits WHERE urls.id = visits.url;"
   cursor.execute(select_statement)
   results = cursor.fetchall() 
   sites_count = {} 
   for url, count in results:
           url = parse(url)
           if url in sites_count:
                   sites_count[url] += 1
           else:
                   sites_count[url] = 1
   sites_count_sorted = OrderedDict(sorted(sites_count.items(), key=operator.itemgetter(1), reverse=True))
   analyze (sites_count_sorted)
history()