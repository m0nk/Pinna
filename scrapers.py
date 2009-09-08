import os
import urllib2
from connection import client
from ui import infowindow_wTree

#def check_album_art():
#  song=client.currentsong()
#  check=os.getenv("HOME")+"/.pinna/album_art/"+song['artist'].lower()+':'+song['album'].lower()+'.jpg'
#  check=check.replace(" ","+")

def change_song():
  song=client.currentsong()
  albm_art_check=os.getenv("HOME")+"/.pinna/album_art/"+song['artist'].lower()+":"+song['album'].lower()+'.jpg'
  album_art_check=album_art_check.replace(' ','+')
  print os.getenv("HOME")+"/.pinna/lyrics"+file_name[0:len(file_name)-3]+'txt'
  infowindow_wTree.get_widget('info_textview').get_buffer().set_text('')
  reutrn album_art_check
  
def get_lyrics():
  file_name=client.currentsong()['file']
  if os.getenv("HOME")+"/.pinna/lyrics"+file_name+'.txt':
    temp=open(os.getenv("HOME")+"/.pinna/lyrics"+file_name+'.txt')
    lyrics=temp.read()
    infowindow_wTree.get_widget('info_textview').get_buffer().set_text(lyrics)
    
if not os.path.isdir(os.getenv("HOME")+"/.pinna"):
  os.mkdir(os.getenv("HOME")+"/.pinna")
if not os.path.isdir(os.getenv("HOME")+"/.pinna/album_art"):
  os.mkdir(os.getenv("HOME")+"/.pinna/album_art")
if not os.path.isdir(os.getenv("HOME")+"/.pinna/bios"):
  os.mkdir(os.getenv("HOME")+"/.pinna/bios")
if not os.path.isdir(os.getenv("HOME")+"/.pinna/lyrics"):
  os.mkdir(os.getenv("HOME")+"/.pinna/lyrics")
  

