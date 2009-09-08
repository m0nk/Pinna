from connection import client
from variables import settings
import os
  
def read_config():
  if os.path.isfile(os.getenv("HOME")+"/.pinna.conf"):
    temp=open(os.getenv("HOME")+"/.pinna.conf")
    for line in temp.read().split("\n"):
      line=line.split(" = ")
      if line[0]=='mpd_host':
        settings.mpd_host=line[1]
      if line[0]=='mpd_port':
        settings.mpd_port=line[1]
      if line[0]=='mpd_pass':
        settings.mpd_pass=line[1]
      if line[0]=='stop_on_exit':
        settings.stop_on_exit=line[1]
      if line[0]=='alarm_enable':
        settings.alarm_enable=line[1]
      if line[0]=='alarm_time':
        settings.alarm_hour=line[1].split(":")[0]
        settings.alarm_minute=line[1].split(":")[1]
      if line[0]=='alarm_volume':
        settings.alarm_volume=line[1]
    temp.close()
  else:
    save_config()
  client.connect(settings.mpd_host,int(settings.mpd_port))

def save_config():
  print 'saving config'
  temp=open(os.getenv("HOME")+"/.pinna.conf",'w')
  temp.write('mpd_host = '+settings.mpd_host+"\n")
  temp.write('mpd_port = '+settings.mpd_port+"\n")
  temp.write('mpd_pass = '+settings.mpd_pass+"\n") 
  temp.write('stop_on_exit = '+settings.stop_on_exit+"\n")
  temp.write('alarm_enable = '+settings.alarm_enable+"\n")
  temp.write('alarm_time = '+settings.alarm_hour+':'+settings.alarm_minute+"\n")
  temp.write('alarm_volume = '+settings.alarm_volume+"\n")
  temp.close()

read_config()
