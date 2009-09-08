import os
import urllib2
from connection import client

def check_album_art():
  song=client.currentsong()
  check=os.getenv("HOME")+"/.pinna/album_art/"+song['artist'].lower()+':'+song['album'].lower()+'.jpg'
  check=check.replace(" ","+")
  print check
  if os.path.isfile(check):
    return check
  else:
    return None

if not os.path.isdir(os.getenv("HOME")+"/.pinna"):
  os.mkdir(os.getenv("HOME")+"/.pinna")
if not os.path.isdir(os.getenv("HOME")+"/.pinna/album_art"):
  os.mkdir(os.getenv("HOME")+"/.pinna/album_art")
if not os.path.isdir(os.getenv("HOME")+"/.pinna/bios"):
  os.mkdir(os.getenv("HOME")+"/.pinna/bios")
if not os.path.isdir(os.getenv("HOME")+"/.pinna/lyrics"):
  os.mkdir(os.getenv("HOME")+"/.pinna/lyrics")
