import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from gaphas import Canvas, GtkView
from gaphas.examples import Box
from gaphas.painter import DefaultPainter
from gaphas.item import Line
from gaphas.segment import Segment
from gaphas.tool import HandleTool, PlacementTool

import numpy as np

from landmark import Landmark, Landmark2D
from edge import Edge
from pose import Pose2D

from gaphas.painter import (
    BoundingBoxPainter,
    FocusedItemPainter,
    HandlePainter,
    ItemPainter,
    PainterChain,
    ToolPainter,
)

from gaphas.freehand import FreeHandPainter


from random import randint

def add_landmark(canvas):
    #builder.get_object("MainWindow").set_cursor(Gtk.Cursor.new(Gtk.CursorType.CROSSHAIR))
    def wrapper():
        landmark = Landmark2D()
        canvas.add(landmark)
        return landmark

    return wrapper

def add_edge(canvas):
    edge = Edge()
    edge.matrix.translate(randint(50, 350), randint(50, 350))
    canvas.add(edge)
    edge.handles()[1].pos = (40, 40)

def add_pose(canvas, position):
    def wrapper():
        pose = Pose2D(position)
        canvas.add(pose)
        return pose

    return wrapper

def handle_changed(view, item, what):
    stack = builder.get_object("PropertiesStack")
    if (type(item) is Landmark):
        stack.set_visible_child_name("LandmarkFrame")
    else:
        stack.set_visible_child_name("EmptyFrame")

class Handler:
    def __init__(self, view):
        self.view = view    
        self.canvas = view.canvas

    def on_MainWindow_destroy(self, *args):
        Gtk.main_quit()

    def on_newLandmarkBtn_clicked(self, button):
        self.view.tool.grab(PlacementTool(self.view, add_landmark(self.canvas), HandleTool(), 0))

    def on_btn2_clicked(self, button):
        add_edge(self.canvas)

    def on_btn3_clicked(self, button):
        item = self.view.focused_item
        if type(item) is Edge:
            h1, h2 = item.handles()
            #print(type(self.canvas.get_connection(h1)))
            print(self.canvas.get_connection(h1))
            print(self.canvas.get_connection(h2))
        
    def on_newPoseBtn_clicked(self, button):
        stack = builder.get_object("PropertiesStack")
        stack.set_visible_child_name("NewPose2DFrame")



    def on_AddPoseButton_clicked(self, button):
        position = np.empty((3, 1), dtype=np.float64)

        for i in range(1, 4):
            entry = builder.get_object("NewPose2DEntry{}".format(i))
            text = entry.get_text()
            print(text)

            try:
                value = np.fromstring(text, dtype=np.float64, sep=' ', count=1)[0]
            except:
                print("Error in entry {}".format(i))
                return

            position[i-1] = value
        
        self.view.tool.grab(PlacementTool(self.view, add_pose(self.canvas, position), HandleTool(), 0))



    def focus_changed(self, view, item, what):
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

    #view.painter = (
    #    PainterChain()
    #    .append(FreeHandPainter(ItemPainter(view)))
    #    .append(HandlePainter(view))
    #    .append(FocusedItemPainter(view))
    #    .append(ToolPainter(view))
    #)
    #view.bounding_box_painter = BoundingBoxPainter(
    #    FreeHandPainter(ItemPainter(view))
    #)

    view.canvas = Canvas()

    handler = Handler(view)
    builder.connect_signals(handler)
    view.connect("focus-changed", handler.focus_changed, "focus")

    gaphas_window = builder.get_object("GaphasWindow")
    gaphas_window.add(view)

    window = builder.get_object("MainWindow")
    window.show_all()
    Gtk.main()

if __name__ == "__main__":
    Main()