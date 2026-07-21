"""Herramienta Selección"""
import cairo
from src.canvas.tools.base_tool import BaseTool

# Tamaño del handle en pixeles de PANTALLA (se ajusta por zoom al usarlo)
HANDLE_SCREEN_SIZE = 8
# Distancia extra de tolerancia al detectar el cursor sobre un handle (pantalla)
HANDLE_HIT_PADDING = 4

# Nombres de handle -> cursor GTK correspondiente
HANDLE_CURSORS = {
    "nw": "nw-resize",
    "n": "n-resize",
    "ne": "ne-resize",
    "e": "e-resize",
    "se": "se-resize",
    "s": "s-resize",
    "sw": "sw-resize",
    "w": "w-resize",
}


class SelectRectTool(BaseTool):
    """Herramienta selección rectangular."""

    def __init__(self):
        super().__init__("Selección", "tool-select")
        self.start_x = 0
        self.start_y = 0
        self.selection = None  # (x, y, w, h)
        self.has_selection = False
        self.marching_ants_offset = 0
        self.selection_surface = None  # Superficie de la selección extraída (a resolución original)
        self.is_moving = False  # Moviendo selección
        self.move_offset_x = 0
        self.move_offset_y = 0

        # --- Resize con handles ---
        self.is_resizing = False
        self.active_handle = None  # 'nw', 'n', 'ne', 'e', 'se', 's', 'sw', 'w'
        self._resize_orig_rect = None  # rect al iniciar el resize (x, y, w, h)

    def on_press(self, canvas, x, y, button=1):
        # 1. ¿Se hizo click sobre un handle de resize?
        if self.has_selection and self.selection:
            handle = self.get_handle_at(x, y, canvas.zoom)
            if handle:
                self.is_resizing = True
                self.active_handle = handle
                self._resize_orig_rect = self.selection
                return

        # 2. ¿Click dentro de la selección? -> mover
        if self.has_selection and self._point_in_selection(x, y):
            self.is_moving = True
            self.move_offset_x = x - self.selection[0]
            self.move_offset_y = y - self.selection[1]

            # BORRAR el área original del canvas (dejar blanco)
            sx, sy, sw, sh = self.selection
            ctx = canvas.image.context
            ctx.set_source_rgb(1, 1, 1)  # Blanco
            ctx.rectangle(sx, sy, sw, sh)
            ctx.fill()
            canvas.commit_drawing()

            return

        # 3. Nueva selección
        self.is_drawing = True
        self.start_x = x
        self.start_y = y
        canvas.image.clear_preview()

    def _point_in_selection(self, x, y):
        """Verifica si un punto está dentro de la selección."""
        if not self.selection:
            return False
        sx, sy, sw, sh = self.selection
        return sx <= x <= sx + sw and sy <= y <= sy + sh

    def get_handle_at(self, x, y, zoom):
        """Devuelve el nombre del handle bajo el punto (x, y) en coords de canvas, o None."""
        if not self.selection:
            return None

        sx, sy, sw, sh = self.selection
        tolerance = (HANDLE_SCREEN_SIZE / 2 + HANDLE_HIT_PADDING) / max(zoom, 0.0001)

        cx, cy = sx + sw / 2, sy + sh / 2
        points = {
            "nw": (sx, sy), "n": (cx, sy), "ne": (sx + sw, sy),
            "e": (sx + sw, cy), "se": (sx + sw, sy + sh), "s": (cx, sy + sh),
            "sw": (sx, sy + sh), "w": (sx, cy),
        }
        for name, (hx, hy) in points.items():
            if abs(x - hx) <= tolerance and abs(y - hy) <= tolerance:
                return name
        return None

    def get_cursor_name_at(self, x, y, zoom):
        """Devuelve el nombre de cursor GTK apropiado para la posición dada."""
        handle = self.get_handle_at(x, y, zoom)
        if handle:
            return HANDLE_CURSORS[handle]
        if self.has_selection and self._point_in_selection(x, y):
            return "grab"
        return "default"

    def on_motion(self, canvas, x, y):
        if self.is_resizing and self._resize_orig_rect:
            self._update_resize(canvas, x, y)
            return

        if self.is_moving and self.has_selection:
            new_x = int(round(x - self.move_offset_x))
            new_y = int(round(y - self.move_offset_y))
            w, h = self.selection[2], self.selection[3]
            self.selection = (new_x, new_y, w, h)

            canvas.image.clear_preview()
            if self.selection_surface:
                ctx = canvas.image.preview_context
                ctx.set_source_surface(self.selection_surface, new_x, new_y)
                ctx.paint()

            canvas.queue_draw()
            return

        if not self.is_drawing:
            return

        x1, y1 = int(min(self.start_x, x)), int(min(self.start_y, y))
        w, h = int(abs(x - self.start_x)), int(abs(y - self.start_y))

        ctx = canvas.image.preview_context
        canvas.image.clear_preview()

        ctx.set_source_rgb(0, 0, 0)
        ctx.set_line_width(1)
        ctx.set_dash([4, 4], self.marching_ants_offset)
        ctx.rectangle(x1, y1, w, h)
        ctx.stroke()
        ctx.set_dash([])

        ctx.set_source_rgba(0.2, 0.4, 0.8, 0.1)
        ctx.rectangle(x1, y1, w, h)
        ctx.fill()

        self.selection = (x1, y1, w, h)
        self.has_selection = w > 2 and h > 2

        canvas.queue_draw()

    def _update_resize(self, canvas, x, y):
        """Recalcula la selección mientras se arrastra un handle, y previsualiza escalado."""
        ox, oy, ow, oh = self._resize_orig_rect
        handle = self.active_handle

        left, top, right, bottom = ox, oy, ox + ow, oy + oh

        if "n" in handle:
            top = y
        if "s" in handle:
            bottom = y
        if "w" in handle:
            left = x
        if "e" in handle:
            right = x

        # Evitar que se invierta (mantener un tamaño mínimo)
        min_size = 2
        if right - left < min_size:
            if "w" in handle:
                left = right - min_size
            else:
                right = left + min_size
        if bottom - top < min_size:
            if "n" in handle:
                top = bottom - min_size
            else:
                bottom = top + min_size

        # Redondear todo a enteros: mantiene la selección alineada al grid de
        # píxeles en todo momento, para que extracción/borrado/pintado usen
        # siempre exactamente el mismo rectángulo (evita dejar una franja
        # residual del contenido original al mover la selección después).
        new_x = int(round(left))
        new_y = int(round(top))
        new_w = max(int(round(right - left)), 1)
        new_h = max(int(round(bottom - top)), 1)
        self.selection = (new_x, new_y, new_w, new_h)

        # Previsualizar el contenido original escalado al nuevo tamaño
        canvas.image.clear_preview()
        if self.selection_surface:
            src_w = self.selection_surface.get_width()
            src_h = self.selection_surface.get_height()
            if src_w > 0 and src_h > 0:
                ctx = canvas.image.preview_context
                ctx.save()
                ctx.rectangle(new_x, new_y, new_w, new_h)
                ctx.clip()
                ctx.translate(new_x, new_y)
                ctx.scale(new_w / src_w, new_h / src_h)
                ctx.set_source_surface(self.selection_surface, 0, 0)
                ctx.get_source().set_filter(cairo.FILTER_GOOD)
                ctx.paint()
                ctx.restore()

        canvas.queue_draw()

    def on_release(self, canvas, x, y):
        if self.is_resizing:
            self.is_resizing = False
            self.active_handle = None
            self._resize_orig_rect = None

            # Componer el contenido escalado definitivamente sobre el canvas
            # (self.selection ya llega con coordenadas enteras desde _update_resize)
            if self.selection_surface and self.selection:
                sx, sy, sw, sh = self.selection

                src_w = self.selection_surface.get_width()
                src_h = self.selection_surface.get_height()

                ctx = canvas.image.context
                ctx.save()
                # Clip estricto al rectángulo destino: evita que el filtro de
                # escalado "sangre" color fuera de los límites de la selección.
                ctx.rectangle(sx, sy, sw, sh)
                ctx.clip()
                ctx.translate(sx, sy)
                ctx.scale(sw / src_w, sh / src_h)
                ctx.set_source_surface(self.selection_surface, 0, 0)
                ctx.get_source().set_filter(cairo.FILTER_GOOD)
                ctx.paint()
                ctx.restore()
                canvas.commit_drawing()

                # Re-extraer a la nueva resolución para que sucesivos resizes partan de aquí
                self._extract_selection(canvas)

            canvas.image.clear_preview()
            canvas.queue_draw()
            return

        if self.is_moving:
            self.is_moving = False

            # Pegar la selección en la nueva posición
            if self.selection_surface and self.selection:
                sx, sy, sw, sh = self.selection
                ctx = canvas.image.context
                ctx.set_source_surface(self.selection_surface, sx, sy)
                ctx.paint()
                canvas.commit_drawing()

            # NO limpiar la selección - queda activa para seguir moviendo
            canvas.queue_draw()
            return

        self.is_drawing = False
        if self.has_selection and self.selection:
            self._extract_selection(canvas)
        canvas.image.clear_preview()
        canvas.queue_draw()

    def _extract_selection(self, canvas):
        """Extrae la imagen seleccionada del canvas."""
        if not self.selection:
            return

        x, y, w, h = self.selection
        x, y, w, h = int(x), int(y), int(w), int(h)

        if w <= 0 or h <= 0:
            return
        # Crear superficie con la selección
        self.selection_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        ctx = cairo.Context(self.selection_surface)
        ctx.set_source_surface(canvas.image.surface, -x, -y)
        ctx.paint()

    def clear_selection(self):
        """Limpia la selección actual."""
        self.selection = None
        self.has_selection = False
        self.selection_surface = None
        self.is_resizing = False
        self.active_handle = None
        self._resize_orig_rect = None

    def get_selection_surface(self):
        """Devuelve la superficie de la selección."""
        return self.selection_surface

    def get_selection_bounds(self):
        """Devuelve los límites de la selección."""
        return self.selection

    def draw_handles(self, ctx, zoom):
        """Dibuja los 8 handles de resize sobre la selección actual."""
        if not self.has_selection or not self.selection:
            return

        sx, sy, sw, sh = self.selection
        size = HANDLE_SCREEN_SIZE / zoom
        half = size / 2

        cx, cy = sx + sw / 2, sy + sh / 2
        points = [
            (sx, sy), (cx, sy), (sx + sw, sy),
            (sx + sw, cy), (sx + sw, sy + sh), (cx, sy + sh),
            (sx, sy + sh), (sx, cy),
        ]

        ctx.save()
        for hx, hy in points:
            ctx.rectangle(hx - half, hy - half, size, size)
            ctx.set_source_rgb(1, 1, 1)
            ctx.fill_preserve()
            ctx.set_source_rgb(0, 0, 0)
            ctx.set_line_width(1 / zoom)
            ctx.stroke()
        ctx.restore()
