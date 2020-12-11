from gaphas.connector import Handle
from gaphas.item import Item
from gaphas.connector import PointPort

import numpy as np
import mrob


from gi.repository import Gtk
import cairo

class Pose(Item):
    side = 45

    def __init__(self):
        super().__init__()
        self._handles = [Handle(movable=False)]
        h = self._handles[0]
        h.visible = False
        self._ports.append(PointPort(h.pos))
        
        self.id: int
        self.colour_hovered = (0.8, 0.8, 1, 0.8)
        self.colour = (1, 0, 1, 0.8)

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
            cr.set_source_rgba(*self.colour_hovered)
        else:
            cr.set_source_rgba(*self.colour)
        cr.fill_preserve()
        #cr.set_source_rgb(0, 0, 0.8)
        cr.stroke()

class Pose2D(Pose):
    def __init__(self, position: np.array((3,1), dtype=np.float64)):
        super().__init__()
        self.position = position


class Anchor2D(Pose2D):
    def __init__(self, position):
        super().__init__(position)
        #todo one more parameter
        self.covariance_matrix = np.empty((3, 3), dtype=np.float64)
        self.colour = (1, 0, 0, 0.8)

class Pose3D(Pose):
    def __init__(self):
        super().__init__()
        self.position: np.empty((6, 6), dtype=np.float64)

class Anchor3D(Pose3D):
    def __init__(self):
        super().__init__()
        #todo one more parameter
        self.covariance_matrix = np.empty((6, 6), dtype=np.float64)
        self.colour = (1, 0, 0, 0.8)
    