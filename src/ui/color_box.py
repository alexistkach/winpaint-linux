"""
Selector de colores - replica la paleta clásica de Paint
"""
import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk, Gdk, GObject

from src.core.constants import CLASSIC_PALETTE


class ColorBox(Gtk.Box):
    """Widget de selección de colores estilo Paint."""

    __gsignals__ = {
        "primary-color-changed": (GObject.SIGNAL_RUN_FIRST, None, (object,)),
        "secondary-color-changed": (GObject.SIGNAL_RUN_FIRST, None, (object,)),
    }

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        self.set_margin_top(8)
        self.set_margin_bottom(8)
        self.set_margin_start(4)
        self.set_margin_end(4)

        self.primary_color = (0, 0, 0)
        self.secondary_color = (1, 1, 1)

        # Frame principal
        frame = Gtk.Frame()
        frame.set_label("Colores")

        container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        container.set_margin_top(8)
        container.set_margin_bottom(8)
        container.set_margin_start(8)
        container.set_margin_end(8)

        # Preview de colores activos
        preview_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        preview_box.set_halign(Gtk.Align.CENTER)

        # Color primario (frente)
        self.primary_btn = Gtk.DrawingArea()
        self.primary_btn.set_size_request(32, 32)
        self.primary_btn.set_draw_func(self._draw_primary_color, None)
        self.primary_btn.set_tooltip_text("Color primario (Click izquierdo)")

        # Color secundario (fondo)
        self.secondary_btn = Gtk.DrawingArea()
        self.secondary_btn.set_size_request(32, 32)
        self.secondary_btn.set_draw_func(self._draw_secondary_color, None)
        self.secondary_btn.set_tooltip_text("Color secundario (Click derecho)")

        preview_box.append(self.primary_btn)
        preview_box.append(self.secondary_btn)

        container.append(preview_box)

        # Separador
        container.append(Gtk.Separator())

        # Paleta de colores (grid 2x14)
        palette_grid = Gtk.Grid()
        palette_grid.set_row_spacing(2)
        palette_grid.set_column_spacing(2)

        self.color_buttons = []

        for i, color in enumerate(CLASSIC_PALETTE):
            btn = Gtk.DrawingArea()
            btn.set_size_request(16, 16)
            btn.set_draw_func(self._draw_palette_color, color)

            # Click controller
            click = Gtk.GestureClick.new()
            click.set_button(0)
            click.connect("pressed", self._on_color_clicked, color)
            btn.add_controller(click)

            row = i // 2
            col = i % 2
            palette_grid.attach(btn, col, row, 1, 1)
            self.color_buttons.append(btn)

        container.append(palette_grid)

        # Botón editar colores
        edit_btn = Gtk.Button(label="Editar colores...")
        edit_btn.connect("clicked", self._on_edit_colors)
        container.append(edit_btn)

        frame.set_child(container)
        self.append(frame)
        self.set_size_request(-1, 150)  # Alto maximo sugerido

    def _draw_primary_color(self, area, ctx, width, height, data):
        """Dibuja el preview del color primario."""
        ctx.set_source_rgb(*self.primary_color)
        ctx.rectangle(0, 0, width, height)
        ctx.fill()

        # Borde
        ctx.set_source_rgb(0.3, 0.3, 0.3)
        ctx.set_line_width(2)
        ctx.rectangle(0, 0, width, height)
        ctx.stroke()

    def _draw_secondary_color(self, area, ctx, width, height, data):
        """Dibuja el preview del color secundario."""
        ctx.set_source_rgb(*self.secondary_color)
        ctx.rectangle(0, 0, width, height)
        ctx.fill()

        # Borde
        ctx.set_source_rgb(0.3, 0.3, 0.3)
        ctx.set_line_width(2)
        ctx.rectangle(0, 0, width, height)
        ctx.stroke()

    def _draw_palette_color(self, area, ctx, width, height, color):
        """Dibuja un color de la paleta."""
        r, g, b = color[0] / 255.0, color[1] / 255.0, color[2] / 255.0
        ctx.set_source_rgb(r, g, b)
        ctx.rectangle(0, 0, width, height)
        ctx.fill()

        # Borde sutil
        ctx.set_source_rgb(0.5, 0.5, 0.5)
        ctx.set_line_width(0.5)
        ctx.rectangle(0, 0, width, height)
        ctx.stroke()

    def _on_color_clicked(self, gesture, n_press, x, y, color):
        """Maneja el click en un color de la paleta."""
        button = gesture.get_current_button()
        rgb = (color[0] / 255.0, color[1] / 255.0, color[2] / 255.0)

        if button == 1:  # Click izquierdo -> color primario
            self.primary_color = rgb
            self.primary_btn.queue_draw()
            self.emit("primary-color-changed", rgb)
        elif button == 3:  # Click derecho -> color secundario
            self.secondary_color = rgb
            self.secondary_btn.queue_draw()
            self.emit("secondary-color-changed", rgb)

    def _on_edit_colors(self, button):
        """Abre diálogo de edición de colores."""
        dialog = Gtk.ColorDialog()
        dialog.choose_rgba(
            parent=self.get_root(),
            initial_color=Gdk.RGBA(self.primary_color[0], self.primary_color[1], self.primary_color[2], 1),
            cancellable=None,
            callback=self._on_color_chosen
        )

    def _on_color_chosen(self, dialog, result):
        """Callback cuando se elige un color."""
        try:
            color = dialog.choose_rgba_finish(result)
            if color:
                rgb = (color.red, color.green, color.blue)
                self.primary_color = rgb
                self.primary_btn.queue_draw()
                self.emit("primary-color-changed", rgb)
        except Exception as e:
            pass  # Usuario canceló

    def get_primary_color(self):
        """Devuelve el color primario actual."""
        return self.primary_color

    def get_secondary_color(self):
        """Devuelve el color secundario actual."""
        return self.secondary_color
