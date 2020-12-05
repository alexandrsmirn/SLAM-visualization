from functools import reduce
from math import atan2
from weakref import WeakKeyDictionary, WeakSet

from gaphas.connector import Handle, LinePort
from gaphas.constraint import (
    EqualsConstraint,
    LessThanConstraint,
    LineAlignConstraint,
    LineConstraint,
)
from gaphas.geometry import distance_line_point, distance_rectangle_point
from gaphas.matrix import Matrix
from gaphas.solver import REQUIRED, VERY_STRONG, WEAK, solvable
from gaphas.state import (
    observed,
    reversible_method,
    reversible_pair,
    reversible_property,
)

from gaphas.item import Item

import mrob
import numpy as np

class Edge(Item):

    def __init__(self):
        super().__init__()
        self._handles = (Handle(connectable=True), Handle((10, 10), connectable=True))
        self._line_width = 2

    @observed
    def _set_line_width(self, line_width):
        self._line_width = line_width

    def opposite(self, handle):
        handles = self._handles
        if handle is handles[0]:
            return handles[-1]
        elif handle is handles[-1]:
            return handles[0]
        else:
            raise KeyError("Handle is not an end handle")

    def post_update(self, context):
        super().post_update(context)
        h0, h1 = self._handles[:2]
        p0, p1 = h0.pos, h1.pos
        self._head_angle = atan2(p1.y - p0.y, p1.x - p0.x)
        h1, h0 = self._handles[-2:]
        p1, p0 = h1.pos, h0.pos
        self._tail_angle = atan2(p1.y - p0.y, p1.x - p0.x)

    def point(self, pos):
        hpos = [h.pos for h in self._handles]

        distance, _point = min(
            map(distance_line_point, hpos[:-1], hpos[1:], [pos] * (len(hpos) - 1))
        )
        return max(0, distance)

    def draw_head(self, context):
        """
        Default head drawer: move cursor to the first handle.
        """
        context.cairo.move_to(0, 0)

    def draw_tail(self, context):
        """
        Default tail drawer: draw line to the last handle.
        """
        context.cairo.line_to(0, 0)

    def draw(self, context):
        """
        Draw the line itself.
        See Item.draw(context).
        """

        def draw_line_end(pos, angle, draw):
            cr = context.cairo
            cr.save()
            try:
                cr.translate(*pos)
                cr.rotate(angle)
                draw(context)
            finally:
                cr.restore()

        cr = context.cairo
        cr.set_line_width(self._line_width)
        draw_line_end(self._handles[0].pos, self._head_angle, self.draw_head)
        for h in self._handles[1:-1]:
            cr.line_to(*h.pos)
        draw_line_end(self._handles[-1].pos, self._tail_angle, self.draw_tail)
        cr.stroke()


class Factor_pp_2D(Edge):
    def __init__(self, observation: np.array((3, 1), dtype=np.float64), cov_matrix: np.array((3, 3), dtype=np.float64)):
        super().__init__()
        self.observation = observation
        self.covariance_matrix = cov_matrix

    def draw_tail(self, context):
        """
        Default tail drawer: draw line to the last handle.
        """
        cr = context.cairo
        cr.line_to(0, 0)
        cr.stroke()
        cr.move_to(15, -6)
        cr.line_to(0, 0)
        cr.line_to(15, 6)

class Factor_pl_2D(Edge):
    def __init__(self, observation: np.array((2, 1), dtype=np.float64), cov_matrix: np.array((2, 2), dtype=np.float64)):
        super().__init__()
        self.observation = observation
        self.covariance_matrix = cov_matrix

class Factor_pp_3D(Edge):
     def __init__(self):
        super().__init__()
        self.observation = np.empty((6, 6), dtype=np.float64)
        self.covariance_matrix = np.empty((3, 3), dtype=np.float64)

class Factor_pl_3D(Edge):
     def __init__(self):
        super().__init__()
        self.observation = np.empty((3, 1), dtype=np.float64)
        self.covariance_matrix = np.empty((3, 3), dtype=np.float64)


