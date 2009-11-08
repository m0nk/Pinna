import urllib2
import os
import gtk
from xml.dom import minidom

from connection import client
from ui import mainwindow_wTree
from ui import infowindow_wTree
from ui import default_albumart
from variables import info_vars
from variables import settings 
from ui import notifier

def display_popup():
  current_song=client.currentsong()
  popup=[]          
  if 'title' in current_song.keys():
    if len(current_song['title'])<=30:
      popup.append(current_song['title'])
    else:
      popup.append(current_song['title'][0:30])
  else:
    insert=current_song['file'].split('/')
    insert=insert[len(insert)-1]
    if len(insert)<=30:
      popup.append(insert)
    else:
      popup.append(insert[0:30])
  if 'artist' in current_song.keys():
    popup.append('by '+current_song['artist'])
    if 'album' in current_song.keys():
      if len(current_song['album']+' on ')<=30:
        popup[1]+=' on '+current_song['album']
      else:
        popup[1]+=' on '+current_song['album'][0:30]
    else:
      popup[1]+=' on unknown album'
  else:
    if len(popup)==2:
      popup[1]='by unknown artist '+popup[1]
    else:
      popup.append('by unknown artist on unknown album')
  notifier.update(popup[0],popup[1])
  notifier.show()


def change_info():
  song=client.currentsong()
  if info_vars.view=='lyrics':
    change_lyrics(None)
  if info_vars.view=='bio':
    change_biography(None)
  if 'album' in song.keys() and 'artist' in song.keys():
    infowindow_wTree.get_widget('album_entry').set_sensitive(True)
    infowindow_wTree.get_widget('from_file').set_sensitive(True)
  else:
    infowindow_wTree.get_widget('album_entry').set_sensitive(False)
    infowindow_wTree.get_widget('from_file').set_sensitive(False)
  display_popup()  

def set_albumart(main=True):
  song=client.currentsong()
  pixbuf=default_albumart
  if 'artist' in song.keys() and 'album' in song.keys():
    song=song['artist']+':'+song['album']+'.jpg'
    song=song.lower().replace(' ','+')
    song=song.replace('/','+')
    check=os.getenv("HOME")+"/.pinna/album_art/"+song
    if os.path.isfile(check):
      pixbuf = gtk.gdk.pixbuf_new_from_file(check)
  if main==True:
    mainwindow_wTree.get_widget('main_window_album_art').set_from_pixbuf(pixbuf.scale_simple(80,80,gtk.gdk.INTERP_BILINEAR))
  infowindow_wTree.get_widget('info_textview').get_buffer().insert_pixbuf(infowindow_wTree.get_widget('info_textview').get_buffer().get_iter_at_line_offset(0,0),pixbuf)
  notifier.set_icon_from_pixbuf(pixbuf.scale_simple(40,40,gtk.gdk.INTERP_BILINEAR))

  
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
    infowindow_wTree.get_widget('info_textview').get_buffer().set_text('\n'+lyrics)
    temp.close()
  else:
    infowindow_wTree.get_widget('info_textview').get_buffer().set_text('')
  set_albumart()
  
def change_biography(widget):
  info_vars.view='bio'
  song=client.currentsong()
  artist=song['artist'].replace(' ','+')
  artist=artist.lower().replace('/','+')
  if os.path.isfile(os.getenv("HOME")+'/.pinna/bios/'+artist):
    temp=open(os.getenv("HOME")+'/.pinna/bios/'+artist)
    infowindow_wTree.get_widget('info_textview').get_buffer().set_text('\n'+temp.read())
    temp.close()
  else:
    infowindow_wTree.get_widget('info_textview').get_buffer().set_text('')
  set_albumart()
  
def format_text(data):
  charcters={'&#8216;':"'",'&#8217;':"'",'&#8220;':'"','&#8221;':'"','&#lt;':'<','&gt;':'>','&quot;':'"','&amp;':'&','&nbsp;':'','&quot;':"'"}
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

def scrape_leoslyrics():
  artist=infowindow_wTree.get_widget('artist_entry').get_text().replace(' ','%20')
  title=infowindow_wTree.get_widget('title_entry').get_text().replace(' ','%20')
  cnode=minidom.parse(urllib2.urlopen('http://api.leoslyrics.com/api_search.php?auth=pinna&artist="'+artist+'"&songtitle="'+title+'"')).getElementsByTagName('result')[0]
  if cnode.getAttribute('exactMatch')=='true':
    lyric_id=cnode.getAttribute('id')
    save_lyrics(minidom.parse(urllib2.urlopen('http://api.leoslyrics.com/api_lyrics.php?auth=pinna&id='+lyric_id)).getElementsByTagName('text')[0].firstChild.data)
  else:
    save_lyrics('')

def scrape_lyrdb():
  artist=infowindow_wTree.get_widget('artist_entry').get_text().replace(' ','%20')
  title=infowindow_wTree.get_widget('title_entry').get_text().replace(' ','%20')
  url='http://webservices.lyrdb.com/lookup.php?q='+artist+'|'+title+'&for=match&agent=pinna'
  u=urllib2.urlopen(url)
  u=urllib2.urlopen('http://webservices.lyrdb.com/getlyr.php?q='+u.read().split('\n')[0].split('\\')[0])
  data=u.read()
  if data.split('\n')[0][0:5]!='error':
    save_lyrics(format_text(data))
  else:
    save_lyrics('')

def scrape_lyricwiki():
  try:
    artist=infowindow_wTree.get_widget('artist_entry').get_text().replace(' ','+')
    title=infowindow_wTree.get_widget('title_entry').get_text().replace(' ','+')
    query=artist+':'+title
    url='http://lyrics.wikia.com/Special:Search?search='+query+'&go=1'
    u=urllib2.urlopen(url)
    data=u.read()
    u.close()

    def get_lyrics(data):
      data=data[data.find("<div class='lyricbox'>"):] 
      data=data[:data.find('<!--')-1]
      data=data[data.find('</div')+6:]
      data=data.replace('<br />','&#10;')
      lyrics=''
      for digit in data.split(';'):
        lyrics+=unichr(int(digit[2:len(digit)]))
      return lyrics

    if data.find("<div class='lyricbox'>")==-1:
      data=data[data.find("<hr/><ul class='mw-search-results'>"):]
      data=data[data.find('"')+1:]
      data=data[:data.find('"')]
      data=data.replace(' ','_')
      u=urllib2.urlopen(data)
      save_lyrics(get_lyrics(u.read()))
      u.close()
    else:
      save_lyrics(get_lyrics(data))
  
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
  change_lyrics(None)

def save_albumart(artwork):
  song=client.currentsong()
  file_name=song['artist']+':'+song['album']
  file_name=file_name.lower().replace(' ','+')
  file_name=file_name.replace('/','+')
  file_name=os.getenv("HOME")+'/.pinna/album_art/'+file_name+'.jpg'
  temp=open(file_name,'w')
  temp.write(artwork)
  temp.close()
  infowindow_wTree.get_widget('info_textview').get_buffer().delete(infowindow_wTree.get_widget('info_textview').get_buffer().get_iter_at_line_offset(0,0),infowindow_wTree.get_widget('info_textview').get_buffer().get_iter_at_line_offset(0,1))
  set_albumart()
  
def scrape_rhapsody(artist,album):
  artist=artist.replace(' ','-')
  album=album.replace(' ','-')
  print 'rhapsody'
  url='http://rhapsody.com/'+artist+'/'+album+'/data.xml'
  print url
  cnodes=minidom.parse(urllib2.urlopen(url)).childNodes
  if len(cnodes)>1:
    cnodes=cnodes[1]
    art_work=cnodes.getElementsByTagName('album-art')
    for art in art_work:
      if art.getAttribute('size')=='large':
        url=art.getElementsByTagName('img')[0].getAttribute('src')
    if url[len(url)-4:len(url)]=='.jpg':
      u=urllib2.urlopen(url)
      save_albumart(u.read())
      u.close()
    print url
    return True
  else:
    return False

def scrape_amazon(artist,album):
  artist=artist.replace(' ','+')
  album=album.replace(' ','+')
  print '\n'
  url="http://musicbrainz.org/ws/1/release/?type=xml&artist='"+artist+"'&title='"+album+"'"
  print url
  xmldoc=minidom.parse(urllib2.urlopen(url))
  cnodes=xmldoc.childNodes[0]
  amazon_id=cnodes.getElementsByTagName('asin')[0].firstChild.data
  amazon_url='http://ec1.images-amazon.com/images/P/'+amazon_id+'.01.SS170.jpg'
  print amazon_url
  if str(amazon_id[0])!=' ':
    u=urllib2.urlopen(amazon_url)
    save_albumart(u.read())
    u.close()

def scrape_albumart():
  song=client.currentsong()
  if 'artist' in song.keys() and 'album' in song.keys():
    artist=infowindow_wTree.get_widget('artist_entry').get_text()
    album=infowindow_wTree.get_widget('album_entry').get_text()
    try:
      if not scrape_rhapsody(artist,album):
        try:
          scrape_amazon(artist,album)
        except:
          pass      
    except:
      try:
        scrape_amazon(artist,album)
      except:
        pass

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
    if infowindow_wTree.get_widget('lyricsite').get_active()==3:
      scrape_leoslyrics()
    if infowindow_wTree.get_widget('lyricsite').get_active()==2:
      scrape_lyrdb()
  if infowindow_wTree.get_widget('search_for').get_active()==1:
    scrape_albumart()
  if infowindow_wTree.get_widget('search_for').get_active()==2:
    if infowindow_wTree.get_widget('lyricsite').get_active()==1:
      scrape_lyricwiki()
    if infowindow_wTree.get_widget('lyricsite').get_active()==0:
      scrape_lyricsplugin()
    if infowindow_wTree.get_widget('lyricsite').get_active()==2:
      scrape_lyrdb()
    if infowindow_wTree.get_widget('lyricsite').get_active()==3:
      scrape_leoslyrics()
  if infowindow_wTree.get_widget('search_for').get_active()==3:
    scrape_artistbio(True)

def showsearch_window(widget):
  infowindow_wTree.get_widget('search_window').show_all()

def close_infowindow(widget,event):
  widget.hide_all()
  return True

def search_for_changed(widget):
  if infowindow_wTree.get_widget('search_for').get_active()!=0 and infowindow_wTree.get_widget('search_for').get_active()!=2:
    infowindow_wTree.get_widget('lyricsite').set_sensitive(False)
  else:
    infowindow_wTree.get_widget('lyricsite').set_sensitive(True)

def searchwindow_event(widget,event):
  if event.keyval==65307:
    widget.hide_all()

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
  widget.hide_all()
  return True

if not os.path.isdir(os.getenv("HOME")+'/.pinna'):
  os.mkdir(os.getenv("HOME")+'/.pinna')
if not os.path.isdir(os.getenv("HOME")+'/.pinna/bios'):
  os.mkdir(os.getenv("HOME")+'/.pinna/bios')
if not os.path.isdir(os.getenv("HOME")+'/.pinna/album_art'):
  os.mkdir(os.getenv("HOME")+'/.pinna/album_art')
if not os.path.isdir(os.getenv("HOME")+'/.pinna/lyrics'):
  os.mkdir(os.getenv("HOME")+'/.pinna/lyrics')

def initiate_filechooser(first=False):
  chooser=infowindow_wTree.get_widget('filechooser')
  if first==True:
    file_filter=gtk.FileFilter()
    file_filter.set_name('Images')
    file_filter.add_mime_type("image/png")
    file_filter.add_mime_type("image/jpg")
    file_filter.add_pattern("*.jpg")
    file_filter.add_pattern("*.gif")
    file_filter.add_pattern("*.bmp")
    chooser.add_filter(file_filter)
  else:
    if settings.music_directory:
      chooser.set_current_folder(settings.music_directory)
    else:
      chooser.set_current_folder(os.getenv("HOME"))
    chooser.show()

def filechooser_ok(widget):
  song=client.currentsong()
  song=song['artist']+':'+song['album']+'.jpg'
  song=song.lower().replace(' ','+')
  song=song.replace('/','+')
  width=170
  height=170
  image_file=gtk.gdk.pixbuf_new_from_file_at_size(infowindow_wTree.get_widget('filechooser').get_filename(),width,height)
  infowindow_wTree.get_widget('info_textview').get_buffer().delete(infowindow_wTree.get_widget('info_textview').get_buffer().get_iter_at_line_offset(0,0),infowindow_wTree.get_widget('info_textview').get_buffer().get_iter_at_line_offset(0,1))
  image_file.save(os.getenv("HOME")+'/.pinna/album_art/'+song,'jpeg')
  set_albumart()
  infowindow_wTree.get_widget('filechooser').hide()
  return True

def show_filechooser(widget):
  initiate_filechooser()

def close_filechooser(widget,event=None):
  widget.hide()
  return True

initiate_filechooser(True)
infowindow_wTree.get_widget('filechooser').hide()

buttons={'on_lyric_button_clicked':change_lyrics,'on_artist_button_clicked':change_biography,'on_search_button_clicked':showsearch_window,'on_info_window_delete_event':close_infowindow,'on_info_window_key_press_event':infowindow_event}
search_buttons={'on_search1_button_clicked':search,'on_search_window_delete_event':close_searchwindow,'on_search_for_changed':search_for_changed,'on_search_window_key_press_event':searchwindow_event,'on_from_file_clicked':show_filechooser}
filechooser_buttons={'on_filechooser_delete_event':close_filechooser,'on_file_ok_clicked':filechooser_ok,'on_file_cancel_clicked':close_filechooser}

infowindow_wTree.get_widget('lyricsite').set_active(0)
infowindow_wTree.get_widget('search_for').set_active(0)

infowindow_wTree.signal_autoconnect(search_buttons)
infowindow_wTree.signal_autoconnect(buttons)
infowindow_wTree.signal_autoconnect(filechooser_buttons)
