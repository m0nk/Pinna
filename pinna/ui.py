import gtk
import gtk.glade
import os
import pynotify

if os.path.dirname(__file__):
  root_path=os.path.dirname(__file__)+"/"
else:
  root_path=""

def init_notifier():
  print 'notifier is made'
  pynotify.init('pinna song notification')
  notifier=pynotify.Notification('testtickles')
  notifier.set_urgency(pynotify.URGENCY_LOW)
  notifier.set_timeout(3000)
  notifier.set_hint("x",0)
  notifier.set_hint('y',0)
  return notifier

mainwindow_wTree=gtk.glade.XML(root_path+"glade/main_window.glade")

settingswindow_wTree=gtk.glade.XML(root_path+"glade/settings_window.glade")

browserwindow_wTree=gtk.glade.XML(root_path+"glade/browser_window.glade")

infowindow_wTree=gtk.glade.XML(root_path+"glade/info_window.glade")

default_albumart=gtk.gdk.pixbuf_new_from_file(root_path+"glade/no_image.png")

notifier=init_notifier()

tray_icon=gtk.StatusIcon()
tray_icon.set_from_file(root_path+'glade/no_image.png')
