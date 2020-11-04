import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk



class Handler:
    def __init__(self):
        self.btn_state = False

    def on_MainWindow_destroy(self, *args):
        Gtk.main_quit()

    def on_button1_clicked(self, button):
        Label = builder.get_object("Label")
        if self.btn_state:
            Label.set_text("monke")
        else:
            Label.set_text("double monke")
        self.btn_state = not self.btn_state


#GTK.builder class offers you the opportunity to design user interfaces
#without writing a single line of code

builder = Gtk.Builder()

#loads all objects defined in example.glade into the Builder object.          
builder.add_from_file("Hello_world.glade")
builder.connect_signals(Handler())

#Every widget can be retrieved from the builder
# by the Gtk.Builder.get_object() method and the widget’s id
window = builder.get_object("MainWindow")
builder.get_object("Label").set_text("monke")
window.show_all()

#builder.get_objects() to get a list of all objects

Gtk.main()