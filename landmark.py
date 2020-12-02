from gaphas.connector import Handle
from gaphas.item import Item
from gaphas.util import path_ellipse
from gaphas.connector import PointPort

class Landmark(Item):
    def __init__(self):
        super().__init__()
        self._handles = [Handle(movable=False)]
        h = self._handles[0]
        h.visible = False
        self._ports = [PointPort(h.pos)]

        self.id: int
        self.radius = 20
        self.colour_hovered = (0.8, 0.8, 1, 0.8)
        self.colour = (1, 1, 1, 0.8)

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
            cr.set_source_rgba(*self.colour_hovered)
        else:
            cr.set_source_rgba(*self.colour)
        cr.fill_preserve()
        #cr.set_source_rgb(0, 0, 0.8)
        cr.stroke()
        #TODO: transparency

class Landmark2D(Landmark):
    pass

class Landmark3D(Landmark):
    pass
    

