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
  print check
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
  check=os.getenv("HOME")+"/.pinna/lyrics/"+file_nae[0:len(file_name)-3]+'txt'
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
  pass

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
  
buttons={'on_info_window_delete_event':close}

infowindow_wTree.signal_autoconnect(buttons)
