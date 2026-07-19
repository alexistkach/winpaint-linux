"""
Herramienta Borrador
"""
import cairo
import math
from src.canvas.tools.base_tool import BaseTool


class EraserTool(BaseTool):
    """Herramienta borrador - borra áreas reemplazándolas con el color secundario."""

    def __init__(self):
        super().__init__("Borrador", "tool-eraser")
        self.last_x = 0
        self.last_y = 0

    def on_press(self, canvas, x, y, button=1):
        self.is_drawing = True
        self.last_x = x
        self.last_y = y

        ctx = canvas.image.context
        ctx.set_antialias(cairo.ANTIALIAS_DEFAULT)
        ctx.set_line_cap(cairo.LINE_CAP_SQUARE)
        ctx.set_line_join(cairo.LINE_JOIN_MITER)
        ctx.set_line_width(self.brush_size)
        self._apply_color(ctx, self.secondary_color)

        # Borrar punto inicial
        half = self.brush_size / 2
        ctx.rectangle(x - half, y - half, self.brush_size, self.brush_size)
        ctx.fill()

        ctx.move_to(x, y)
        canvas.queue_draw()

    def on_motion(self, canvas, x, y):
        if not self.is_drawing:
            return

        ctx = canvas.image.context
        ctx.set_antialias(cairo.ANTIALIAS_DEFAULT)
        ctx.set_line_cap(cairo.LINE_CAP_SQUARE)
        ctx.set_line_join(cairo.LINE_JOIN_MITER)
        ctx.set_line_width(self.brush_size)
        self._apply_color(ctx, self.secondary_color)

        ctx.line_to(x, y)
        ctx.stroke()
        ctx.move_to(x, y)

        self.last_x = x
        self.last_y = y

        canvas.queue_draw()

    def on_release(self, canvas, x, y):
        self.is_drawing = False
        canvas.commit_drawing()
