from gaphas.connector import Handle
from gaphas.item import Item
from gaphas.util import path_ellipse
from gaphas.connector import PointPort

class Landmark(Item):
    def __init__(self):
        super().__init__()
        self._handles.append(Handle())
        h1 = self._handles[0]
        h1.movable = False
        h1.visible = False

        self.radius = 20
        self._ports.append(PointPort(h1.pos))

    def point(self, pos):
        h1 = self._handles[0]
        p1 = h1.pos
        x, y = pos
        dist = ((x - p1.x) ** 2 + (y - p1.y) ** 2) ** 0.5
        return dist - self.radius

    def draw(self, context):
        cr = context.cairo
        path_ellipse(cr, 0, 0, 2 * self.radius, 2 * self.radius)
        if context.hovered:
            cr.set_source_rgba(0.8, 0.8, 1, 0.8)
        else:
            cr.set_source_rgba(1, 1, 1, 0.8)
        cr.fill_preserve()
        #cr.set_source_rgb(0, 0, 0.8)
        cr.stroke()
        #TODO: transparency
