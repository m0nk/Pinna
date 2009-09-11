import os
import urllib2
import gtk
from connection import client
from ui import infowindow_wTree
from ui import mainwindow_wTree
from ui import default_albumart

def change_info():
  song=client.currentsong()
  file_name=song['file'].split('/')
  file_name=file_name[len(file_name)-1]
  check=os.getenv("HOME")+"/.pinna/lyrics/"+file_name[0:len(file_name)-3]+'txt'
  if os.path.isfile(check):
    temp=open(check)
    lyrics=temp.read()
    infowindow_wTree.get_widget('info_textview').get_buffer().set_text(lyrics)
    temp.close()
  else:
    infowindow_wTree.get_widget('info_textview').get_buffer().set_text('')
  if 'artist' in song.keys() and 'title' in song.keys():  
    check=os.getenv("HOME")+"/.pinna/album_art/"+song['artist'].lower()+":"+song['album'].lower()+'.jpg'
    check=check.replace(' ','+')
    if os.path.isfile(check):
      mainwindow_wTree.get_widget("main_window_album_art").set_from_pixbuf(gtk.gdk.pixbuf_new_from_file(check).scale_simple(80,80,gtk.gdk.INTERP_BILINEAR))
      infowindow_wTree.get_widget('album_art').set_from_pixbuf(gtk.gdk.pixbuf_new_from_file(check))
    else:
      mainwindow_wTree.get_widget('main_window_album_art').set_from_pixbuf(default_albumart.scale_simple(80,80,gtk.gdk.INTERP_BILINEAR))
      infowindow_wTree.get_widget('album_art').set_from_pixbuf(default_albumart)
  else:
     mainwindow_wTree.get_widget('main_window_album_art').set_from_pixbuf(default_albumart.scale_simple(80,80,gtk.gdk.INTERP_BILINEAR))
     infowindow_wTree.get_widget('album_art').set_from_pixbuf(default_albumart)
     
def get_lyrics(widget):
  song=client.currentsong()
  file_name=song['file'].split("/")
  file_name=file_name[len(file_name)-1]
  check=os.getenv("HOME")+"/.pinna/lyrics/"+file_name[0:len(file_name)-3]+'txt'
  lyrics=''
  if os.path.isfile(check):
    temp=open(check)
    lyrics=temp.read()
    temp.close()
  else:
    lyrics=scrape_lyrics()
    if lyrics:
      temp=open(check, 'w')
      temp.write(lyrics)
  infowindow_wTree.get_widget('info_textview').get_buffer().set_text(lyrics)

def scrape_lyrics():
  artist=infowindow_wTree.get_widget('artist_entry').get_text().replace(' ','%20')
  title=infowindow_wTree.get_widget('title_entry').get_text().replace(' ','%20')
  
  url='http://lyricsplugin.com/wmplayer03/plugin/?artist='+artist+'&title='+title
  u=urllib2.urlopen(url)
  lyrics=u.read()
  lyrics=lyrics[lyrics.find('<div id="lyrics">')+17:len(lyrics)]
  lyrics=lyrics[0:lyrics.find('</div>')]
  lyrics=lyrics.replace('<br />\n<br />','\n')
  lyrics=lyrics.replace('<br />','')
  u.close()
  if not lyrics == '\n\n':
    return format_text(lyrics)
  return ''

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

def get_artist_bio(widget):
  song=client.currentsong()
  bio=''
  if 'artist' in song.keys():
    real_artist=song['artist'].lower().replace(' ','+')
    artist=infowindow_wTree.get_widget('artist_entry').get_text().lower().replace(' ','+')
    
    if os.path.isfile(os.getenv("HOME")+"/.pinna/bios/"+real_artist):
      temp=open(os.getenv("HOME")+"/.pinna/bios/"+real_artist)
      bio=temp.read()
      temp.close()
    else:
      url='http://www.last.fm/music/'+artist+'/+wiki'
      print url
      u=urllib2.urlopen(url)
      data=u.read()
      start=data.find('<div id="wiki">')+36
      end=data.find('</div><!-- #wiki -->')
      data=data[start:end]
      bio=format_text(data)
      temp=open(os.getenv("HOME")+"/.pinna/bios/"+real_artist,'w')
      temp.write(bio)
      temp.close()
  infowindow_wTree.get_widget('info_textview').get_buffer().set_text(bio)

def get_albumart(widget):
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
    print data
    u=urllib2.urlopen(data)
    picture=u.read()
    u.close()
    image_file=open(os.getenv("HOME")+"/.pinna/album_art/"+file_name, 'w')
    image_file.write(picture)
    image_file.close()

    infowindow_wTree.get_widget('album_art').set_from_file(os.getenv("HOME")+"/.pinna/album_art/"+file_name)
    mainwindow_wTree.get_widget("main_window_album_art").set_from_pixbuf(gtk.gdk.pixbuf_new_from_file(os.getenv("HOME")+"/.pinna/album_art/"+file_name).scale_simple(80,80,gtk.gdk.INTERP_BILINEAR))

def close(widget,event):
  infowindow_wTree.get_widget('info_window').hide()
  return True

if not os.path.isdir(os.getenv("HOME")+"/.pinna"):
  os.mkdir(os.getenv("HOME")+"/.pinna")
if not os.path.isdir(os.getenv("HOME")+"/.pinna/album_art"):
  os.mkdir(os.getenv("HOME")+"/.pinna/album_art")
if not os.path.isdir(os.getenv("HOME")+"/.pinna/bios"):
  os.mkdir(os.getenv("HOME")+"/.pinna/bios")
if not os.path.isdir(os.getenv("HOME")+"/.pinna/lyrics"):
  os.mkdir(os.getenv("HOME")+"/.pinna/lyrics")
  
def hotkeys(widget,event):
  keypress=event.keyval
  if keypress == 65470:
    get_lyrics(None)
  if keypress == 65471:
    get_artist_bio(None)
  if keypress == 65472:
    get_albumart(None)
  if keypress == 65307:
    close(None,None)
      
  
buttons={'on_info_window_delete_event':close,'on_lyric_button_clicked':get_lyrics,'on_albumart_button_clicked':get_albumart,'on_info_button_clicked':get_artist_bio,'on_info_window_key_press_event':hotkeys}

infowindow_wTree.signal_autoconnect(buttons)
