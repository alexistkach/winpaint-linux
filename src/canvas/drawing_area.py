"""Area de dibujo principal"""
import cairo
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
from gi.repository import Gtk, Gdk, GObject

from src.core.image import PaintImage
from src.core.constants import DEFAULT_CANVAS_WIDTH, DEFAULT_CANVAS_HEIGHT
from src.canvas.history import HistoryManager
from src.canvas.tools import (
    PencilTool, BrushTool, LineTool, RectangleTool,
    EllipseTool, EraserTool, FillTool, TextTool, SelectRectTool, SelectFreeTool
)

class DrawingArea(Gtk.DrawingArea):
    __gsignals__ = {
        "coordinates-changed": (GObject.SIGNAL_RUN_FIRST, None, (str,)),
        "image-modified": (GObject.SIGNAL_RUN_FIRST, None, (bool,)),
        "tool-changed": (GObject.SIGNAL_RUN_FIRST, None, (str,)),
        "resize-request": (GObject.SIGNAL_RUN_FIRST, None, (int, int)),
    }

    def __init__(self):
        super().__init__()
        self.image = PaintImage(DEFAULT_CANVAS_WIDTH, DEFAULT_CANVAS_HEIGHT)
        # Forzar tamano natural 0 para que el layout no expanda
        self.set_size_request(100, 100)  # Minimo visible pero pequeno
        self.history = HistoryManager(max_history=50)
        self.history.push_state(self.image.surface)
        self.tools = {
            "pencil": PencilTool(), "brush": BrushTool(), "line": LineTool(),
            "rectangle": RectangleTool(), "ellipse": EllipseTool(),
            "eraser": EraserTool(), "fill": FillTool(), "text": TextTool(),
            "select_rect": SelectRectTool(),
            "select_free": SelectFreeTool(),            
        }
        self.current_tool_name = "pencil"
        self.current_tool = self.tools["pencil"]
        self.primary_color = (0, 0, 0)
        self.secondary_color = (1, 1, 1)
        self._update_tool_colors()
        self.set_draw_func(self._draw, None)
        self._setup_events()
        self.zoom = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.text_entry = None
        self.text_entry_active = False

    def _setup_events(self):
        click = Gtk.GestureClick.new()
        click.set_button(0)
        click.connect("pressed", self._on_button_press)
        click.connect("released", self._on_button_release)
        self.add_controller(click)
        motion = Gtk.EventControllerMotion.new()
        motion.connect("motion", self._on_motion)
        self.add_controller(motion)
        scroll = Gtk.EventControllerScroll.new(Gtk.EventControllerScrollFlags.VERTICAL)
        scroll.connect("scroll", self._on_scroll)
        self.add_controller(scroll)

    def _draw(self, area, ctx, width, height, data):
            """Funcion de dibujo del widget."""
            # Fondo del area (gris como Paint)
            ctx.set_source_rgb(0.5, 0.5, 0.5)
            ctx.paint()
            
            # Calcular offset para centrar el canvas
            img_w = self.image.width * self.zoom
            img_h = self.image.height * self.zoom
            self.offset_x = max(0, (width - img_w) / 2)
            self.offset_y = max(0, (height - img_h) / 2)
            
            # Aplicar zoom y offset
            ctx.save()
            ctx.translate(self.offset_x, self.offset_y)
            ctx.scale(self.zoom, self.zoom)
            
            # Dibujar imagen principal
            ctx.set_source_surface(self.image.surface, 0, 0)
            ctx.paint()
            
            # Dibujar preview
            ctx.set_source_surface(self.image.preview_surface, 0, 0)
            ctx.paint()
            
            # Marching ants
            if self.current_tool_name == "select_rect" and self.current_tool.has_selection:
                self._draw_selection_marching_ants(ctx)
            
            ctx.restore()

    def _draw_selection_marching_ants(self, ctx):
        if not self.current_tool.selection:
            return
        x, y, w, h = self.current_tool.selection
        ctx.set_source_rgb(0, 0, 0)
        ctx.set_line_width(1 / self.zoom)
        ctx.set_dash([4 / self.zoom, 4 / self.zoom], self.current_tool.marching_ants_offset)
        ctx.rectangle(x, y, w, h)
        ctx.stroke()
        ctx.set_dash([])

    def _get_canvas_coords(self, widget_x, widget_y):
        return (widget_x - self.offset_x) / self.zoom, (widget_y - self.offset_y) / self.zoom

    def _on_button_press(self, gesture, n_press, x, y):
        if self.text_entry_active:
            return
        canvas_x, canvas_y = self._get_canvas_coords(x, y)
        button = gesture.get_current_button()
        self.current_tool.on_press(self, canvas_x, canvas_y, button)
        self._update_coordinates(canvas_x, canvas_y)

    def _on_motion(self, controller, x, y):
        canvas_x, canvas_y = self._get_canvas_coords(x, y)
        
        # Cambiar cursor si estamos sobre selección
        if self.current_tool_name in ("select_rect", "select_free") and self.current_tool.has_selection:
            if self.current_tool._point_in_selection(canvas_x, canvas_y):
                self.set_cursor_from_name("grab")
            else:
                self.set_cursor_from_name("default")
        
        if self.current_tool.is_drawing or getattr(self.current_tool, 'is_moving', False):
            self.current_tool.on_motion(self, canvas_x, canvas_y)
        
        self._update_coordinates(canvas_x, canvas_y)

    def _on_button_release(self, gesture, n_press, x, y):
        canvas_x, canvas_y = self._get_canvas_coords(x, y)
        self.current_tool.on_release(self, canvas_x, canvas_y)

    def _on_scroll(self, controller, dx, dy):
        if controller.get_current_event_state() & Gdk.ModifierType.CONTROL_MASK:
            if dy < 0:
                self.zoom_in()
            else:
                self.zoom_out()
            return True
        return False

    def _update_coordinates(self, x, y):
        self.emit("coordinates-changed", f"{int(x)}, {int(y)} px")

    def _update_tool_colors(self):
        for tool in self.tools.values():
            tool.set_colors(self.primary_color, self.secondary_color)

    def set_tool(self, tool_name):
        if tool_name in self.tools:
            self.current_tool_name = tool_name
            self.current_tool = self.tools[tool_name]
            self.emit("tool-changed", tool_name)

    def set_primary_color(self, color):
        self.primary_color = color
        self._update_tool_colors()

    def set_secondary_color(self, color):
        self.secondary_color = color
        self._update_tool_colors()

    def set_brush_size(self, size):
        for tool in self.tools.values():
            tool.set_brush_size(size)

    def commit_drawing(self):
        self.history.push_state(self.image.surface)
        self.image.modified = True
        self.emit("image-modified", True)

    def undo(self):
        if self.history.can_undo():
            self.history.undo(self.image.surface)
            self.image.modified = True
            self.queue_draw()
            self.emit("image-modified", True)

    def redo(self):
        if self.history.can_redo():
            self.history.redo(self.image.surface)
            self.image.modified = True
            self.queue_draw()
            self.emit("image-modified", True)

    def zoom_in(self):
        self.zoom = min(self.zoom * 2, 8.0)
        self.queue_draw()

    def zoom_out(self):
        self.zoom = max(self.zoom / 2, 0.125)
        self.queue_draw()

    def zoom_reset(self):
        self.zoom = 1.0
        self.queue_draw()

    def new_image(self, width, height):
        self.image.new(width, height)
        self.history.clear()
        self.history.push_state(self.image.surface)
        self.queue_draw()
        self.emit("image-modified", False)
        self.emit("resize-request", width, height)

    def open_image(self, filepath):
        try:
            self.image.load(filepath)
            self.history.clear()
            self.history.push_state(self.image.surface)
            self.queue_draw()
            self.emit("image-modified", False)
            self.emit("resize-request", self.image.width, self.image.height)
            return True
        except Exception as e:
            print(f"Error al abrir imagen: {e}")
            return False

    def save_image(self, filepath, format_name="png"):
        try:
            self.image.save(filepath, format_name)
            self.emit("image-modified", False)
            return True
        except Exception as e:
            print(f"Error al guardar imagen: {e}")
            return False

    def show_text_entry(self, x, y):
        self.text_entry_active = True

    def get_image_dimensions(self):
        return self.image.width, self.image.height

    def is_modified(self):
        return self.image.modified

    def resize_image(self, new_width, new_height):
        self.image.resize(new_width, new_height)
        self.history.push_state(self.image.surface)
        self.queue_draw()
        self.emit("image-modified", True)
        self.emit("resize-request", new_width, new_height)
