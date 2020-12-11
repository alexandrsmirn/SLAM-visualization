import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

from controller import Controller
from viewer import MainView

from gaphas import Canvas, GtkView
from gaphas.painter import DefaultPainter

def main():
    builder = Gtk.Builder()
    builder.add_from_file("AppWindow.glade")

    graph_view = GtkView()
    graph_view.painter = DefaultPainter()
    graph_view.canvas = Canvas()

    gaphas_window = builder.get_object("GaphasWindow")
    gaphas_window.add(graph_view)

    main_view = MainView()
    controller = Controller(builder, main_view, graph_view)
    builder.connect_signals(controller)
    #view.connect("focus-changed", handler.focus_changed, "focus")

    window = builder.get_object("MainWindow")
    main_view.show_main_window(window)

    Gtk.main()

if __name__ == "__main__":
    main()
