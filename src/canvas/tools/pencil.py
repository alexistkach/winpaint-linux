"""
Herramienta Lápiz
"""
import cairo
from src.canvas.tools.base_tool import BaseTool


class PencilTool(BaseTool):
    """Herramienta lápiz - dibuja líneas de 1px sin anti-aliasing."""

    def __init__(self):
        super().__init__("Lápiz", "tool-pencil")
        self.last_x = 0
        self.last_y = 0

    def on_press(self, canvas, x, y, button=1):
        self.is_drawing = True
        self.last_x = int(x)
        self.last_y = int(y)

        color = self._get_color_for_button(button)
        ctx = canvas.image.context

        ctx.set_antialias(cairo.ANTIALIAS_NONE)
        ctx.set_line_width(1)
        self._apply_color(ctx, color)

        # Dibujar punto inicial
        ctx.rectangle(self.last_x, self.last_y, 1, 1)
        ctx.fill()

        canvas.queue_draw()

    def on_motion(self, canvas, x, y):
        if not self.is_drawing:
            return

        x = int(x)
        y = int(y)

        ctx = canvas.image.context
        ctx.set_antialias(cairo.ANTIALIAS_NONE)
        ctx.set_line_width(1)

        # Dibujar línea Bresenham-like
        ctx.move_to(self.last_x + 0.5, self.last_y + 0.5)
        ctx.line_to(x + 0.5, y + 0.5)
        ctx.stroke()

        self.last_x = x
        self.last_y = y

        canvas.queue_draw()

    def on_release(self, canvas, x, y):
        self.is_drawing = False
        canvas.commit_drawing()
