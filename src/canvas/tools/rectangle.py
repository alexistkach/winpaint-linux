"""
Herramienta Rectángulo
"""
import cairo
from src.canvas.tools.base_tool import BaseTool


class RectangleTool(BaseTool):
    """Herramienta rectángulo - dibuja rectángulos con o sin relleno."""

    def __init__(self):
        super().__init__("Rectángulo", "tool-rectangle")
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

        x1, y1 = min(self.start_x, x), min(self.start_y, y)
        w, h = abs(x - self.start_x), abs(y - self.start_y)

        if self.filled:
            ctx.rectangle(x1, y1, w, h)
            ctx.fill()
        else:
            # Para bordes finos, ajustar coordenadas
            ctx.rectangle(x1, y1, w, h)
            ctx.stroke()

        canvas.queue_draw()

    def on_release(self, canvas, x, y):
        self.is_drawing = False
        canvas.image.commit_preview()
        canvas.commit_drawing()

    def toggle_filled(self):
        """Alterna entre rectángulo relleno y vacío."""
        self.filled = not self.filled
