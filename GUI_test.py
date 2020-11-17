import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from gaphas import Canvas, GtkView
from gaphas.examples import Box
from gaphas.painter import DefaultPainter
from gaphas.item import Line
from gaphas.segment import Segment
from landmark import Landmark
from edge import Edge


from random import randint

def add_landmark(canvas):
    landmark = Landmark()
    landmark.matrix.translate(randint(50, 350), randint(50, 350))
    canvas.add(landmark)

def add_edge(canvas):
    edge = Edge()
    edge.matrix.translate(randint(50, 350), randint(50, 350))
    canvas.add(edge)
    edge.handles()[1].pos = (40, 40)

def handle_changed(view, item, what):
    stack = builder.get_object("PropertiesStack")
    if (type(item) is Landmark):
        stack.set_visible_child_name("LandmarkFrame")
    else:
        stack.set_visible_child_name("EmptyFrame")

class Handler:
    def __init__(self, view):
        self.canvas = view.canvas
        self.view = view

    def on_MainWindow_destroy(self, *args):
        Gtk.main_quit()

    def on_btn1_clicked(self, button):
        add_landmark(self.canvas)

    def on_btn2_clicked(self, button):
        add_edge(self.canvas)

    def on_btn3_clicked(self, button):
        item = self.view.focused_item
        if type(item) is Edge:
            h1, h2 = item.handles()
            print(self.canvas.get_connection(h1))
            print(self.canvas.get_connection(h2))

    def handle_changed(self, view, item, what):
        view.focused_item = item
        stack = builder.get_object("PropertiesStack")
        if (type(item) is Landmark):
            stack.set_visible_child_name("LandmarkFrame")
        else:
            stack.set_visible_child_name("EmptyFrame")

def Main():
    global builder
    builder = Gtk.Builder()
    builder.add_from_file("GUI_test.glade")

    view = GtkView() #Gtk widget
    view.painter = DefaultPainter()
    view.canvas = Canvas()

    handler = Handler(view)
    builder.connect_signals(handler)
    view.connect("focus-changed", handler.handle_changed, "focus")

    gaphas_window = builder.get_object("GaphasWindow")
    gaphas_window.add(view)

    window = builder.get_object("MainWindow")
    window.show_all()
    Gtk.main()

if __name__ == "__main__":
    Main()