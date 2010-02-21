#idle loops
import gobject
from connection import client
from variables import *
from ui import *
from scrapers import change_info
import time
import operator

def get_insert(item):
  song=['','','','']
  if 'album' in item.keys():
    song[3]=item['album']
  if 'artist' in item.keys():
    song[1]=item['artist']
  if 'title' in item.keys():
    song[2]=item['title']
  if song[1] and song[2]:
    song[0]=song[1]+' - '+song[2]
    song[0]=song[0].replace('&','&amp;')
  else:
    song[0]=str(item['file'].split('/')[len(item['file'].split('/'))-1]).replace('&','&amp;')
  return song

def song_change():
  song=get_insert(client.currentsong())
  
  mainwindow_wTree.get_widget('current_song_label').set_property("label","<span font_size='12344'>"+song[0]+"</span>")
  infowindow_wTree.get_widget('artist_entry').set_text(song[1])
  infowindow_wTree.get_widget('title_entry').set_text(song[2])
  infowindow_wTree.get_widget('album_entry').set_text(song[3])
  highlight_song()

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

def set_file_browser(oldsongs):
  model=browserwindow_wTree.get_widget('browser_list').get_model()
  current_playlist_files=map(operator.itemgetter(2),browser_vars.current_playlist[1])
  browser_files=map(operator.itemgetter(2),browser_vars.browser_list[1])
  ### set new highlights
  for song in current_playlist_files:
    if song in current_playlist_files and song in browser_files:
      index=browser_files.index(song)
      liter=model.get_iter(index)
      model.set_value(liter,1,'<b>'+browser_vars.browser_list[1][index][1]+'</b>')
  ### remove old highlights
  for song in oldsongs:
    if song in browser_files and song not in current_playlist_files:
      index=browser_files.index(song)
      liter=model.get_iter(index)
      model.set_value(liter,1,browser_vars.browser_list[1][index][1])
  #highlight_song()

def set_current_browser(deleted,to_modify,old_length):
  model=browserwindow_wTree.get_widget('browser_list').get_model()
  browserwindow_wTree.get_widget('browser_list').set_model(None)
  if deleted:
    for i in range(old_length-1,old_length-deleted-1,-1):
      model.remove(model.get_iter(i))
  if len(to_modify)!=0:
    for item in to_modify:
      try:
        liter=model.get_iter(item[0])
        model.set_value(liter,1,item[1])
      except:
        model.append([gtk.STOCK_CDROM,item[1]])
  browserwindow_wTree.get_widget('browser_list').set_model(model)
  playing_song=client.currentsong()
  if len(playing_song.keys())!=0:
    if checks.last_song:
     if checks.last_song[0]!=playing_song['pos']:
      checks.last_song=(playing_song['pos'],get_insert(playing_song)[0],playing_song['file'])
      highlight_song()


def highlight_song():
  playing_song=client.currentsong()
  model=browserwindow_wTree.get_widget('browser_list').get_model()
  if browser_vars.view=='current':
    if checks.last_song:
      if checks.last_song[0]!=int(playing_song['pos']):
        model.set_value(model.get_iter(checks.last_song[0]),1,checks.last_song[1])
    checks.last_song=(int(playing_song['pos']),get_insert(playing_song)[0],playing_song['file'])
    model.set_value(model.get_iter(checks.last_song[0]),1,'<b>'+checks.last_song[1]+'</b>')
  if browser_vars.view=='file':
    if checks.last_song:
      browser_files=map(operator.itemgetter(2),browser_vars.browser_list[1])
      if checks.last_song[2] in browser_files:
        index=browser_files.index(checks.last_song[2])
        liter=model.get_iter(index)
        model.set_value(liter,1,'<b>'+checks.last_song[1]+'</b>')
      if playing_song['file'] in browser_files:
        index=browser_files.index(playing_song['file'])
        liter=model.get_iter(index)
        model.set_value(liter,1,'<b><i>'+get_insert(playing_song)[0]+'</i></b>')
    if 'pos' in playing_song.keys():
      checks.last_song=(int(playing_song['pos']),get_insert(playing_song)[0],playing_song['file'])

def update_current_playlist(version):
  model=browserwindow_wTree.get_widget('browser_list').get_model()
  changes=client.plchanges(version)
  current_playlist_files=map(operator.itemgetter(2),browser_vars.current_playlist[1])
  oldsongs=current_playlist_files[:]
  playlist_length=int(client.status()['playlistlength'])
  if playlist_length==0:
    checks.last_song=None
  old_length=len(oldsongs)
  if old_length > playlist_length:
    deleted=old_length-playlist_length
  else:
    deleted=None
  to_modify=[]
  if len(changes)>0:
    for change in changes:
      if int(change['pos'])>len(current_playlist_files)-1:
        browser_vars.current_playlist[1].append((change['pos'],get_insert(change)[0],change['file']))
        to_modify.append((int(change['pos']),get_insert(change)[0],change['file']))
      else:
        if current_playlist_files[int(change['pos'])]!=change['file']:
          browser_vars.current_playlist[1][int(change['pos'])]=(change['pos'],get_insert(change)[0],change['file'])
          to_modify.append((int(change['pos']),get_insert(change)[0],change['file']))

  browser_vars.current_playlist[1]=browser_vars.current_playlist[1][:playlist_length]
     
  if browser_vars.view=='file':
    set_file_browser(oldsongs[:])
  if browser_vars.view=='current':
    set_current_browser(deleted,to_modify,old_length)

def check_alarm():
  real_time=time.localtime()[3:6]
  alarm_time=(settings.alarm_hour,settings.alarm_minute)
  if real_time[2]==0 and settings.alarm_enable=='1':
    if real_time[0]==int(alarm_time[0]) and real_time[1]==int(alarm_time[1]):
      client.setvol(int(settings.alarm_volume))
      client.clear()
      client.load('alarm')
      client.play()
    
def idle_loop():
  #try:
    status=client.status()    
    stats=client.stats()
    if status['playlist'] != checks.playlist_version:
      update_current_playlist(checks.playlist_version)
      checks.playlist_version=status['playlist']
    if status['state']!='play':
      check_alarm()
    if 'time' in status:
      if 'song' in status:
       if int(status['songid'])!=checks.song:
        highlight_song()
        change_info()
        song_change()
        checks.song=int(status['songid'])
      else:
        checks.song=-1
        
      handle_time(status)
    else:     
      if 'song' not in status:
        checks.song=-1
        mainwindow_wTree.get_widget('main_window_album_art').set_from_pixbuf(default_albumart.scale_simple(80,80,gtk.gdk.INTERP_BILINEAR))
        infowindow_wTree.get_widget('info_textview').get_buffer().set_text('')
        infowindow_wTree.get_widget('info_textview').get_buffer().insert_pixbuf(infowindow_wTree.get_widget('info_textview').get_buffer().get_iter_at_line_offset(0,0),default_albumart)
        infowindow_wTree.get_widget('artist_entry').set_text('')
        infowindow_wTree.get_widget('title_entry').set_text('')
        infowindow_wTree.get_widget('album_entry').set_text('')
      mainwindow_wTree.get_widget('progressbar').set_text('00:00/00:00')
      mainwindow_wTree.get_widget('progressbar').set_fraction(0.0)
      #checks.last_song=None
      if status['playlistlength']=='0':
        mainwindow_wTree.get_widget('current_song_label').set_property('label','')
    ###set things that are bound to change often :)
    mainwindow_wTree.get_widget('volume_scale').set_value(int(status['volume']))
    handle_toggles(status)
  #except: 
  #  checks.song=-1
  #  mainwindow_wTree.get_widget('progressbar').set_text('not connected')
  #  mainwindow_wTree.get_widget('progressbar').set_fraction(0.0)
  #  mainwindow_wTree.get_widget('current_song_label').set_property('label','')
  #  try:
  #    client.disconnect()
  #  except:
  #    pass
  #  try:
  #    client.connect(settings.mpd_host,int(settings.mpd_port))
  #    client.password(settings.mpd_pass)
  #  except:
  #    pass
    return True  


gobject.timeout_add(250,idle_loop)  
