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