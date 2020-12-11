import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from models.model2D import Model2D
from viewer import MainView

class Controller:
    def __init__(self, builder, main_view, graph_view):
        self.builder = builder
        self.model = Model2D(builder, graph_view)
        self.main_view = main_view

    def on_MainWindow_destroy(self, *args):
        Gtk.main_quit()


    def on_SaveCanvasBtn_clicked(self, button):
        self.model.save_state()


    def on_NewLandmarkBtn_clicked(self, button):
        self.model.add_landmark()
        
    
    def on_NewPoseBtn_clicked(self, button):
        stack = self.builder.get_object("PropertiesStack")
        self.main_view.open_new_pose_editor(stack)
        

    def on_AddPoseButton_clicked(self, button):
        self.model.add_pose()

        
    def on_NewFactorPPBtn_clicked(self, button):
        stack = self.builder.get_object("PropertiesStack")
        self.main_view.open_new_factorPP_editor(stack)   
  
    
    def on_AddFactor2DPPBtn_clicked(self, button):
        self.model.add_factor_2DPP()


    def on_SetCovMatricesBtn_clicked(self, button):
        stack = self.builder.get_object("PropertiesStack")
        self.main_view.open_cov_matrices_set_editor(stack)

        
    def on_ApplyCovMatrices2DBtn_clicked(self, button):
        self.model.apply_cov_matrices()

    
    def on_NewFactorPLBtn_clicked(self, button):
        stack = self.builder.get_object("PropertiesStack")
        self.main_view.open_new_factorPL_editor(stack)


    def on_AddFactor2DPLBtn_clicked(self, button):
        self.model.add_factor_2DPL()


    def on_PlotGraphBtn_clicked(self, button):        
        self.model.plot_graph()


    def on_DeleteFocusedBtn_clicked(self, button):
        self.model.delete_focused()


    def on_LoadCanvasBtn_clicked(self, button):
        self.model.load_canvas()

        
    def focus_changed(self, view, item, what):
        pass