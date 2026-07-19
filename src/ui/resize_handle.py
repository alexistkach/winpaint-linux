"""Resize Handle - Cuadradito negro"""
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk, GObject

class ResizeHandle(Gtk.DrawingArea):
    __gsignals__ = {
        "resize-request": (GObject.SIGNAL_RUN_FIRST, None, (int, int)),
    }

    HANDLE_SIZE = 8

    def __init__(self):
        super().__init__()
        self.set_size_request(self.HANDLE_SIZE, self.HANDLE_SIZE)
        self.set_draw_func(self._draw_handle, None)
        self.set_cursor_from_name("se-resize")
        self._setup_drag()
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.current_width = 0
        self.current_height = 0

    def _setup_drag(self):
        drag = Gtk.GestureDrag.new()
        drag.connect("drag-begin", self._on_drag_begin)
        drag.connect("drag-update", self._on_drag_update)
        drag.connect("drag-end", self._on_drag_end)
        self.add_controller(drag)

    def _draw_handle(self, area, ctx, width, height, data):
        ctx.set_source_rgb(0, 0, 0)
        ctx.rectangle(0, 0, width, height)
        ctx.fill()
        ctx.set_source_rgb(1, 1, 1)
        ctx.set_line_width(1)
        ctx.rectangle(0.5, 0.5, width - 1, height - 1)
        ctx.stroke()

    def _on_drag_begin(self, gesture, start_x, start_y):
        self.drag_start_x = start_x
        self.drag_start_y = start_y

    def _on_drag_update(self, gesture, offset_x, offset_y):
        pass

    def _on_drag_end(self, gesture, offset_x, offset_y):
        new_w = max(1, int(self.current_width + offset_x))
        new_h = max(1, int(self.current_height + offset_y))
        self.emit("resize-request", new_w, new_h)

    def set_canvas_size(self, width, height):
        self.current_width = width
        self.current_height = height
