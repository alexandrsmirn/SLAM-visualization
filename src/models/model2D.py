import pickle
import mrob
import numpy as np

from src.items.landmark import Landmark, Landmark2D
from src.items.pose import Pose, Pose2D
from src.items.edge import Edge, Factor_pl_2D, Factor_pp_2D

from src.placement import CustomPlacementTool

from gaphas.tool import PlacementTool, ConnectHandleTool, HandleTool
from gaphas import Canvas, GtkView
from gaphas.painter import DefaultPainter
import gaphas.picklers

class Model2D:
    def __init__(self, builder, view):
        
        self.view = view
        self.builder = builder

        self.pose_landmark_matrix = np.empty((2, 2), dtype=np.float64)
        self.pose_pose_matrix = np.empty((3, 3), dtype=np.float64)

        self.are_cov_matrices_set = False
        self.has_anchor = False

        self.graph = mrob.fgraph.FGraph()


    def _add_landmark(self, canvas):
        def wrapper():
            landmark = Landmark2D()
            canvas.add(landmark)
            return landmark

        return wrapper

    def _add_factor_pp(self, canvas, observation, cov_matrix):
        def wrapper():
            factor = Factor_pp_2D(observation, cov_matrix)
            canvas.add(factor)
            return factor

        return wrapper

    def _add_factor_pl(self, canvas, observation, cov_matrix):
        def wrapper():
            factor = Factor_pl_2D(observation, cov_matrix)
            canvas.add(factor)
            return factor

        return wrapper

    def _add_pose(self, canvas, position):
        def wrapper():
            pose = Pose2D(position)
            canvas.add(pose)
            return pose

        return wrapper

    
    def save_state(self):
        if self.are_cov_matrices_set:
            pickle.dump(self.pose_landmark_matrix, open('saves/pl_matrix.pkl', 'wb+'))
            pickle.dump(self.pose_pose_matrix, open('saves/pp_matrix.pkl', 'wb+'))
            pickle.dump(self.view.canvas, open('saves/canvas.pkl', 'wb+'))
        else:
            print("Set cov matrices!!!")


    def add_landmark(self):
        self.view.tool.grab(PlacementTool(self.view, self._add_landmark(self.view.canvas), HandleTool(), 0))


    def add_pose(self):
        position = np.empty((3, 1), dtype=np.float64)

        for i in range(1, 4):
            entry = self.builder.get_object("NewPose2DEntry{}".format(i))
            text = entry.get_text()
            print(text)

            try:
                value = float(text)
            except:
                print("Error in entry {}".format(i))
                entry.set_text("")
                return

            position[i-1] = value
        
        self.view.tool.grab(PlacementTool(self.view, self._add_pose(self.view.canvas, position), HandleTool(), 0))


    def add_factor_2DPP(self):
        observation = np.empty((3, 1), dtype=np.float64)    

        if (not self.are_cov_matrices_set):
            print("set cov matrices!!!")
            return

        for i in range(1, 4):
            entry = self.builder.get_object("NewFactor2DPPEntry{}".format(i))
            try:
                value = float(entry.get_text())
            except:
                print("Error in entry {}".format(i))
                entry.set_text("")
                return
            observation[i-1] = value

        self.view.tool.grab(CustomPlacementTool(self.view, self._add_factor_pp(self.view.canvas, observation, self.pose_pose_matrix), ConnectHandleTool(), 1))

    
    def apply_cov_matrices(self):
        for i in range(1, 3):
            for j in range(1, 3):
                entry = self.builder.get_object("PL2DMatrixEntry{}{}".format(i, j))
                try:
                    value = float(entry.get_text())
                except:
                    print("Error in PL matrix entry {}, {}".format(i, j))
                    entry.set_text("")
                    return
                self.pose_landmark_matrix[i-1, j-1] = value

        for i in range(1, 4):
            for j in range(1, 4):
                entry = self.builder.get_object("PP2DMatrixEntry{}{}".format(i, j))
                try:
                    value = float(entry.get_text())
                except:
                    print("Error in PP matrix entry {}, {}".format(i, j))
                    entry.set_text("")
                    return
                self.pose_pose_matrix[i-1, j-1] = value

        self.are_cov_matrices_set = True


    def add_factor_2DPL(self):
        observation = np.empty((2, 1), dtype=np.float64)    

        if (not self.are_cov_matrices_set):
            print("set cov matrices!!!")
            return

        for i in range(1, 3):
            entry = self.builder.get_object("NewFactor2DPLEntry{}".format(i))
            try:
                value = float(entry.get_text())
            except:
                print("Error in entry {}".format(i))
                entry.set_text("")
                return
            observation[i-1] = value

        self.view.tool.grab(CustomPlacementTool(self.view, self._add_factor_pl(self.view.canvas, observation, self.pose_landmark_matrix), ConnectHandleTool(), 1))


    def plot_graph(self):
        items = self.view.canvas.get_all_items()
    
        for item in items:
            if isinstance(item, Landmark):
                item.id = self.graph.add_node_landmark_2d(np.array([0,0]))
            elif isinstance(item, Pose):
                item.id = self.graph.add_node_pose_2d(item.position)
                if not self.has_anchor:#TODO
                    self.graph.add_factor_1pose_2d(np.zeros(3), item.id, self.pose_pose_matrix)
                    self.has_anchor = True

        for item in items:
            if isinstance(item, Factor_pl_2D):
                h1, h2 = item.handles()
                first_connected = self.view.canvas.get_connection(h1).connected
                second_connected = self.view.canvas.get_connection(h2).connected

                if isinstance(second_connected, Landmark) and isinstance(first_connected, Pose):
                    self.graph.add_factor_1pose_1landmark_2d(item.observation, first_connected.id, second_connected.id, self.pose_landmark_matrix)

                elif isinstance(second_connected, Pose) and isinstance(first_connected, Landmark):
                    self.graph.add_factor_1pose_1landmark_2d(item.observation, second_connected.id, first_connected.id, self.pose_landmark_matrix)

                else:
                    print("Error")

            elif isinstance(item, Factor_pp_2D):
                h1, h2 = item.handles()
                first_connected = self.view.canvas.get_connection(h1).connected
                second_connected = self.view.canvas.get_connection(h2).connected

                if (isinstance(first_connected, Pose) and isinstance(second_connected, Pose)):
                    self.graph.add_factor_2poses_2d(item.observation, first_connected.id, second_connected.id, self.pose_pose_matrix)
                
                else:
                    print("Error")

        self.graph.print()
        self.graph.solve(mrob.fgraph.LM)
        self.graph.print(True)


    def delete_focused(self):
        if self.view.focused_item:
            self.view.canvas.remove(self.view.focused_item)


    def load_canvas(self):
        print("Loading")
        self.view.canvas = pickle.load(open('saves/canvas.pkl', 'rb'))
        self.pose_landmark_matrix = pickle.load(open('saves/pl_matrix.pkl', 'rb'))
        self.pose_pose_matrix = pickle.load(open('saves/pp_matrix.pkl', 'rb'))
        self.are_cov_matrices_set = True