"""
Manejo del portapapeles - copiar/pegar selecciones
"""
import cairo
import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk, Gdk, GObject


class ClipboardManager:
    """Gestiona operaciones de copiar/pegar con el portapapeles del sistema."""

    def __init__(self, window):
        self.window = window
        self.clipboard = Gdk.Display.get_default().get_clipboard()
        self.stored_surface = None
        self.stored_bounds = None

    def copy_selection(self, surface, bounds):
        """Copia una selección al portapapeles."""
        self.stored_surface = surface
        self.stored_bounds = bounds

        # También copiar como imagen PNG al portapapeles del sistema
        # Esto requiere implementación adicional con Gdk.Clipboard
        # Por ahora, almacenamos internamente

    def cut_selection(self, surface, bounds, target_surface):
        """Corta una selección (copia + borra)."""
        self.copy_selection(surface, bounds)

        # Borrar área seleccionada
        x, y, w, h = bounds
        ctx = cairo.Context(target_surface)
        ctx.set_operator(cairo.OPERATOR_CLEAR)
        ctx.rectangle(x, y, w, h)
        ctx.fill()

    def paste(self):
        """Pega la selección almacenada."""
        return self.stored_surface, self.stored_bounds

    def has_content(self):
        """Verifica si hay contenido en el portapapeles."""
        return self.stored_surface is not None
