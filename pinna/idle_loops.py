#idle loops
import gobject
from connection import client
from variables import *
from ui import *
from scrapers import change_info
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
  insert=insert.replace('&','&amp;')

  mainwindow_wTree.get_widget('current_song_label').set_property("label","<span font_size='12344'>"+insert+"</span>")
  infowindow_wTree.get_widget('artist_entry').set_text(artist)
  infowindow_wTree.get_widget('title_entry').set_text(title)
  infowindow_wTree.get_widget('album_entry').set_text(album)

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

def get_insert(item):
  if 'artist' in item.keys() and 'title' in item.keys():
    return str(item['artist']+' - '+item['title']).replace('&','&amp;')
  else:
    return str(item['file'].split('/')[len(item['file'].split('/'))-1]).replace('&','&amp;')

def set_file_browser(oldsongs):
  model=browserwindow_wTree.get_widget('browser_list').get_model()
  for song in browser_vars.browser_list[2]:
    if song in browser_vars.current_playlist[2] and song not in oldsongs:
      index=browser_vars.browser_list[2].index(song)
      liter=model.get_iter(index)
      model.set_value(liter,1,'<b>'+browser_vars.browser_list[1][index][1]+'</b>')
    if song not in browser_vars.current_playlist[2] and song in oldsongs:
      index=browser_vars.browser_list[2].index(song)
      liter=model.get_iter(index)
      model.set_value(liter,1,browser_vars.browser_list[1][index][1])    
  highlight_song()

def set_current_browser(oldsongs):
  model=browserwindow_wTree.get_widget('browser_list').get_model()
  browserwindow_wTree.get_widget('browser_list').set_model(None)
  if len(oldsongs)>len(browser_vars.current_playlist[2]):
    number=len(oldsongs)-len(browser_vars.current_playlist[2])
    for i in range(len(oldsongs)-1,len(oldsongs)-number-1,-1):
        oldsongs.pop(i)
        model.remove(model.get_iter(i))   
  for song in browser_vars.current_playlist[2]:
    if song not in oldsongs:
      index=browser_vars.current_playlist[2].index(song)
      try:
        liter=model.get_iter(index)
        model.set_value(liter,1,browser_vars.current_playlist[1][index])
      except:
        model.append([gtk.STOCK_CDROM,browser_vars.current_playlist[1][index]])
  browserwindow_wTree.get_widget('browser_list').set_model(model)
  highlight_song()

def highlight_song():
  if browser_vars.view=='current':
    model=browserwindow_wTree.get_widget('browser_list').get_model()
    playing_song=client.currentsong()
    if len(playing_song.keys())!=0:
      if checks.last_song and checks.last_song[0]!=int(playing_song['pos']):
        liter=model.get_iter(checks.last_song[0])
        model.set_value(liter,1,checks.last_song[1])
        checks.last_song=(int(playing_song['pos']),get_insert(playing_song),playing_song['file'])
      if checks.last_song:
        liter=model.get_iter(checks.last_song[0])
        model.set_value(liter,1,'<b>'+checks.last_song[1]+'</b>')
      else:
        if not checks.last_song:
          checks.last_song=(int(playing_song['pos']),get_insert(playing_song),playing_song['file'])   
          highlight_song()

  if browser_vars.view=='file':
    model=browserwindow_wTree.get_widget('browser_list').get_model()
    playing_song=client.currentsong()
    if len(playing_song.keys())!=0:
      if checks.last_song:
        if checks.last_song[2] in browser_vars.browser_list[2] and checks.last_song[0]!=int(playing_song['pos']):
          liter=model.get_iter(browser_vars.browser_list[2].index(checks.last_song[2]))
          model.set_value(liter,1,'<b>'+checks.last_song[1]+'</b>')        
        checks.last_song=(int(playing_song['pos']),get_insert(playing_song),playing_song['file'])
        if checks.last_song[2] in browser_vars.browser_list[2]:
          liter=model.get_iter(browser_vars.browser_list[2].index(checks.last_song[2]))
          model.set_value(liter,1,'<b><i>'+checks.last_song[1]+'</i></b>')
      else:
        if not checks.last_song:
          checks.last_song=(int(playing_song['pos']),get_insert(playing_song),playing_song['file'])
          if checks.last_song[2] in browser_vars.browser_list[2]:
            highlight_song()


def update_current_playlist(version):
  changes=client.plchanges(version)
  oldsongs=browser_vars.current_playlist[2][:]
  playlist_length=int(client.status()['playlistlength'])
  if len(changes)>0:
    for change in changes:
      if int(change['pos'])>len(browser_vars.current_playlist[2])-1:
        browser_vars.current_playlist[2].append(change['file'])
        browser_vars.current_playlist[1].append(get_insert(change))
      if browser_vars.current_playlist[2][int(change['pos'])]!=change['file']:
        browser_vars.current_playlist[2][int(change['pos'])]=change['file']
        browser_vars.current_playlist[1][int(change['pos'])]=get_insert(change)
  browser_vars.current_playlist[1]=browser_vars.current_playlist[1][:playlist_length]
  browser_vars.current_playlist[2]=browser_vars.current_playlist[2][:playlist_length]
     
  if browser_vars.view=='file':
    set_file_browser(oldsongs[:])
  if browser_vars.view=='current':
    set_current_browser(oldsongs[:])

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
  try:
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
      checks.last_song=None
      if status['playlistlength']=='0':
        mainwindow_wTree.get_widget('current_song_label').set_property('label','')
    ###set things that are bound to change often :)
    mainwindow_wTree.get_widget('volume_scale').set_value(int(status['volume']))
    handle_toggles(status)
  except: 
    checks.song=-1
    mainwindow_wTree.get_widget('progressbar').set_text('not connected')
    mainwindow_wTree.get_widget('progressbar').set_fraction(0.0)
    mainwindow_wTree.get_widget('current_song_label').set_property('label','')
    try:
      client.disconnect()
    except:
      pass
    try:
      client.connect(settings.mpd_host,int(settings.mpd_port))
      client.password(settings.mpd_pass)
    except:
      pass
  return True  

gobject.timeout_add(250,idle_loop)  
