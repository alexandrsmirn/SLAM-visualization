import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

win = Gtk.Window()                      #create an empty window
win.connect("destroy", Gtk.main_quit)   #connect callback to the event
win.show_all()                          #display the window
Gtk.main()                              #start GTK processing loop for events