import urllib2
import os
import gtk
from connection import client
from ui import mainwindow_wTree
from ui import infowindow_wTree
from ui import default_albumart
from variables import info_vars

def change_info():
  song=client.currentsong()
  if info_vars.view=='lyrics':
    change_lyrics(None)
  if info_vars.view=='bio':
    change_biography(None)
  if 'artist' in song.keys() and 'album' in song.keys():
    song=song['artist']+':'+song['album']+'.jpg'
    song=song.lower().replace(' ','+')
    song=song.replace('/','+')
    check=os.getenv("HOME")+"/.pinna/album_art/"+song
    if os.path.isfile(check):
      mainwindow_wTree.get_widget('main_window_album_art').set_from_pixbuf(gtk.gdk.pixbuf_new_from_file(check).scale_simple(80,80,gtk.gdk.INTERP_BILINEAR))   
      #infowindow_wTree.get_widget('info_textview').get_buffer().insert_pixbuf(infowindow_wTree.get_widget('info_textview').get_buffer().get_iter_at_line_offset(0,0),gtk.gdk.pixbuf_new_from_file(check))      
    else:
      mainwindow_wTree.get_widget('main_window_album_art').set_from_pixbuf(default_albumart.scale_simple(80,80,gtk.gdk.INTERP_BILINEAR))
  else:
    mainwindow_wTree.get_widget('main_window_album_art').set_from_pixbuf(default_albumart.scale_simple(80,80,gtk.gdk.INTERP_BILINEAR))

def change_lyrics(widget):
  info_vars.view='lyrics'
  file_name=client.currentsong()['file'].split('/')
  file_name=file_name[len(file_name)-1]
  file_name=file_name.replace(' ','+')
  file_name=file_name[0:len(file_name)-4]+'.txt'
  check=os.getenv("HOME")+'/.pinna/lyrics/'+file_name
  if os.path.isfile(check):
    temp=open(check)
    lyrics=temp.read()
    infowindow_wTree.get_widget('info_textview').get_buffer().set_text(lyrics)
    temp.close()
  else:
    infowindow_wTree.get_widget('info_textview').get_buffer().set_text('')

def change_biography(widget):
  info_vars.view='bio'
  song=client.currentsong()
  artist=song['artist'].replace(' ','+')
  artist=artist.lower().replace('/','+')
  if os.path.isfile(os.getenv("HOME")+'/.pinna/bios/'+artist):
    temp=open(os.getenv("HOME")+'/.pinna/bios/'+artist)
    infowindow_wTree.get_widget('info_textview').get_buffer().set_text(temp.read())
    temp.close()
  else:
    infowindow_wTree.get_widget('info_textview').get_buffer().set_text('')
  
def format_text(data):
  charcters={'&#8216;':"'",'&#8217;':"'",'&#8220;':'"','&#8221;':'"','&#lt;':'<','&gt;':'>','&quot;':'"','&amp;':'&'}
  for charcter in charcters.keys():
    data=data.replace(charcter,charcters[charcter])
  new_data=""
  x=0
  while x<len(data):
    if data[x]=="<":
      while data[x]!=">":
        x+=1
    else:
      new_data+=data[x]     
    x+=1
  return new_data

def scrape_artistbio(show):
  song=client.currentsong()
  if 'artist' in song.keys():
    bio=''
    artist=infowindow_wTree.get_widget('artist_entry').get_text().lower().replace(' ','+')
    url='http://www.last.fm/music/'+artist+'/+wiki'
    u=urllib2.urlopen(url)
    data=u.read()
    start=data.find('<div id="wiki">')+36
    end=data.find('</div><!-- #wiki -->')
    data=data[start:end]
    save_artistbio(format_text(data),show)
   
def save_artistbio(bio,show):
  artist=client.currentsong()['artist']
  artist=artist.lower().replace(' ','+')
  artist=artist.replace('/','+')
  temp=open(os.getenv("HOME")+'/.pinna/bios/'+artist,'w')
  temp.write(bio)
  temp.close()
  if show==True:
    info_vars.view='bio'
    infowindow_wTree.get_widget('info_textview').get_buffer().set_text(bio)

def scrape_lyricwiki():
  artist=infowindow_wTree.get_widget('artist_entry').get_text().replace(' ','_')
  title=infowindow_wTree.get_widget('title_entry').get_text().replace(' ','_')
  try:
    song=artist+':'+title
    url='http://lyrics.wikia.com/lyrics/'+song
    u=urllib2.urlopen(url)
    data=u.read()
    u.close()
    data=data[data.find("<div class='lyricbox' >")+23:len(data)]
    data=data[0:data.find('<!-- ')]
    data=data.replace('<br />','\n')
    save_lyrics(format_text(data))
  except:
    save_lyrics('')

def scrape_lyricsplugin():
  artist=infowindow_wTree.get_widget('artist_entry').get_text().replace(' ','%20')
  title=infowindow_wTree.get_widget('title_entry').get_text().replace(' ','%20')
  
  url='http://lyricsplugin.com/wmplayer03/plugin/?artist='+artist+'&title='+title
  u=urllib2.urlopen(url)
  lyrics=u.read()
  lyrics=lyrics[lyrics.find('<div id="lyrics">')+18:len(lyrics)]
  lyrics=lyrics[0:lyrics.find('</div>')]
  lyrics=lyrics.replace('<br />\n<br />','\n')
  lyrics=lyrics.replace('<br />','')
  u.close()
  if not lyrics == '\n':
    save_lyrics(format_text(lyrics))
  else:
    save_lyrics('')
    
def save_lyrics(lyrics):
  info_vars.view='lyrics'
  file_name=client.currentsong()['file'].split('/')
  file_name=file_name[len(file_name)-1]
  file_name=file_name.replace(' ','+')
  file_name=file_name[0:len(file_name)-4]
  file_name=os.getenv("HOME")+'/.pinna/lyrics/'+file_name+'.txt'
  
  temp=open(file_name,'w')
  temp.write(lyrics)
  temp.close()
  infowindow_wTree.get_widget('info_textview').get_buffer().set_text(lyrics)

def save_albumart(artwork):
  song=client.currentsong()
  file_name=song['artist']+':'+song['album']
  file_name=file_name.lower().replace(' ','+')
  file_name=file_name.replace('/','+')
  file_name=os.getenv("HOME")+'/.pinna/album_art/'+file_name+'.jpg'
  
  temp=open(file_name,'w')
  temp.write(artwork)
  temp.close()

def scrape_albumart():
  song=client.currentsong()
  file_name=song['artist']+':'+song['album']+'.jpg'
  file_name=file_name.replace(' ','+')
  file_name=file_name.lower()
  if 'artist' in song.keys() and 'album' in song.keys():
    song = infowindow_wTree.get_widget('artist_entry').get_text()+'+'+infowindow_wTree.get_widget('album_entry').get_text()
    song=song.replace(' ','+')
    url='http://www.amazon.com/s/ref=nb_ss_gw?url=search-alias%3Dpopular&field-keywords='+song+'&x=0&y=0'
    temp=urllib2.urlopen(url.encode('latin1'))
    data=temp.read()
    temp.close()
    start=data.find('<td class="imageColumn" width="123"><table border="0" cellpadding="0" cellspacing="0">')
    end=data.find('<td class="dataColumn"><table cellpadding="0" cellspacing="0" border="0"><tr><td>')
    data=data[start:end]
    temp=data.find('<img src="')
    if temp < 0:
      temp=data.find(' src=')+6
    else:
      temp+=10
    data=data[temp:data.find('.jpg"')+4]
    u=urllib2.urlopen(data)
    picture=u.read()
    u.close()
    image_file=open(os.getenv("HOME")+"/.pinna/album_art/"+file_name, 'w')
    image_file.write(picture)
    image_file.close()
    mainwindow_wTree.get_widget("main_window_album_art").set_from_pixbuf(gtk.gdk.pixbuf_new_from_file(os.getenv("HOME")+"/.pinna/album_art/"+file_name).scale_simple(80,80,gtk.gdk.INTERP_BILINEAR))

def search(widget):
  if infowindow_wTree.get_widget('search_for').get_active()==0:
    try:
      scrape_artistbio(False)
    except: 
      pass
    try:
      scrape_albumart()
    except:
      pass
    if infowindow_wTree.get_widget('lyricsite').get_active()==1:
      scrape_lyricwiki()
    if infowindow_wTree.get_widget('lyricsite').get_active()==0:
      scrape_lyricsplugin()
  if infowindow_wTree.get_widget('search_for').get_active()==1:
    scrape_albumart()
  if infowindow_wTree.get_widget('search_for').get_active()==2:
    if infowindow_wTree.get_widget('lyricsite').get_active()==1:
      scrape_lyricwiki()
    if infowindow_wTree.get_widget('lyricsite').get_active()==0:
      scrape_lyricsplugin()
  if infowindow_wTree.get_widget('search_for').get_active()==3:
    scrape_artistbio(True)

def showsearch_window(widget):
  infowindow_wTree.get_widget('search_window').show()

def close_infowindow(widget,event):
  infowindow_wTree.get_widget('info_window').hide()
  return True

def search_for_changed(widget):
  if infowindow_wTree.get_widget('search_for').get_active()!=0 and infowindow_wTree.get_widget('search_for').get_active()!=2:
    infowindow_wTree.get_widget('lyricsite').set_sensitive(False)
  else:
    infowindow_wTree.get_widget('lyricsite').set_sensitive(True)

def infowindow_event(widget,event):
  if event.keyval==65307:
    close_infowindow(widget,event)
  if event.keyval==65470:
    change_lyrics(widget)
  if event.keyval==65471:
    change_biography(widget)
  if event.keyval==65472:
    showsearch_window(widget)

def close_searchwindow(widget,event):
  infowindow_wTree.get_widget('search_window').hide()
  return True

if not os.path.isdir(os.getenv("HOME")+'/.pinna'):
  os.mkdir(os.getenv("HOME")+'/.pinna')
if not os.path.isdir(os.getenv("HOME")+'/.pinna/bios'):
  os.mkdir(os.getenv("HOME")+'/.pinna/bios')
if not os.path.isdir(os.getenv("HOME")+'/.pinna/album_art'):
  os.mkdir(os.getenv("HOME")+'/.pinna/album_art')
if not os.path.isdir(os.getenv("HOME")+'/.pinna/lyrics'):
  os.mkdir(os.getenv("HOME")+'/.pinna/lyrics')

buttons={'on_lyric_button_clicked':change_lyrics,'on_artist_button_clicked':change_biography,'on_search_button_clicked':showsearch_window,'on_info_window_delete_event':close_infowindow,'on_info_window_key_press_event':infowindow_event}
search_buttons={'on_search1_button_clicked':search,'on_search_window_delete_event':close_searchwindow,'on_search_for_changed':search_for_changed}

infowindow_wTree.get_widget('lyricsite').set_active(0)
infowindow_wTree.get_widget('search_for').set_active(0)

infowindow_wTree.signal_autoconnect(search_buttons)
infowindow_wTree.signal_autoconnect(buttons)
