"""Manejo del portapapeles - copiar/pegar selecciones"""
import cairo
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk, GObject, Gio
import io


class ClipboardManager:
    """Gestiona operaciones de copiar/pegar con el portapapeles del sistema."""
    
    def __init__(self, window):
        self.window = window
        self.clipboard = Gdk.Display.get_default().get_clipboard()
        self.stored_surface = None
        self.stored_bounds = None
    
    def copy_selection(self, surface, bounds):
        """Copia una selección al portapapeles del sistema como PNG."""
        self.stored_surface = surface
        self.stored_bounds = bounds
        
        if surface is None:
            return
        
        # Serializar a PNG bytes
        buf = io.BytesIO()
        surface.write_to_png(buf)
        png_bytes = buf.getvalue()
        
        # Crear Gdk.Texture desde los bytes PNG
        try:
            texture = Gdk.Texture.new_from_bytes(GLib.Bytes.new(png_bytes))
            self.clipboard.set_texture(texture)
        except Exception as e:
            print(f"Error al copiar al portapapeles: {e}")
    
    def cut_selection(self, surface, bounds, target_surface):
        """Corta una selección (copia + borra)."""
        self.copy_selection(surface, bounds)
        
        # Borrar área seleccionada
        if bounds:
            x, y, w, h = bounds
            ctx = cairo.Context(target_surface)
            ctx.set_operator(cairo.OPERATOR_CLEAR)
            ctx.rectangle(x, y, w, h)
            ctx.fill()
    
    def paste(self, canvas):
        """Lee del portapapeles del sistema y pega en el canvas."""
        # Primero intentar del portapapeles del sistema
        texture = self.clipboard.read_texture_finish(None)
        if texture:
            # Convertir Gdk.Texture a cairo.ImageSurface
            width = texture.get_width()
            height = texture.get_height()
            surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
            # TODO: convertir texture bytes a surface
            return surface, (0, 0, width, height)
        
        # Fallback al almacenamiento interno
        return self.stored_surface, self.stored_bounds

    def paste_async(self, canvas, callback):
        """Lee del portapapeles de forma asincrona."""
        def on_texture_ready(clipboard, result):
            try:
                texture = clipboard.read_texture_finish(result)
                if texture:
                    # Convertir texture a surface
                    width = texture.get_width()
                    height = texture.get_height()
                    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
                    # Guardar y notificar
                    self.stored_surface = surface
                    self.stored_bounds = (0, 0, width, height)
                    callback(surface, self.stored_bounds)
                else:
                    callback(None, None)
            except Exception as e:
                print(f"Error al pegar: {e}")
                callback(None, None)
        
        self.clipboard.read_texture_async(None, on_texture_ready)    
        
    def has_content(self):
        """Verifica si hay contenido en el portapapeles."""
        return self.stored_surface is not None
