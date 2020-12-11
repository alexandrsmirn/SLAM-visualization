import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class MainView:

    def show_main_window(self, window):
        main_window = window
        main_window.show_all()

    def open_new_pose_editor(self, stack):
        stack.set_visible_child_name("NewPose2DFrame")

    def open_new_factorPP_editor(self, stack):
        stack.set_visible_child_name("NewFactor2DPPFrame")

    def open_cov_matrices_set_editor(self, stack):
        stack.set_visible_child_name("SetCovMatrices2DFrame")

    def open_new_factorPL_editor(self, stack):
        stack.set_visible_child_name("NewFactor2DPLFrame")