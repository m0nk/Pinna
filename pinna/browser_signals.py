from ui import browserwindow_wTree
import gtk
from variables import checks
from variables import browser_vars
import gtk.gdk
from connection import client

#playlist code

def change_playlist():
  if not browser_vars.playlist_list[1]:
    playlists=client.lsinfo('')
    for playlist in playlists:
      if 'playlist' in playlist.keys():
        browser_vars.playlist_list[1].append(playlist['playlist'])
  if browser_vars.view=='playlist':
    model=browserwindow_wTree.get_widget('browser_list').get_model()
    browserwindow_wTree.get_widget('browser_list').set_model()
    model.clear()
    for item in browser_vars.playlist_list[1]:
      model.append([item])
    browserwindow_wTree.get_widget('browser_list').set_model(model)  
    if browser_vars.playlist_list[0]:
      adj=browserwindow_wTree.get_widget('browser_scroll').get_vadjustment()
      adj.lower=browser_vars.playlist_list[0][0]
      adj.upper=browser_vars.playlist_list[0][3]-browser_vars.current_playlist[0][2]+browser_vars.current_playlist[0][0]
      adj.value=browser_vars.playlist_list[0][0]
      adj.page_size=browser_vars.playlist_list[0][1]
       
def add_playlist(widget):
  client.clear()
  selection=browserwindow_wTree.get_widget('browser_list').get_selection().get_selected_rows()[1][0][0]
  client.load(browser_vars.playlist_list[1][selection])

def merge_playlist(widget):
  selections=browserwindow_wTree.get_widget('browser_list').get_selection().get_selected_rows()[1][0]
  for selection in selections:
    client.load(browser_vars.playlist_list[1][selection])

def delete_playlist(widget):
  browserwindow_wTree.get_widget('ask_yes_no').show() 
  
def ok_clicked(widget):
  selections=browserwindow_wTree.get_widget('browser_list').get_selection().get_selected_rows()[1][0]
  for selection in selections:
    client.rm(browser_vars.playlist_list[1][selection])
  browser_vars.playlist_list[1]=[]
  browser_vars.playlist_list[0]=None
  change_playlist()
  browserwindow_wTree.get_widget('ask_yes_no').hide()
  return True
  
def cancel_button(widget):
  browserwindow_wTree.get_widget('ask_yes_no').hide()
  return True
      
#current playlist code

def change_current():
  model=browserwindow_wTree.get_widget('browser_list').get_model()
  browserwindow_wTree.get_widget('browser_list').set_model()
  model.clear()
  if browser_vars.current_playlist[1]:
    for song in browser_vars.current_playlist[1]:
      model.append([song])
  browserwindow_wTree.get_widget('browser_list').set_model(model)
  if browser_vars.current_playlist[0]:
    adj=browserwindow_wTree.get_widget('browser_scroll').get_vadjustment()
    adj.lower=browser_vars.current_playlist[0][0]
    adj.upper=browser_vars.current_playlist[0][3]-browser_vars.current_playlist[0][2]+browser_vars.current_playlist[0][0]
    adj.value=browser_vars.current_playlist[0][0]
    adj.page_size=browser_vars.current_playlist[0][1]
    browserwindow_wTree.get_widget('browser_scroll').set_vadjustment(adj)
    
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
  browserwindow_wTree.get_widget('ask_user_input').show()

def create_playlist_ok(widget):
  playlist_name=browserwindow_wTree.get_widget('user_input_entry').get_text()
  client.save(playlist_name)
  browserwindow_wTree.get_widget('ask_user_input').hide()
  browserwindow_wTree.get_widget('user_input_entry').set_text('')
  browser_vars.playlist_list[1].append(playlist_name)
  change_playlist()
  return True
  
def create_playlist_cancel(widget):
  browserwindow_wTree.get_widget('user_input_entry').set_text('')
  browserwindow_wTree.get_widget('ask_user_input').hide()
  return True

def current_clear(widget):
  client.clear()
  browser_vars.current_playlist[0]=None
   
#file browser code

def change_browser():  
  if browser_vars.browser_list[1]:
    model=browserwindow_wTree.get_widget('browser_list').get_model()
    browserwindow_wTree.get_widget('browser_list').set_model()
    model.clear()
    for song in browser_vars.browser_list[1]:
      model.append([song[1]])
    browserwindow_wTree.get_widget('browser_list').set_model(model)
  else:
    change_directory('')
  #set scroll
  if browser_vars.browser_list[0]:
    adj=browserwindow_wTree.get_widget('browser_scroll').get_vadjustment()
    adj.lower=browser_vars.browser_list[0][0]
    adj.value=browser_vars.browser_list[0][0]
    adj.page_size=browser_vars.browser_list[0][1]
    adj.upper=browser_vars.browser_list[0][3]-browser_vars.browser_list[0][2]+browser_vars.browser_list[0][0]    
    browserwindow_wTree.get_widget('browser_scroll').set_vadjustment(adj)
    
def change_directory(new_directory):
  browser_vars.browser_list[1]=[]
  browser_vars.browser_list[0]=None
  chunks=client.lsinfo(new_directory)
  if new_directory:
    up_directory=''
    temp=new_directory.split('/')
    up_directory+='/'.join(temp[0:len(temp)-1])
    browser_vars.browser_list[1].append(('directory','[..]',up_directory))
  for item in chunks:
    if 'directory' in item.keys():
      file_type='directory'
      file_name=item['directory']
      display=file_name.split('/')
      display=display[len(display)-1].replace('&','&amp;')
      browser_vars.browser_list[1].append((file_type,display,file_name))
    if 'file' in item.keys():
      file_type='file'
      file_name=item['file']
      if 'artist' in item.keys() and 'title' in item.keys():
        display=item['artist']+' - '+item['title']
      else:
        display=file_name.split('/')
        display=display[len(display)-1]
      display=display.replace('&','&amp;')
      browser_vars.browser_list[1].append((file_type,display,file_name))
  if browser_vars.view=='file':
    model=browserwindow_wTree.get_widget('browser_list').get_model()
    browserwindow_wTree.get_widget('browser_list').set_model()
    model.clear()
    for item in browser_vars.browser_list[1]:
      model.append([item[1]])
    browserwindow_wTree.get_widget('browser_list').set_model(model)

def browser_open(widget):
  selections=browserwindow_wTree.get_widget('browser_list').get_selection().get_selected_rows()[1][0]
  selection=selections[0]
  change_directory(browser_vars.browser_list[1][selection][2])

def browser_doubleclick():
  selections=browserwindow_wTree.get_widget('browser_list').get_selection().get_selected_rows()[1][0]
  if browser_vars.browser_list[1][selections[0]][0]=='file':
    client.add(browser_vars.browser_list[1][selections[0]][2])
  if browser_vars.browser_list[1][selections[0]][0]=='directory':
    change_directory(browser_vars.browser_list[1][selections[0]][2])

def browser_add(widget):
  selections=browserwindow_wTree.get_widget('browser_list').get_selection().get_selected_rows()[1]
  for selection in selections:
    client.add(browser_vars.browser_list[1][selection[0]][2])

def update_database(widget):
  client.update()

def search(widget):
 if browserwindow_wTree.get_widget('browser_mode').get_active()==1:
  query = browserwindow_wTree.get_widget('search_query').get_text()
  term = browserwindow_wTree.get_widget('search_item').get_active_text()
  model=browserwindow_wTree.get_widget('browser_list').get_model()
  browserwindow_wTree.get_widget('browser_list').set_model()
  model.clear()
  browser_vars.browser_list[0]=None
  browser_vars.browser_list[1]=[]
  browser_vars.browser_list[1].append(('directory','[ END SEARCH ]',''))
  results = client.search(term,query)
  for result in results:
    if 'artist' in result.keys() and 'title' in result.keys():
      insert=result['artist']+' - '+result['title']
    else:
      insert=result['file'].split('/')
      insert=insert[len(insert)-1]
    browser_vars.browser_list[1].append(('file',insert.replace('&','&amp;'),result['file']))
  for song in browser_vars.browser_list[1]:
    model.append([song[1]])
  browserwindow_wTree.get_widget('browser_list').set_model(model)
 
#bs 
def close_browser(widget,event):
  browserwindow_wTree.get_widget('browser_window').hide()
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
  adj=browserwindow_wTree.get_widget('browser_scroll').get_vadjustment()
  if browser_vars.view=='file':
    browser_vars.browser_list[0]=(adj.value,adj.page_size,adj.lower,adj.upper)
  if browser_vars.view=='current':
    browser_vars.current_playlist[0]=(adj.value,adj.page_size,adj.lower,adj.upper)
  if browser_vars.view=='playlist':
    browser_vars.playlist_list[0]=(adj.value,adj.page_size,adj.lower,adj.upper)
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
    if browser_vars.view=='file':
      browserwindow_wTree.get_widget('file_menu').popup(None,None,None,event.button,event.time)
    if browser_vars.view=='current':
      browserwindow_wTree.get_widget('current_menu').popup(None,None,None,event.button,event.time)
    if browser_vars.view=='playlist':
      browserwindow_wTree.get_widget('playlist_menu').popup(None,None,None,event.button,event.time)
    return True

def browser_list_hotkey(wdiget,event):
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
    close_browser(None,None)
  
  if keypress == 65379: #insert
    if browser_vars.view=='browser':
      browser_add(None)
    if browser_vars.view=='playlist':
      merge_playlist(None)
  return True
    
liststore=gtk.ListStore(str)
browserwindow_wTree.get_widget("browser_list").set_model(liststore)
cell = gtk.CellRendererText()
column = gtk.TreeViewColumn("Pango Markup",cell,markup=0)
browserwindow_wTree.get_widget("browser_list").append_column(column)
browserwindow_wTree.get_widget("browser_list").get_selection().set_mode(gtk.SELECTION_MULTIPLE)
browserwindow_wTree.get_widget('browser_list').freeze_child_notify()

browser_vars.view='current'
browserwindow_wTree.get_widget('browser_mode').set_active(0)
browserwindow_wTree.get_widget('search_item').set_active(0)

events={'on_browser_list_button_press_event':treeview_event,'on_browser_list_key_press_event':browser_list_hotkey}

shared_buttons={'on_browser_mode_changed':change_browse_mode,'browser_window_destroy':close_browser}
current_buttons={'play_clicked':current_play,'clear_clicked':current_clear,'delete_clicked':current_delete,'create_playlist_clicked':create_playlist_show}
file_buttons={'open_clicked':browser_open,'add_clicked':browser_add,'update_DB_clicked':update_database,'on_search_button_clicked':search}

playlist_buttons={'user_input_destroy':create_playlist_cancel,'user_input_cancel_clicked_cb':create_playlist_cancel,'user_input_ok_clicked_cb':create_playlist_ok,
'add_playlist_clicked':add_playlist,'merge_playlist_clicked':merge_playlist,'delete_playlist_clicked':delete_playlist,'on_ok_button_clicked':ok_clicked,
'on_cancel_button_clicked':cancel_button}

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
