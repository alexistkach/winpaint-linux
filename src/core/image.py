"""
Modelo de imagen - maneja el buffer de píxeles y operaciones
"""
import cairo
from PIL import Image
import io

from src.core.constants import DEFAULT_CANVAS_WIDTH, DEFAULT_CANVAS_HEIGHT


class PaintImage:
    """Representa una imagen editable en memoria."""

    def __init__(self, width=DEFAULT_CANVAS_WIDTH, height=DEFAULT_CANVAS_HEIGHT):
        self.width = width
        self.height = height

        # Surface principal (RGBA para soporte de transparencia)
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        self.context = cairo.Context(self.surface)

        # Fondo blanco por defecto
        self.context.set_source_rgb(1, 1, 1)
        self.context.paint()

        # Surface de preview (para dibujar formas mientras se arrastra)
        self.preview_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        self.preview_context = cairo.Context(self.preview_surface)
        self.preview_context.set_operator(cairo.OPERATOR_CLEAR)
        self.preview_context.paint()
        self.preview_context.set_operator(cairo.OPERATOR_OVER)

        self.filename = None
        self.modified = False

    def resize(self, new_width, new_height, anchor="topleft"):
        """Redimensiona la imagen."""
        new_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, new_width, new_height)
        ctx = cairo.Context(new_surface)

        # Fondo blanco
        ctx.set_source_rgb(1, 1, 1)
        ctx.paint()

        # Copiar imagen existente según ancla
        if anchor == "topleft":
            ctx.set_source_surface(self.surface, 0, 0)
        elif anchor == "center":
            x = (new_width - self.width) // 2
            y = (new_height - self.height) // 2
            ctx.set_source_surface(self.surface, x, y)

        ctx.paint()

        self.surface = new_surface
        self.context = cairo.Context(self.surface)
        self.width = new_width
        self.height = new_height
        self._recreate_preview()
        self.modified = True

    def _recreate_preview(self):
        """Recrea el surface de preview con las nuevas dimensiones."""
        self.preview_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)
        self.preview_context = cairo.Context(self.preview_surface)
        self.preview_context.set_operator(cairo.OPERATOR_CLEAR)
        self.preview_context.paint()
        self.preview_context.set_operator(cairo.OPERATOR_OVER)

    def clear_preview(self):
        """Limpia el surface de preview."""
        self.preview_context.set_operator(cairo.OPERATOR_CLEAR)
        self.preview_context.paint()
        self.preview_context.set_operator(cairo.OPERATOR_OVER)

    def commit_preview(self):
        """Aplica el preview al surface principal."""
        self.context.set_source_surface(self.preview_surface, 0, 0)
        self.context.paint()
        self.clear_preview()
        self.modified = True

    def get_combined_surface(self):
        """Devuelve una superficie combinada (principal + preview)."""
        combined = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)
        ctx = cairo.Context(combined)

        ctx.set_source_surface(self.surface, 0, 0)
        ctx.paint()

        ctx.set_source_surface(self.preview_surface, 0, 0)
        ctx.paint()

        return combined

    def save(self, filepath, format_name="png", quality=90):
        """Guarda la imagen en disco."""
        if format_name.lower() in ["jpg", "jpeg"]:
            # Cairo no soporta JPG directamente, usar PIL
            buf = self._get_png_buffer()
            img = Image.open(buf)
            if img.mode == "RGBA":
                # Convertir a RGB con fondo blanco para JPG
                background = Image.new("RGB", img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3])
                img = background
            img.save(filepath, "JPEG", quality=quality)
        else:
            self.surface.write_to_png(filepath)

        self.filename = filepath
        self.modified = False

    def load(self, filepath):
        """Carga una imagen desde disco."""
        img = Image.open(filepath)

        # Convertir a RGBA si es necesario
        if img.mode != "RGBA":
            img = img.convert("RGBA")

        self.width, self.height = img.size

        # Crear nuevo surface
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)
        self.context = cairo.Context(self.surface)

        # Copiar datos de PIL a Cairo
        data = img.tobytes("raw", "BGRA")
        self.surface.get_data()[:] = data
        self.surface.mark_dirty()

        self._recreate_preview()
        self.filename = filepath
        self.modified = False

    def _get_png_buffer(self):
        """Devuelve un buffer PNG de la imagen actual."""
        buf = io.BytesIO()
        self.surface.write_to_png(buf)
        buf.seek(0)
        return buf

    def new(self, width, height):
        """Crea una nueva imagen en blanco."""
        self.width = width
        self.height = height
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        self.context = cairo.Context(self.surface)
        self.context.set_source_rgb(1, 1, 1)
        self.context.paint()
        self._recreate_preview()
        self.filename = None
        self.modified = False

    def get_pixel_color(self, x, y):
        """Obtiene el color de un píxel específico."""
        if 0 <= x < self.width and 0 <= y < self.height:
            # Leer directamente del buffer
            stride = self.surface.get_stride()
            data = self.surface.get_data()
            offset = y * stride + x * 4
            # BGRA format
            b = data[offset] / 255.0
            g = data[offset + 1] / 255.0
            r = data[offset + 2] / 255.0
            a = data[offset + 3] / 255.0
            return (r, g, b, a)
        return (1, 1, 1, 1)
