from gaphas.tool import PlacementTool

class CustomPlacementTool(PlacementTool):
    def on_button_press(self, event):
        view = self.view
        canvas = view.canvas
        pos = event.get_coords()[1:]
        new_item = self._create_item(pos)
        # Enforce matrix update, as a good matrix is required for the handle
        # positioning:
        canvas.get_matrix_i2c(new_item, calculate=True)

        self._new_item = new_item
        view.focused_item = new_item

        self.handle_tool.connect(new_item, new_item.handles()[0], pos)

        h = new_item.handles()[self._handle_index]
        if h.movable:
            self.handle_tool.grab_handle(new_item, h)
            self.grabbed_handle = h
        return True