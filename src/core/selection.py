"""
Lógica de selección - maneja selecciones rectangulares y libres
"""
import cairo


class Selection:
    """Representa una selección en la imagen."""

    def __init__(self):
        self.rect = None  # (x, y, w, h) para selección rectangular
        self.path = None  # Lista de puntos para selección libre
        self.surface = None  # Superficie de la selección
        self.active = False
        self.marching_ants_offset = 0

    def set_rect(self, x, y, w, h):
        """Establece una selección rectangular."""
        self.rect = (x, y, w, h)
        self.path = None
        self.active = True

    def set_free_path(self, points):
        """Establece una selección libre."""
        self.path = points
        self.rect = None
        self.active = True

    def clear(self):
        """Limpia la selección."""
        self.rect = None
        self.path = None
        self.surface = None
        self.active = False

    def get_bounds(self):
        """Devuelve los límites de la selección."""
        if self.rect:
            return self.rect
        elif self.path:
            xs = [p[0] for p in self.path]
            ys = [p[1] for p in self.path]
            return (min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys))
        return None

    def extract(self, source_surface):
        """Extrae la selección de una superficie."""
        bounds = self.get_bounds()
        if not bounds:
            return None

        x, y, w, h = bounds
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        ctx = cairo.Context(self.surface)
        ctx.set_source_surface(source_surface, -x, -y)

        if self.path:
            # Clip por path para selección libre
            ctx.move_to(self.path[0][0] - x, self.path[0][1] - y)
            for px, py in self.path[1:]:
                ctx.line_to(px - x, py - y)
            ctx.close_path()
            ctx.clip()

        ctx.paint()
        return self.surface

    def draw_marching_ants(self, ctx):
        """Dibuja el borde de selección animado."""
        if not self.active:
            return

        bounds = self.get_bounds()
        if not bounds:
            return

        x, y, w, h = bounds

        ctx.save()
        ctx.set_source_rgb(0, 0, 0)
        ctx.set_line_width(1)
        ctx.set_dash([4, 4], self.marching_ants_offset)

        if self.path:
            ctx.move_to(self.path[0][0], self.path[0][1])
            for px, py in self.path[1:]:
                ctx.line_to(px, py)
            ctx.close_path()
        else:
            ctx.rectangle(x, y, w, h)

        ctx.stroke()
        ctx.restore()

        # Actualizar offset para animación
        self.marching_ants_offset = (self.marching_ants_offset + 1) % 8
