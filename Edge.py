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

class Edge(Item):
    """
    A Line item.

    Properties:
     - fuzziness (0.0..n): an extra margin that should be taken into
         account when calculating the distance from the line (using
         point()).
     - orthogonal (bool): whether or not the line should be
         orthogonal (only straight angles)
     - horizontal: first line segment is horizontal
     - line_width: width of the line to be drawn

    This line also supports arrow heads on both the begin and end of
    the line. These are drawn with the methods draw_head(context) and
    draw_tail(context). The coordinate system is altered so the
    methods do not have to know about the angle of the line segment
    (e.g. drawing a line from (10, 10) via (0, 0) to (10, -10) will
    draw an arrow point).
    """

    def __init__(self):
        super().__init__()
        self._handles = [Handle(connectable=True), Handle((10, 10), connectable=True)]
        self._ports = []
        #self._update_ports()

        self._line_width = 2
        self._fuzziness = 0
        self._orthogonal_constraints = []
        self._horizontal = False
        self._head_angle = self._tail_angle = 0

    @observed
    def _set_line_width(self, line_width):
        self._line_width = line_width

    line_width = reversible_property(lambda s: s._line_width, _set_line_width)

    @observed
    def _set_fuzziness(self, fuzziness):
        self._fuzziness = fuzziness

    fuzziness = reversible_property(lambda s: s._fuzziness, _set_fuzziness)

    def _update_orthogonal_constraints(self, orthogonal):
        """
        Update the constraints required to maintain the orthogonal line.
        The actual constraints attribute (``_orthogonal_constraints``) is
        observed, so the undo system will update the contents properly
        """
        if not self.canvas:
            self._orthogonal_constraints = orthogonal and [None] or []
            return

        for c in self._orthogonal_constraints:
            self.canvas.solver.remove_constraint(c)
        del self._orthogonal_constraints[:]

        if not orthogonal:
            return

        h = self._handles
        # if len(h) < 3:
        #    self.split_segment(0)
        eq = EqualsConstraint  # lambda a, b: a - b
        add = self.canvas.solver.add_constraint
        cons = []
        rest = self._horizontal and 1 or 0
        for pos, (h0, h1) in enumerate(zip(h, h[1:])):
            p0 = h0.pos
            p1 = h1.pos
            if pos % 2 == rest:  # odd
                cons.append(add(eq(a=p0.x, b=p1.x)))
            else:
                cons.append(add(eq(a=p0.y, b=p1.y)))
            self.canvas.solver.request_resolve(p1.x)
            self.canvas.solver.request_resolve(p1.y)
        self._set_orthogonal_constraints(cons)
        self.request_update()

    @observed
    def _set_orthogonal_constraints(self, orthogonal_constraints):
        """
        Setter for the constraints maintained. Required for the undo
        system.
        """
        self._orthogonal_constraints = orthogonal_constraints

    reversible_property(
        lambda s: s._orthogonal_constraints, _set_orthogonal_constraints
    )

    @observed
    def _set_orthogonal(self, orthogonal):
        """
        >>> a = Line()
        >>> a.orthogonal
        False
        """
        if orthogonal and len(self.handles()) < 3:
            raise ValueError("Can't set orthogonal line with less than 3 handles")
        self._update_orthogonal_constraints(orthogonal)

    orthogonal = reversible_property(
        lambda s: bool(s._orthogonal_constraints), _set_orthogonal
    )

    @observed
    def _inner_set_horizontal(self, horizontal):
        self._horizontal = horizontal

    reversible_method(
        _inner_set_horizontal,
        _inner_set_horizontal,
        {"horizontal": lambda horizontal: not horizontal},
    )

    def _set_horizontal(self, horizontal):
        """
        >>> line = Line()
        >>> line.horizontal
        False
        >>> line.horizontal = False
        >>> line.horizontal
        False
        """
        self._inner_set_horizontal(horizontal)
        self._update_orthogonal_constraints(self.orthogonal)

    horizontal = reversible_property(lambda s: s._horizontal, _set_horizontal)

    def setup_canvas(self):
        """
        Setup constraints. In this case orthogonal.
        """
        super().setup_canvas()
        self._update_orthogonal_constraints(self.orthogonal)

    def teardown_canvas(self):
        """
        Remove constraints created in setup_canvas().
        """
        super().teardown_canvas()
        for c in self._orthogonal_constraints:
            self.canvas.solver.remove_constraint(c)

    @observed
    def _reversible_insert_handle(self, index, handle):
        self._handles.insert(index, handle)

    @observed
    def _reversible_remove_handle(self, handle):
        self._handles.remove(handle)

    reversible_pair(
        _reversible_insert_handle,
        _reversible_remove_handle,
        bind1={"index": lambda self, handle: self._handles.index(handle)},
    )

    @observed
    def _reversible_insert_port(self, index, port):
        self._ports.insert(index, port)

    @observed
    def _reversible_remove_port(self, port):
        self._ports.remove(port)

    reversible_pair(
        _reversible_insert_port,
        _reversible_remove_port,
        bind1={"index": lambda self, port: self._ports.index(port)},
    )

    def _create_handle(self, pos, strength=WEAK):
        return Handle(pos, strength=strength)

    def _create_port(self, p1, p2):
        return LinePort(p1, p2)

    def _update_ports(self):
        """
        Update line ports. This destroys all previously created ports
        and should only be used when initializing the line.
        """
        assert len(self._handles) >= 2, "Not enough segments"
        self._ports = []
        handles = self._handles
        for h1, h2 in zip(handles[:-1], handles[1:]):
            self._ports.append(self._create_port(h1.pos, h2.pos))

    def opposite(self, handle):
        """
        Given the handle of one end of the line, return the other end.
        """
        handles = self._handles
        if handle is handles[0]:
            return handles[-1]
        elif handle is handles[-1]:
            return handles[0]
        else:
            raise KeyError("Handle is not an end handle")

    def post_update(self, context):
        """
        """
        super().post_update(context)
        h0, h1 = self._handles[:2]
        p0, p1 = h0.pos, h1.pos
        self._head_angle = atan2(p1.y - p0.y, p1.x - p0.x)
        h1, h0 = self._handles[-2:]
        p1, p0 = h1.pos, h0.pos
        self._tail_angle = atan2(p1.y - p0.y, p1.x - p0.x)

    def point(self, pos):
        """
        >>> a = Line()
        >>> a.handles()[1].pos = 25, 5
        >>> a._handles.append(a._create_handle((30, 30)))
        >>> a.point((-1, 0))
        1.0
        >>> f"{a.point((5, 4)):.3f}
        '2.942'
        >>> f"{a.point((29, 29)):.3f}
        '0.784'
        """
        hpos = [h.pos for h in self._handles]

        distance, _point = min(
            map(distance_line_point, hpos[:-1], hpos[1:], [pos] * (len(hpos) - 1))
        )
        return max(0, distance - self.fuzziness)

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
        cr.set_line_width(self.line_width)
        draw_line_end(self._handles[0].pos, self._head_angle, self.draw_head)
        for h in self._handles[1:-1]:
            cr.line_to(*h.pos)
        draw_line_end(self._handles[-1].pos, self._tail_angle, self.draw_tail)
        cr.stroke()