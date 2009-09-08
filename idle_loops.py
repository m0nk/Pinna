#idle loops
import gobject
import gtk
from connection import client
from variables import checks
from variables import settings
from variables import main_vars
from variables import *
from ui import *
#from scrapers import check_album_art
from scrapers import change_song
import time

def song_change():
  current_song=client.currentsong()
  artist=''
  title=''
  album=''
  if 'artist' in current_song:
    artist=current_song['artist']
  if 'title' in current_song:
    title=current_song['title']
  if 'album' in current_song:
    album=current_song['album']  
  if artist and title:
    insert = artist+' - '+title
  else:
    insert=current_song['file'].split('/')
    insert=insert[len(insert)-1]
  change_art(artist,album)
  insert=insert.replace('&','&amp;')
  mainwindow_wTree.get_widget('current_song_label').set_property("label","<span font_size='12344'>"+insert+"</span>")
  infowindow_wTree.get_widget('artist_entry').set_text(artist)
  infowindow_wTree.get_widget('title_entry').set_text(title)
  infowindow_wTree.get_widget('album_entry').set_text(album)

def change_art(artist,album):
  check=None
  if artist and album:
    check = change_song()
  if check:
    mainwindow_wTree.get_widget("main_window_album_art").set_from_pixbuf(gtk.gdk.pixbuf_new_from_file(check).scale_simple(80,80,gtk.gdk.INTERP_BILINEAR))
    infowindow_wTree.get_widget('album_art')set_from_pixbuf(gtk.gdk.pixbuf_new_from_file(check)
  else:
    mainwindow_wTree.get_widget('main_window_album_art').set_from_pixbuf(default_albumart.scale_simple(80,80,gtk.gdk.INTERP_BILINEAR))
    infowindow_wTree.get_widget('album_art').set_from_pixbuf(default_albumart)

def parse_time(mtime):
  new_time=""
  minutes=str(int(mtime)%60)
  hours=str(int(mtime)/60)
  if len(minutes)<2:
    minutes='0'+str(minutes)
  if len(hours)<2:
    hours='0'+str(hours)
  return str(hours)+":"+str(minutes)

def handle_time(status):
  time=status['time'].split(':')
  fraction=float(time[0])/float(time[1])
  mainwindow_wTree.get_widget('progressbar').set_fraction(fraction)
  elapsed=parse_time(time[0])
  full=parse_time(time[1])
  mainwindow_wTree.get_widget('progressbar').set_text(elapsed+"/"+full)

def handle_toggles(status):
  shuffle=status['random']
  if shuffle!=checks.shuffle:
    mainwindow_wTree.get_widget("shuffle_button").handler_block(main_vars.shuffle_id)
    mainwindow_wTree.get_widget('shuffle_button').set_active(int(status['random']))
    mainwindow_wTree.get_widget('shuffle_button').handler_unblock(main_vars.shuffle_id)
    checks.shuffle=shuffle
  repeat=status['repeat']
  if repeat!=checks.repeat:
    mainwindow_wTree.get_widget('repeat_button').handler_block(main_vars.repeat_id)
    mainwindow_wTree.get_widget('repeat_button').set_active(int(status['repeat']))
    mainwindow_wTree.get_widget('repeat_button').handler_unblock(main_vars.repeat_id)
    checks.repeat=repeat
    
  
def highlight_current_song():
  pass

def update_current_playlist():
  status=client.status()
  browser_vars.current_playlist[0]=None
  browser_vars.current_playlist[1]=[]
  print browser_vars.current_playlist
  for song in client.playlistinfo():
    if 'artist' and 'title' in song.keys():
      insert=song['artist']+' - '+song['title']
    else:
      insert=song['file'].split('/')
      insert=insert[len(insert)-1]        
    browser_vars.current_playlist[1].append(insert.replace('&','&amp;'))
  if browser_vars.view=='current':
    model=browserwindow_wTree.get_widget('browser_list').get_model()
    print model
    browserwindow_wTree.get_widget('browser_list').set_model()
    model.clear()
    for item in browser_vars.current_playlist[1]:
      model.append([item])
    browserwindow_wTree.get_widget('browser_list').set_model(model)
  browser_vars.playlist_version=status['playlist']
  
def check_alarm():
  real_time=time.localtime()[3:6]
  print real_time
  alarm_time=(settings.alarm_hour,settings.alarm_minute)
  if real_time[2]==0:
    if real_time[0]==int(alarm_time[0]) and real_time[1]==int(alarm_time[1]):
      client.volume(int(settings.alarm_volume)-int(client.status()['volume']))
      client.clear()
      client.load('alarm')
      client.play()
    print 'dicks'
    
def idle_loop():
  try:
    status=client.status()    
    stats=client.stats()
    if status['playlist'] != browser_vars.playlist_version:
      update_current_playlist()
    if status['state']!='play':
      check_alarm()
    if 'time' in status:
      if 'song' in status:
       if status['song']!=checks.song:
        song_change()
        checks.song=status['song']
      handle_time(status)
    else:
      if 'song' not in status:
        mainwindow_wTree.get_widget('main_window_album_art').set_from_pixbuf(default_albumart.scale_simple(80,80,gtk.gdk.INTERP_BILINEAR))
      mainwindow_wTree.get_widget('progressbar').set_text('00:00/00:00')
      mainwindow_wTree.get_widget('progressbar').set_fraction(0.0)
      if status['playlistlength']=='0':
        mainwindow_wTree.get_widget('current_song_label').set_property('label','')
    ###set things that are bound to change often :)
    mainwindow_wTree.get_widget('volume_scale').set_value(int(status['volume']))
    handle_toggles(status)  
  except: 
   mainwindow_wTree.get_widget('progressbar').set_text('not connected')
   mainwindow_wTree.get_widget('progressbar').set_fraction(0.0)
   mainwindow_wTree.get_widget('current_song_label').set_property('label','')
   try:
     try:
       client.disconnect()
     except:
       pass
     client.connect(settings.mpd_host,int(settings.mpd_port))
   except:
     pass
  return True  

gobject.timeout_add(250,idle_loop)  
