"""
Herramienta Línea
"""
import cairo
from src.canvas.tools.base_tool import BaseTool


class LineTool(BaseTool):
    """Herramienta línea - dibuja líneas rectas."""

    def __init__(self):
        super().__init__("Línea", "tool-line")
        self.start_x = 0
        self.start_y = 0

    def on_press(self, canvas, x, y, button=1):
        self.is_drawing = True
        self.start_x = x
        self.start_y = y
        canvas.image.clear_preview()

    def on_motion(self, canvas, x, y):
        if not self.is_drawing:
            return

        color = self._get_color_for_button(1)  # Siempre usa color primario
        ctx = canvas.image.preview_context

        canvas.image.clear_preview()

        ctx.set_antialias(cairo.ANTIALIAS_DEFAULT)
        ctx.set_line_width(self.brush_size)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        self._apply_color(ctx, color)

        ctx.move_to(self.start_x, self.start_y)
        ctx.line_to(x, y)
        ctx.stroke()

        canvas.queue_draw()

    def on_release(self, canvas, x, y):
        self.is_drawing = False
        canvas.image.commit_preview()
        canvas.commit_drawing()
