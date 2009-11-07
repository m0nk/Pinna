from connection import client
from variables import settings
from ui import settingswindow_wTree
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
      if line[0]=='music_directory':
        settings.music_directory=line[1]
    temp.close()
    insert_config()
  else:
    insert_config()
    save_config(None)
  try:
    client.disconnect()
  except:
    pass
  try: 
    client.connect(settings.mpd_host,int(settings.mpd_port))
    if settings.mpd_pass:
      client.password(settings.mpd_pass)
  except:
    pass
    
def insert_config():
  settingswindow_wTree.get_widget('mpd_host').set_text(settings.mpd_host)
  settingswindow_wTree.get_widget('mpd_port').set_text(settings.mpd_port)
  settingswindow_wTree.get_widget('mpd_password').set_text(settings.mpd_pass)
  settingswindow_wTree.get_widget('stop_on_exit').set_active(int(settings.stop_on_exit))
  settingswindow_wTree.get_widget('alarm_enable').set_active(int(settings.alarm_enable))
  settingswindow_wTree.get_widget('alarm_hours').set_value(int(settings.alarm_hour))
  settingswindow_wTree.get_widget('alarm_minutes').set_value(int(settings.alarm_minute))
  settingswindow_wTree.get_widget('alarm_volume').set_value(int(settings.alarm_volume))
  settingswindow_wTree.get_widget('music_directory').set_text(settings.music_directory)

def apply_settings():
  settings.mpd_host=settingswindow_wTree.get_widget('mpd_host').get_text()
  settings.mpd_port=settingswindow_wTree.get_widget('mpd_port').get_text()
  settings.mpd_pass=settingswindow_wTree.get_widget('mpd_password').get_text()
  settings.stop_on_exit=settingswindow_wTree.get_widget('stop_on_exit').get_active()
  settings.alarm_enable=settingswindow_wTree.get_widget('alarm_enable').get_active()
  settings.alarm_hour=settingswindow_wTree.get_widget('alarm_hours').get_text()
  settings.alarm_minute=settingswindow_wTree.get_widget('alarm_minutes').get_text()
  settings.alarm_volume=settingswindow_wTree.get_widget('alarm_volume').get_text()
  settings.music_directory=settingswindow_wTree.get_widget('music_directory').get_text()
  if settings.stop_on_exit==True:
    settings.stop_on_exit='1'
  else:
    settings.stop_on_exit='0'
  if settings.alarm_enable==True:
    settings.alarm_enable='1'
  else:
    settings.alarm_enable='0'
    
def save_config(widget):
  apply_settings()
  temp=open(os.getenv("HOME")+"/.pinna.conf",'w')
  temp.write('mpd_host = '+settings.mpd_host+"\n")
  temp.write('mpd_port = '+settings.mpd_port+"\n")
  temp.write('mpd_pass = '+settings.mpd_pass+"\n") 
  temp.write('stop_on_exit = '+settings.stop_on_exit+"\n")
  temp.write('alarm_enable = '+settings.alarm_enable+"\n")
  temp.write('alarm_time = '+settings.alarm_hour+':'+settings.alarm_minute+"\n")
  temp.write('alarm_volume = '+settings.alarm_volume+"\n")
  temp.write('music_directory = '+settings.music_directory+'\n')
  temp.close()
  read_config()

def close_window(widget,event):
  settingswindow_wTree.get_widget('settings_window').hide_all()
  return True
  
def hotkeys(widget,event):
  keypress=event.keyval
  if keypress==65307:
    close_window(None,None)
    return True
  
buttons={'on_save_button_clicked':save_config,'on_settings_window_delete_event':close_window,'on_settings_window_key_press_event':hotkeys}
settingswindow_wTree.signal_autoconnect(buttons)
read_config()
