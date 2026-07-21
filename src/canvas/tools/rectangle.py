"""
Herramienta Rectángulo
"""
import cairo
from src.canvas.tools.base_tool import BaseTool


class RectangleTool(BaseTool):
    """Herramienta rectángulo - contorno, contorno+relleno o solo relleno."""

    def __init__(self):
        super().__init__("Rectángulo", "tool-rectangle")
        self.start_x = 0
        self.start_y = 0
        self.fill_mode = "outline"  # 'outline' | 'outline_fill' | 'fill'
        self._active_button = 1

    def set_fill_mode(self, mode):
        if mode in ("outline", "outline_fill", "fill"):
            self.fill_mode = mode

    def on_press(self, canvas, x, y, button=1):
        self.is_drawing = True
        self.start_x = x
        self.start_y = y
        self._active_button = button
        canvas.image.clear_preview()

    def on_motion(self, canvas, x, y):
        if not self.is_drawing:
            return

        # Click izquierdo: borde=primario, relleno=secundario. Click derecho: al revés.
        border_color = self.primary_color if self._active_button != 3 else self.secondary_color
        fill_color = self.secondary_color if self._active_button != 3 else self.primary_color

        ctx = canvas.image.preview_context
        canvas.image.clear_preview()
        ctx.set_antialias(cairo.ANTIALIAS_DEFAULT)
        ctx.set_line_width(self.brush_size)

        x1, y1 = min(self.start_x, x), min(self.start_y, y)
        w, h = abs(x - self.start_x), abs(y - self.start_y)
        ctx.rectangle(x1, y1, w, h)

        if self.fill_mode == "fill":
            self._apply_color(ctx, border_color)
            ctx.fill()
        elif self.fill_mode == "outline_fill":
            self._apply_color(ctx, fill_color)
            ctx.fill_preserve()
            self._apply_color(ctx, border_color)
            ctx.stroke()
        else:  # outline
            self._apply_color(ctx, border_color)
            ctx.stroke()

        canvas.queue_draw()

    def on_release(self, canvas, x, y):
        self.is_drawing = False
        canvas.image.commit_preview()
        canvas.commit_drawing()

    def toggle_filled(self):
        """Compat: alterna entre contorno y solo-relleno."""
        self.fill_mode = "fill" if self.fill_mode == "outline" else "outline"
