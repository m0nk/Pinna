import gtk
import gtk.glade
import sys
from connection import client
from ui import *
from variables import settings
from variables import checks
from variables import main_vars

def show_browser_window(widget):
  browserwindow_wTree.get_widget('browser_window').show()

def show_settings_window(widget):
 settingswindow_wTree.get_widget('settings_window').show()
 
def show_info_window(widget):
  infowindow_wTree.get_widget('info_window').show() 
 
def stop(widget):
  client.stop()
  print settings.stop_on_exit
  
def previous(widget):
  client.previous() 
  
def next(widget):
  client.next()
  settings.stop_on_exit=1
  
def play(widget):
  status=client.status()['state']
  if status!='stop':
    client.pause()
  else:
    client.play() 

def shuffle(widget):
  if client.status()['random']=='0':
    client.random(1)
  else:
    client.random(0)

def repeat(widget):
  if client.status()['repeat']=='0':
    client.repeat(1)
  else:
    client.repeat(0)

def change_volume(widget,value):
  current_volume=int(client.status()['volume'])
  new_volume=int(value)
  client.volume(str(new_volume-current_volume))

def song_scroll(widget,click):
  click=click.x
  if main_vars.album_art=='1':
    click=float(click/249.0)
  else:
    click=float(click/329.0)  
  status=client.status()
  song=status['song']
  fulltime=int(status['time'].split(":")[1])
  change=int(click*fulltime)
  client.seek(song,change)

def quit(widget,event):
  if settings.stop_on_exit=='1':
    client.stop()
  sys.exit(1)

def hotkeys(widget,event):
  keypress = event.keyval
  if keypress == 65367: # end
    client.stop()
  if keypress == 65362: # up
    client.volume(3)
  if keypress == 65364: #down
    client.volume('-2')
  if keypress == 65361: # left
    client.previous()
  if keypress == 65363: # right
    client.next()
  if keypress == 65535: # delete
    shuffle(None)
  if keypress == 65366: # pg down
    repeat(None)
  if keypress == 32: #space
    play(None)
  return True
  
buttons={'on_previous_button_clicked':previous,'on_next_button_clicked':next,'on_play_button_clicked':play,'on_stop_button_clicked':stop,
'on_info_button_clicked':show_info_window,'on_browser_button_clicked':show_browser_window,'on_settings_button_clicked':show_settings_window,
'dicks':change_volume,'on_progressbar_button_press_event':song_scroll,'on_windowMain_delete_event':quit,'on_windowMain_key_press_event':hotkeys}
mainwindow_wTree.signal_autoconnect(buttons)

temp=mainwindow_wTree.get_widget("shuffle_button")
main_vars.shuffle_id=temp.connect("toggled",shuffle)
    
temp=mainwindow_wTree.get_widget("repeat_button")
main_vars.repeat_id=temp.connect("toggled",repeat)




