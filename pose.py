from gaphas.connector import Handle
from gaphas.item import Item
from gaphas.connector import PointPort


from gi.repository import Gtk
import cairo

class Pose(Item):
    side = 45

    def __init__(self):
        super().__init__()
        self._handles = [Handle()]
        h1 = self._handles[0]
        h1.movable = False
        h1.visible = False
        self._ports.append(PointPort(h1.pos))

    def point(self, pos):
        h1 = self._handles[0]
        p1 = h1.pos
        x, y = pos
        dist = ((x - p1.x) ** 2 + (y - p1.y) ** 2) ** 0.5
        return dist - self.side/2

    def draw(self, context):
        from math import sqrt
        cr = context.cairo
        
        cr.move_to(0, -self.side/2)
        cr.line_to(self.side/2, self.side/4)
        cr.line_to(-self.side/2, self.side/4)
        cr.line_to(0, -self.side/2)

        if context.hovered:
            cr.set_source_rgba(0.8, 0.8, 1, 0.8)
        else:
            cr.set_source_rgba(1, 1, 1, 0.8)
        cr.fill_preserve()
        #cr.set_source_rgb(0, 0, 0.8)
        cr.stroke()

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from gaphas import Canvas, GtkView
from gaphas.examples import Box
from gaphas.painter import DefaultPainter
from gaphas.item import Line
from gaphas.segment import Segment


def Main():

    def create_canvas(canvas, title):
        # Setup drawing window
        window = Gtk.Window()
        window.set_title(title)
        window.set_default_size(400, 400)

        view = GtkView() #Gtk widget
        view.painter = DefaultPainter()
        view.canvas = canvas

        win_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL) #added Gtk box to Gtk window
        window.add(win_box)
        win_box.pack_start(view, True, True, 0) #added "view" widget to the box

        pose = Pose()
        pose.matrix.translate(100, 100)
        canvas.add(pose)

        window.show_all()
        window.connect("destroy", Gtk.main_quit)


    c = Canvas()
    create_canvas(c, "it's gonna be SLAM graph")
    Gtk.main()

if __name__ == "__main__":
    Main()