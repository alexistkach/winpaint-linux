"""
Barra de estado - muestra coordenadas, dimensiones y zoom
"""
import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk, GObject


class StatusBar(Gtk.Box):
    """Barra de estado estilo Paint."""

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.set_margin_top(4)
        self.set_margin_bottom(4)
        self.set_margin_start(8)
        self.set_margin_end(8)

        # Coordenadas del cursor
        self.coords_label = Gtk.Label(label="0, 0 px")
        self.coords_label.set_width_chars(15)
        self.append(self.coords_label)

        # Separador
        self.append(Gtk.Separator(orientation=Gtk.Orientation.VERTICAL))

        # Dimensiones de la imagen
        self.size_label = Gtk.Label(label="640 x 480 px")
        self.size_label.set_width_chars(18)
        self.append(self.size_label)

        # Separador
        self.append(Gtk.Separator(orientation=Gtk.Orientation.VERTICAL))

        # Zoom
        self.zoom_label = Gtk.Label(label="100%")
        self.zoom_label.set_width_chars(8)
        self.append(self.zoom_label)

        # Spacer
        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        self.append(spacer)

        # Estado modificado
        self.modified_label = Gtk.Label(label="")
        self.append(self.modified_label)

    def set_coordinates(self, text):
        """Actualiza las coordenadas mostradas."""
        self.coords_label.set_text(text)

    def set_image_size(self, width, height):
        """Actualiza las dimensiones de la imagen."""
        self.size_label.set_text(f"{width} x {height} px")

    def set_zoom(self, zoom):
        """Actualiza el porcentaje de zoom."""
        percentage = int(zoom * 100)
        self.zoom_label.set_text(f"{percentage}%")

    def set_modified(self, modified):
        """Muestra si la imagen ha sido modificada."""
        self.modified_label.set_text("* Modificado" if modified else "")
