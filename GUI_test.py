import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from gaphas import Canvas, GtkView
from gaphas.examples import Box
from gaphas.painter import DefaultPainter
from gaphas.item import Line
from gaphas.segment import Segment

from random import randint

def add_box(canvas):
    b2 = Box(60, 60)
    b2.min_width = 40
    b2.min_height = 50
    b2.matrix.translate(randint(50, 350), randint(50, 350))
    canvas.add(b2)

def add_line(canvas):
    line = Line()
    line.matrix.translate(randint(50, 350), randint(50, 350))
    canvas.add(line)
    line.handles()[1].pos = (30, 30)


class Handler:
    def __init__(self, canvas):
        self.canvas = canvas

    def on_MainWindow_destroy(self, *args):
        Gtk.main_quit()

    def on_btn1_clicked(self, button):
        add_box(self.canvas)

    def on_btn2_clicked(self, button):
        add_line(self.canvas)

def Main():
    builder = Gtk.Builder()
    builder.add_from_file("GUI_test.glade")

    view = GtkView() #Gtk widget
    view.painter = DefaultPainter()
    view.canvas = Canvas()

    builder.connect_signals(Handler(view.canvas))

    gaphas_window = builder.get_object("GaphasWindow")
    gaphas_window.add(view)

    window = builder.get_object("MainWindow")
    window.show_all()
    Gtk.main()

if __name__ == "__main__":
    Main()