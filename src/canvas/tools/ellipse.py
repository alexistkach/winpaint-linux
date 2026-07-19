"""
Herramienta Elipse
"""
import cairo
import math
from src.canvas.tools.base_tool import BaseTool


class EllipseTool(BaseTool):
    """Herramienta elipse - dibuja óvalos con o sin relleno."""

    def __init__(self):
        super().__init__("Elipse", "tool-ellipse")
        self.start_x = 0
        self.start_y = 0
        self.filled = False

    def on_press(self, canvas, x, y, button=1):
        self.is_drawing = True
        self.start_x = x
        self.start_y = y
        canvas.image.clear_preview()

    def on_motion(self, canvas, x, y):
        if not self.is_drawing:
            return

        color = self._get_color_for_button(1)
        ctx = canvas.image.preview_context

        canvas.image.clear_preview()

        ctx.set_antialias(cairo.ANTIALIAS_DEFAULT)
        ctx.set_line_width(self.brush_size)
        self._apply_color(ctx, color)

        center_x = (self.start_x + x) / 2
        center_y = (self.start_y + y) / 2
        radius_x = abs(x - self.start_x) / 2
        radius_y = abs(y - self.start_y) / 2

        ctx.save()
        ctx.translate(center_x, center_y)
        ctx.scale(radius_x or 1, radius_y or 1)
        ctx.arc(0, 0, 1, 0, 2 * math.pi)
        ctx.restore()

        if self.filled:
            ctx.fill()
        else:
            ctx.stroke()

        canvas.queue_draw()

    def on_release(self, canvas, x, y):
        self.is_drawing = False
        canvas.image.commit_preview()
        canvas.commit_drawing()

    def toggle_filled(self):
        """Alterna entre elipse rellena y vacía."""
        self.filled = not self.filled
