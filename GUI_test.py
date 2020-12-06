import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

from gaphas import Canvas, GtkView
from gaphas.examples import Box
from gaphas.painter import DefaultPainter
from gaphas.item import Line
from gaphas.segment import Segment
from gaphas.tool import HandleTool, PlacementTool

import numpy as np

from landmark import Landmark, Landmark2D
from edge import Edge, Factor_pl_2D, Factor_pp_2D
from pose import Pose, Pose2D

from random import randint
import mrob
import pickle


def add_landmark(canvas):
    #builder.get_object("GaphasWindow").set_cursor(Gdk.Cursor.new(Gdk.CursorType.CROSSHAIR))
    def wrapper():
        landmark = Landmark2D()
        canvas.add(landmark)
        return landmark

    return wrapper

def add_factor_pp(canvas, observation, cov_matrix):
    def wrapper():
        factor = Factor_pp_2D(observation, cov_matrix)
        canvas.add(factor)
        return factor
    
    return wrapper

def add_factor_pl(canvas, observation, cov_matrix):
    def wrapper():
        factor = Factor_pl_2D(observation, cov_matrix)
        canvas.add(factor)
        return factor

    return wrapper

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
        self.pose_landmark_matrix = np.empty((2, 2), dtype=np.float64)
        self.pose_pose_matrix = np.empty((3, 3), dtype=np.float64)
        self.are_cov_matrices_set = False
        self.has_anchor = False


    def on_MainWindow_destroy(self, *args):
        #pickle.dump(self.canvas.get_all_items()[0], open('canvas.pkl', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
        Gtk.main_quit()

    def on_NewLandmarkBtn_clicked(self, button):
        self.view.tool.grab(PlacementTool(self.view, add_landmark(self.canvas), HandleTool(), 0))
    

    def on_NewPoseBtn_clicked(self, button):
        stack = builder.get_object("PropertiesStack")
        stack.set_visible_child_name("NewPose2DFrame")



    def on_AddPoseButton_clicked(self, button):
        position = np.empty((3, 1), dtype=np.float64)

        for i in range(1, 4):
            entry = builder.get_object("NewPose2DEntry{}".format(i))
            text = entry.get_text()
            print(text)

            try:
                value = float(text)
            except:
                print("Error in entry {}".format(i))
                entry.set_text("")
                return

            position[i-1] = value
        
        self.view.tool.grab(PlacementTool(self.view, add_pose(self.canvas, position), HandleTool(), 0))

        

    
    def on_NewFactorPPBtn_clicked(self, button):
        stack = builder.get_object("PropertiesStack")
        stack.set_visible_child_name("NewFactor2DPPFrame")


    
    def on_AddFactor2DPPBtn_clicked(self, button):
        observation = np.empty((3, 1), dtype=np.float64)    

        if (not self.are_cov_matrices_set):
            print("set cov matrices!!!")
            return

        for i in range(1, 4):
            entry = builder.get_object("NewFactor2DPPEntry{}".format(i))
            try:
                value = float(entry.get_text())
            except:
                print("Error in entry {}".format(i))
                entry.set_text("")
                return
            observation[i-1] = value

        self.view.tool.grab(PlacementTool(self.view, add_factor_pp(self.canvas, observation, self.pose_pose_matrix), HandleTool(), 1))#???? 1 or 0



    def on_SetCovMatricesBtn_clicked(self, button):
        stack = builder.get_object("PropertiesStack")
        stack.set_visible_child_name("SetCovMatrices2DFrame")



    def on_ApplyCovMatrices2DBtn_clicked(self, button):
        for i in range(1, 3):
            for j in range(1, 3):
                entry = builder.get_object("PL2DMatrixEntry{}{}".format(i, j))
                try:
                    value = float(entry.get_text())
                except:
                    print("Error in PL matrix entry {}, {}".format(i, j))
                    entry.set_text("")
                    return
                self.pose_landmark_matrix[i-1, j-1] = value

        for i in range(1, 4):
            for j in range(1, 4):
                entry = builder.get_object("PP2DMatrixEntry{}{}".format(i, j))
                try:
                    value = float(entry.get_text())
                except:
                    print("Error in PP matrix entry {}, {}".format(i, j))
                    entry.set_text("")
                    return
                self.pose_pose_matrix[i-1, j-1] = value

        self.are_cov_matrices_set = True


    
    def on_NewFactorPLBtn_clicked(self, button):
        stack = builder.get_object("PropertiesStack")
        stack.set_visible_child_name("NewFactor2DPLFrame")



    def on_AddFactor2DPLBtn_clicked(self, button):
        observation = np.empty((2, 1), dtype=np.float64)    

        if (not self.are_cov_matrices_set):
            print("set cov matrices!!!")
            return

        for i in range(1, 3):
            entry = builder.get_object("NewFactor2DPLEntry{}".format(i))
            try:
                value = float(entry.get_text())
            except:
                print("Error in entry {}".format(i))
                entry.set_text("")
                return
            observation[i-1] = value

        self.view.tool.grab(PlacementTool(self.view, add_factor_pl(self.canvas, observation, self.pose_landmark_matrix), HandleTool(), 1))


    def on_PlotGraphBtn_clicked(self, button):
        items = self.canvas.get_all_items()
    
        for item in items:
            if isinstance(item, Landmark):
                item.id = graph.add_node_landmark_2d(np.array([0,0]))
            elif isinstance(item, Pose):
                item.id = graph.add_node_pose_2d(item.position)
                if not self.has_anchor:#TODO
                    graph.add_factor_1pose_2d(np.zeros(3), item.id, self.pose_pose_matrix)
                    self.has_anchor = True

        for item in items:
            if isinstance(item, Factor_pl_2D):
                h1, h2 = item.handles()
                first_connected = self.canvas.get_connection(h1).connected
                second_connected = self.canvas.get_connection(h2).connected

                if isinstance(second_connected, Landmark) and isinstance(first_connected, Pose):
                    graph.add_factor_1pose_1landmark_2d(item.observation, first_connected.id, second_connected.id, self.pose_landmark_matrix)

                elif isinstance(second_connected.Pose) and isinstance(first_connected, Landmark):
                    graph.add_factor_1pose_1landmark_2d(item.observation, second_connected.id, first_connected.id, self.pose_landmark_matrix)

                else:
                    print("Error")

            elif isinstance(item, Factor_pp_2D):
                h1, h2 = item.handles()
                first_connected = self.canvas.get_connection(h1).connected
                second_connected = self.canvas.get_connection(h2).connected

                if (isinstance(first_connected, Pose) and isinstance(second_connected, Pose)):
                    graph.add_factor_2poses_2d(item.observation, first_connected.id, second_connected.id, self.pose_pose_matrix)
                
                else:
                    print("Error")

        graph.print()
        graph.solve(mrob.fgraph.LM)
        graph.print(True)


    def on_DeleteFocusedBtn_clicked(self, button):
        if self.view.focused_item:
            self.canvas.remove(self.view.focused_item)

    #def on_LoadCanvas_clicked(self, button):
        #self.canvas = pickle.load(open('canvas.pkl', 'rb'))

        
    def focus_changed(self, view, item, what):
        view.focused_item = item
        stack = builder.get_object("PropertiesStack")
        if (type(item) is Landmark):
            stack.set_visible_child_name("LandmarkFrame")
        else:
            stack.set_visible_child_name("EmptyFrame")

def Main():
    global builder
    global graph

    graph = mrob.fgraph.FGraph()

    builder = Gtk.Builder()
    builder.add_from_file("GUI_test.glade")

    view = GtkView() #Gtk widget
    view.painter = DefaultPainter()

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