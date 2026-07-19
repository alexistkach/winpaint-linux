"""
Herramienta Selección
"""
import cairo
from src.canvas.tools.base_tool import BaseTool


class SelectRectTool(BaseTool):
    """Herramienta selección rectangular."""

    def __init__(self):
        super().__init__("Selección", "tool-select")
        self.start_x = 0
        self.start_y = 0
        self.selection = None  # (x, y, w, h)
        self.has_selection = False
        self.marching_ants_offset = 0

    def on_press(self, canvas, x, y, button=1):
        self.is_drawing = True
        self.start_x = x
        self.start_y = y
        canvas.image.clear_preview()

    def on_motion(self, canvas, x, y):
        if not self.is_drawing:
            return

        ctx = canvas.image.preview_context
        canvas.image.clear_preview()

        x1, y1 = min(self.start_x, x), min(self.start_y, y)
        w, h = abs(x - self.start_x), abs(y - self.start_y)

        # Dibujar rectángulo de selección con marching ants
        ctx.set_source_rgb(0, 0, 0)
        ctx.set_line_width(1)
        ctx.set_dash([4, 4], self.marching_ants_offset)
        ctx.rectangle(x1, y1, w, h)
        ctx.stroke()
        ctx.set_dash([])

        self.selection = (x1, y1, w, h)
        self.has_selection = w > 2 and h > 2

        canvas.queue_draw()

    def on_release(self, canvas, x, y):
        self.is_drawing = False
        canvas.image.clear_preview()
        canvas.queue_draw()

    def clear_selection(self):
        """Limpia la selección actual."""
        self.selection = None
        self.has_selection = False

    def get_selection_surface(self, canvas):
        """Obtiene la superficie de la selección."""
        if not self.has_selection or not self.selection:
            return None

        x, y, w, h = self.selection
        sub_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        ctx = cairo.Context(sub_surface)
        ctx.set_source_surface(canvas.image.surface, -x, -y)
        ctx.paint()

        return sub_surface
