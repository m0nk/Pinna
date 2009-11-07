from ui import browserwindow_wTree
import gtk
from variables import checks
from variables import browser_vars
from connection import client
from ui import browser_popups
#playlist code

def change_playlist():
  browser_vars.playlist_list=[None,[]]
  playlists=client.lsinfo('')
  model=browserwindow_wTree.get_widget('browser_list').get_model()
  model.clear()
  browserwindow_wTree.get_widget('browser_list').set_model(None)
  for playlist in playlists:
    if 'playlist' in playlist.keys():
      model.append([gtk.STOCK_FILE,playlist['playlist']])
      browser_vars.playlist_list[1].append(playlist['playlist'])
  browserwindow_wTree.get_widget('browser_list').set_model(model)

def add_playlist(widget):
  client.clear()
  selection=browserwindow_wTree.get_widget('browser_list').get_selection().get_selected_rows()[1][0][0]
  client.load(browser_vars.playlist_list[1][selection])

def merge_playlist(widget):
  selections=browserwindow_wTree.get_widget('browser_list').get_selection().get_selected_rows()[1][0]
  for selection in selections:
    client.load(browser_vars.playlist_list[1][selection])

def delete_playlist(widget):
  if browser_popups[1].run()==True:
    selections=browserwindow_wTree.get_widget('browser_list').get_selection().get_selected_rows()[1][0]
    for selection in selections:
      client.rm(browser_vars.playlist_list[1][selection])
    browser_vars.playlist_list=[[],None]
    change_playlist()
      
#current playlist code
def change_current():
  model=browserwindow_wTree.get_widget('browser_list').get_model()
  browserwindow_wTree.get_widget('browser_list').set_model(None)
  model.clear()
  if browser_vars.current_playlist[1]:
    for song in browser_vars.current_playlist[1]:
      model.append([gtk.STOCK_CDROM,song])
  if checks.last_song:
    if checks.last_song[2] in browser_vars.current_playlist[2]:
      model.set_value(model.get_iter(checks.last_song[0]),1,'<b>'+checks.last_song[1]+'</b>')
  browserwindow_wTree.get_widget('browser_list').set_model(model)

def current_play(widget):
  selection=browserwindow_wTree.get_widget('browser_list').get_selection().get_selected_rows()[1][0][0]
  client.play(selection)

def current_delete(widget):
  selections=browserwindow_wTree.get_widget('browser_list').get_selection().get_selected_rows()[1]
  new_selections=[]
  for selection in selections:
    new_selections.append(selection[0])
  new_selections.sort(reverse=True)
  for selection in new_selections:
    client.delete(selection)

def create_playlist_show(widget):
  playlist_name=browser_popups[0].run()
  client.save(playlist_name)
  browser_vars.playlist_list[1].append(playlist_name)

def current_clear(widget):
  client.clear()
  
#file browser code
def change_browser():
  if browser_vars.browser_list[1]:
    insert_items()
  else:
    change_directory('')
    
def change_directory(new_directory):
  format_browser_vars(client.lsinfo(new_directory))
  if browser_vars.view=='file':
    insert_items()

def browser_open(widget):
  selections=browserwindow_wTree.get_widget('browser_list').get_selection().get_selected_rows()[1][0]
  selection=selections[0]
  change_directory(browser_vars.browser_list[1][selection][2])

def browser_doubleclick():
  selections=browserwindow_wTree.get_widget('browser_list').get_selection().get_selected_rows()[1][0]
  if browser_vars.browser_list[1][selections[0]][0]=='file':
    if browser_vars.browser_list[1][selections[0]][2] not in browser_vars.current_playlist[2]:
      client.add(browser_vars.browser_list[1][selections[0]][2])
    else:
      client.play(browser_vars.current_playlist[2].index(browser_vars.browser_list[1][selections[0]][2]))
  if browser_vars.browser_list[1][selections[0]][0]=='directory':
    change_directory(browser_vars.browser_list[1][selections[0]][2])

### universal code
def insert_items():
  model=browserwindow_wTree.get_widget('browser_list').get_model()
  model.clear()
  browserwindow_wTree.get_widget('browser_list').set_model(None)
  for song in browser_vars.browser_list[1]:
    if song[0]=='directory':
      model.append([gtk.STOCK_DIRECTORY,song[1]])
    if song[0]=='file':
      model.append([gtk.STOCK_CDROM,song[1]])
  set_highlights(model)
  browserwindow_wTree.get_widget('browser_list').set_model(model)

def set_highlights(model):
  for song in browser_vars.browser_list[1]:
    if song[0]=='file' and song[2] in browser_vars.current_playlist[2]:
      index=browser_vars.browser_list[2].index(song[2])
      liter=model.get_iter(index)
      if checks.last_song and song[2] == checks.last_song[2]:
        model.set_value(liter,1,'<i><b>'+song[1]+'</b></i>')
      else:
        model.set_value(liter,1,'<b>'+song[1]+'</b>')

def format_browser_vars(song_info,search=False):
  browser_vars.browser_list=[None,[],[]]
  for song in song_info:
    if len(browser_vars.browser_list[1])==0:
      if 'file' in song.keys() and search==False or 'directory' in song.keys() and search==False:
        if 'file' in song.keys():
          item='file'
        if 'directory' in song.keys():
          item='directory'
        if ''+'/'.join(song[item].split('/')[0:len(song[item].split('/'))-1]):
          up_directory=''+'/'.join(song[item].split('/')[0:len(song[item].split('/'))-2])
          if not up_directory:
            up_directory=''
          browser_vars.browser_list[1].append(('directory','[ .. ]',up_directory))
          browser_vars.browser_list[2].append('****FILLER****')
      if search==True:
        browser_vars.browser_list[1].append(('directory','[ END SEARCH ]',''))    
        browser_vars.browser_list[2].append('****FILLER****')

    if 'directory' in song.keys():
      file_type='directory'
      path=song['directory']
      display=song['directory'].split('/')[len(song['directory'].split('/'))-1]
    if 'file' in song.keys():
      file_type='file'
      path=song['file']
      if 'artist' in song.keys() and 'title' in song.keys():
        display=song['artist']+' - '+song['title']
      else:
        display=song['file'].split('/')[len(song['file'].split('/'))-1]
    if 'playlist' not in song.keys():
      browser_vars.browser_list[1].append((file_type,display.replace('&','&amp;'),path))
      browser_vars.browser_list[2].append(path)

def handle_scrollbars(view,work='save'):
  if view=='file':
    item=browser_vars.browser_list
  if view=='playlist':
    item=browser_vars.playlist_list
  if view=='current':
    item=browser_vars.current_playlist
  if work=='save':
    adj=browserwindow_wTree.get_widget('browser_scroll').get_vadjustment()
    item[0]=(adj.value,adj.page_size,adj.lower,adj.upper)
  if work=='read':
    if item[0]:
      adj=browserwindow_wTree.get_widget('browser_scroll').get_vadjustment()
      adj.lower=item[0][0]
      adj.value=item[0][0]
      adj.page_size=item[0][1]
      adj.upper=item[0][3]-item[0][2]+item[0][0]    
      browserwindow_wTree.get_widget('browser_scroll').set_vadjustment(adj)
### end universal code
      
def smart_add(directory):
  songs=client.lsinfo(directory)
  for song in songs:
    if 'directory' in song.keys():
      smart_add(song['directory'])
    if 'file' in song.keys() and song['file'] not in browser_vars.current_playlist[2]:
      client.add(song['file'])

def browser_add(widget):
  model=browserwindow_wTree.get_widget('browser_list').get_model()
  selections=browserwindow_wTree.get_widget('browser_list').get_selection().get_selected_rows()[1]
  for selection in selections:
    if browser_vars.browser_list[1][selection[0]][0]=='file': 
      if browser_vars.browser_list[1][selection[0]][2] not in browser_vars.current_playlist[2]:
        client.add(browser_vars.browser_list[1][selection[0]][2])
    if browser_vars.browser_list[1][selection[0]][0]=='directory':
      smart_add(browser_vars.browser_list[1][selection[0]][2])

def update_database(widget):
  client.update()

def search(widget):
 if browserwindow_wTree.get_widget('browser_mode').get_active()==1:
  query = browserwindow_wTree.get_widget('search_query').get_text()
  term = browserwindow_wTree.get_widget('search_item').get_active_text()
  format_browser_vars(client.search(term,query),True)
  if browser_vars.view=='file':
    insert_items()
 
#bs 
def close_browser(widget,event):
  widget.hide_all()
  return True

def disable_search():
  browserwindow_wTree.get_widget('search_query').set_sensitive(False)
  browserwindow_wTree.get_widget('search_item').set_sensitive(False)
  browserwindow_wTree.get_widget('search_button').set_sensitive(False)

def enable_search():
  browserwindow_wTree.get_widget('search_query').set_sensitive(True)
  browserwindow_wTree.get_widget('search_item').set_sensitive(True)
  browserwindow_wTree.get_widget('search_button').set_sensitive(True)

def change_browse_mode(widget):
  handle_scrollbars(browser_vars.view,'save')
  selection=widget.get_active_text().strip('\n')
  if selection=='File':
    enable_search()
    change_browser()
    browser_vars.view='file'
    browserwindow_wTree.get_widget('browser_window').set_title('Pinna - File Browser')
  if selection=='Current':
    disable_search()
    change_current()
    browser_vars.view='current'
    browserwindow_wTree.get_widget('browser_window').set_title('Pinna - Current Browser')
  if selection=='Playlist':
    disable_search()
    browser_vars.view='playlist'
    change_playlist()
    browserwindow_wTree.get_widget('browser_window').set_title('Pinna - Playlist Browser')
  handle_scrollbars(browser_vars.view,'read')

def treeview_event(widget,event):
  #left double click
  if event.type==gtk.gdk._2BUTTON_PRESS and event.button==1:
    if browser_vars.view=='current':
      current_play(None)    
    if browser_vars.view=='file':
      browser_doubleclick()
    if browser_vars.view=='playlist':
      merge_playlist(None)
    return True
  #right click
  if event.type==gtk.gdk.BUTTON_PRESS and event.button==3:
    variable=True
    if browser_vars.view=='file':
      browserwindow_wTree.get_widget('file_menu').popup(None,None,None,event.button,event.time)
    elif browser_vars.view=='current':
      browserwindow_wTree.get_widget('current_menu').popup(None,None,None,event.button,event.time)
    elif browser_vars.view=='playlist':
      browserwindow_wTree.get_widget('playlist_menu').popup(None,None,None,event.button,event.time)
    else:
      variable=False
    return variable

def browser_list_hotkey(widget,event):
  keypress=event.keyval
  if keypress == 65535: #delete
    if browser_vars.view == 'current':
      current_delete(None)
    if browser_vars.view == 'playlist':
      delete_playlist(None)
    
  if keypress == 65470: #F1
    browserwindow_wTree.get_widget('browser_mode').set_active(0)
  if keypress == 65471: #F2
    browserwindow_wTree.get_widget('browser_mode').set_active(1)
  if keypress == 65472: #F3
    browserwindow_wTree.get_widget('browser_mode').set_active(2)
  
  if keypress == 65307: #escape
    browserwindow_wTree.get_widget('browser_window').hide_all()

  if keypress == 65379: #insert
    if browser_vars.view=='browser':
      browser_add(None)
    if browser_vars.view=='playlist':
      merge_playlist(None)
  return True
    
liststore=gtk.ListStore(str,str)

browserwindow_wTree.get_widget("browser_list").set_model(liststore)
image_cell=gtk.CellRendererPixbuf()
text_cell=gtk.CellRendererText()
column=gtk.TreeViewColumn('song listing')

column.pack_start(image_cell,False)
column.set_attributes(image_cell,stock_id=0)
column.pack_start(text_cell,True)
column.set_attributes(text_cell,markup=1)

browserwindow_wTree.get_widget('browser_list').append_column(column)

browserwindow_wTree.get_widget("browser_list").get_selection().set_mode(gtk.SELECTION_MULTIPLE)
browserwindow_wTree.get_widget('browser_list').freeze_child_notify()

browser_vars.view='current'
browserwindow_wTree.get_widget('browser_mode').set_active(0)
browserwindow_wTree.get_widget('search_item').set_active(0)

events={'on_browser_list_button_press_event':treeview_event,'on_browser_list_key_press_event':browser_list_hotkey}

shared_buttons={'on_browser_mode_changed':change_browse_mode,'browser_window_destroy':close_browser}
current_buttons={'play_clicked':current_play,'clear_clicked':current_clear,'delete_clicked':current_delete,'create_playlist_clicked':create_playlist_show}
file_buttons={'open_clicked':browser_open,'add_clicked':browser_add,'update_DB_clicked':update_database,'on_search_button_clicked':search}

playlist_buttons={'add_playlist_clicked':add_playlist,'merge_playlist_clicked':merge_playlist,'delete_playlist_clicked':delete_playlist}

try:
  disable_search()
  change_current()
  change_directory('')
except:
  pass

browserwindow_wTree.signal_autoconnect(file_buttons)
browserwindow_wTree.signal_autoconnect(events)
browserwindow_wTree.signal_autoconnect(shared_buttons)
browserwindow_wTree.signal_autoconnect(current_buttons)
browserwindow_wTree.signal_autoconnect(playlist_buttons)
browserwindow_wTree.get_widget('browser_window').show_all()
