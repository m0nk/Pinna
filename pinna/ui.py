import gtk
import gtk.glade
import os
import pynotify

if os.path.dirname(__file__):
  root_path=os.path.dirname(__file__)+"/"
else:
  root_path=""

def init_notifier():
  pynotify.init('pinna song notification')
  notifier=pynotify.Notification('testtickles')
  notifier.set_urgency(pynotify.URGENCY_LOW)
  notifier.set_timeout(3000)
  return notifier

class dialog_input:
  def __init__(self,title,parent,message):
    self.dialog = gtk.MessageDialog(
        parent,
        gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
        gtk.MESSAGE_QUESTION,
        gtk.BUTTONS_OK_CANCEL,
        None)
    #dialog.title(title)
    self.entry=gtk.Entry()
    self.entry.connect("activate", self.enter_callback,self.dialog, gtk.RESPONSE_OK)
    if message:
      self.dialog.set_markup(message)
    self.dialog.vbox.pack_end(self.entry, True, True, 0)

  def enter_callback(self,entry,dialog,response):
    dialog.response(response)

  def run(self):
    self.dialog.show_all()
    signal=self.dialog.run()
    if signal==-4 or signal==-6:
      self.dialog.hide_all()
      self.entry.set_text('')
      return None
    elif signal==-5:
      text=self.entry.get_text()
      if text.strip(' '):
        self.entry.set_text('')
        self.dialog.hide_all()
        return text
      else:
        self.entry.set_text('')
        self.run()
    else:
      self.run()

class ask_yes_no:
  def __init__(self,title,parent,message):
    self.dialog=gtk.MessageDialog(
      parent,
      gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
      gtk.MESSAGE_QUESTION,
      gtk.BUTTONS_YES_NO,
      None)
    if message:
      self.dialog.set_markup(message)
  
  def run(self):
    signal=self.dialog.run()    
    if signal==-8:
      self.dialog.hide_all()
      return True
    elif signal==-4 or signal==-9:
      self.dialog.hide_all()
      return False

mainwindow_wTree=gtk.glade.XML(root_path+"glade/main_window.glade")
settingswindow_wTree=gtk.glade.XML(root_path+"glade/settings_window.glade")
browserwindow_wTree=gtk.glade.XML(root_path+"glade/browser_window.glade")
infowindow_wTree=gtk.glade.XML(root_path+"glade/info_window.glade")
default_albumart=gtk.gdk.pixbuf_new_from_file(root_path+"glade/no_image.png")

notifier=init_notifier()

tray_icon=gtk.StatusIcon()
tray_icon.set_from_file(root_path+'glade/no_image.png')

browser_popups=(dialog_input(None,browserwindow_wTree.get_widget('brwoser_window'),'Please enter a name for the playlist:'),
  ask_yes_no(None,browserwindow_wTree.get_widget('browser_window'),'Are you sure?'))
