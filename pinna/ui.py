import gtk
import gtk.glade
import os

if os.path.dirname(__file__):
  root_path=os.path.dirname(__file__)+"/"
else:
  root_path=""


mainwindow_wTree=gtk.glade.XML(root_path+"glade/main_window.glade")

settingswindow_wTree=gtk.glade.XML(root_path+"glade/settings_window.glade")

browserwindow_wTree=gtk.glade.XML(root_path+"glade/browser_window.glade")

infowindow_wTree=gtk.glade.XML(root_path+"glade/info_window.glade")

default_albumart=gtk.gdk.pixbuf_new_from_file(root_path+"glade/no_image.png")

tray_menu=gtk.glade.XML(root_path+"glade/tray_popup.glade")
tray_icon=gtk.StatusIcon()
tray_icon.set_from_file(root_path+'glade/no_image.png')
