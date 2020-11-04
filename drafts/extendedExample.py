import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from gaphas import Canvas, GtkView
from gaphas.examples import Box
from gaphas.painter import DefaultPainter
from gaphas.item import Line
from gaphas.segment import Segment


class MyWindow(Gtk.Window):
    def __init__(self, canvas):
        Gtk.Window.__init__(self, title="Hello World")  

        #connect the  button widget
        #connect to its clicked signal
        #add is as child to the top-level window
        #self.button = Gtk.Button(label="Click Here")
        #self.button.connect("clicked", self.on_button_clicked)

        self.label = Gtk.Label()

        self.view = GtkView() #Gtk widget
        self.view.painter = DefaultPainter()

        self.view.canvas = canvas

        self.win_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.add(self.win_box)

        self.win_box.pack_start(self.label, True, True, 0)
        self.win_box.pack_start(self.view, True, True, 0)

        self.b2 = Box(60, 60)
        self.b2.min_width = 40
        self.b2.min_height = 50
        self.b2.matrix.translate(170, 170)
        canvas.add(self.b2)

        # Draw gaphas line
        self.line = Line()
        self.line.matrix.translate(100, 60)
        canvas.add(self.line)
        self.line.handles()[1].pos = (30, 30)
        self.segment = Segment(self.line, canvas)
        self.segment.split_segment(0)

    def on_button_clicked(self, button):
        button.set_label("monke")
        print("Hello World")


c = Canvas()
win = MyWindow(c)
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()