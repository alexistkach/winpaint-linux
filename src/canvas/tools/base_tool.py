"""
Clase base para todas las herramientas de dibujo
"""
from abc import ABC, abstractmethod


class BaseTool(ABC):
    """Clase base abstracta para herramientas de dibujo."""

    def __init__(self, name, icon_name=""):
        self.name = name
        self.icon_name = icon_name
        self.primary_color = (0, 0, 0)
        self.secondary_color = (1, 1, 1)
        self.brush_size = 3
        self.is_drawing = False

    def set_colors(self, primary, secondary):
        """Establece los colores primario y secundario."""
        self.primary_color = primary
        self.secondary_color = secondary

    def set_brush_size(self, size):
        """Establece el tamaño del pincel."""
        self.brush_size = max(1, size)

    @abstractmethod
    def on_press(self, canvas, x, y, button=1):
        """Se llama cuando se presiona el botón del mouse."""
        pass

    @abstractmethod
    def on_motion(self, canvas, x, y):
        """Se llama cuando se mueve el mouse mientras se presiona."""
        pass

    @abstractmethod
    def on_release(self, canvas, x, y):
        """Se llama cuando se suelta el botón del mouse."""
        pass

    def _get_color_for_button(self, button):
        """Devuelve el color según el botón del mouse (1=primario, 3=secundario)."""
        if button == 3:
            return self.secondary_color
        return self.primary_color

    def _apply_color(self, ctx, color):
        """Aplica un color RGB al contexto de Cairo."""
        ctx.set_source_rgb(color[0], color[1], color[2])

    def _apply_color_rgba(self, ctx, color):
        """Aplica un color RGBA al contexto de Cairo."""
        if len(color) == 4:
            ctx.set_source_rgba(color[0], color[1], color[2], color[3])
        else:
            ctx.set_source_rgb(color[0], color[1], color[2])
