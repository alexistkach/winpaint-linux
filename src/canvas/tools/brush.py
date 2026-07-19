"""
Herramienta Pincel
"""
import cairo
import math
from src.canvas.tools.base_tool import BaseTool


class BrushTool(BaseTool):
    """Herramienta pincel - dibuja con diferentes tamaños y bordes suaves."""

    def __init__(self):
        super().__init__("Pincel", "tool-brush")
        self.last_x = 0
        self.last_y = 0

    def on_press(self, canvas, x, y, button=1):
        self.is_drawing = True
        self.last_x = x
        self.last_y = y

        color = self._get_color_for_button(button)
        ctx = canvas.image.context

        ctx.set_antialias(cairo.ANTIALIAS_DEFAULT)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.set_line_width(self.brush_size)
        self._apply_color(ctx, color)

        # Dibujar punto inicial
        ctx.arc(x, y, self.brush_size / 2, 0, 2 * math.pi)
        ctx.fill()

        ctx.move_to(x, y)

        canvas.queue_draw()

    def on_motion(self, canvas, x, y):
        if not self.is_drawing:
            return

        ctx = canvas.image.context
        ctx.set_antialias(cairo.ANTIALIAS_DEFAULT)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.set_line_width(self.brush_size)

        ctx.line_to(x, y)
        ctx.stroke()
        ctx.move_to(x, y)

        self.last_x = x
        self.last_y = y

        canvas.queue_draw()

    def on_release(self, canvas, x, y):
        self.is_drawing = False
        canvas.commit_drawing()
