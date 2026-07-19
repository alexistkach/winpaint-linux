"""Barra de herramientas"""
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk, GObject

class ToolBox(Gtk.Box):
    __gsignals__ = {
        "tool-selected": (GObject.SIGNAL_RUN_FIRST, None, (str,)),
        "brush-size-changed": (GObject.SIGNAL_RUN_FIRST, None, (int,)),
    }

    TOOLS = [
        ("select_rect", "Seleccion rectangular", "edit-select-all", "🔲"),
        ("select_free", "Seleccion libre", "edit-select-none", "✂️"),
        ("text", "Texto", "insert-text", "📝"),
        ("pencil", "Lapiz", "document-edit", "✏️"),
        ("brush", "Pincel", "applications-graphics", "🖌️"),
        ("fill", "Relleno", "color-select", "🪣"),
        ("line", "Linea", "draw-line", "📏"),
        ("rectangle", "Rectangulo", "draw-rectangle", "⬜"),
        ("ellipse", "Elipse", "draw-ellipse", "⭕"),
        ("eraser", "Borrador", "edit-clear", "🧼"),
    ]

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        self.set_margin_top(8)
        self.set_margin_bottom(8)
        self.set_margin_start(4)
        self.set_margin_end(4)
        self.current_tool = "pencil"
        self.tool_buttons = {}

        frame = Gtk.Frame()
        frame.set_label("Herramientas")
        container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        container.set_margin_top(8)
        container.set_margin_bottom(8)
        container.set_margin_start(8)
        container.set_margin_end(8)

        tools_grid = Gtk.Grid()
        tools_grid.set_row_spacing(2)
        tools_grid.set_column_spacing(2)

        for i, (tool_id, tooltip, icon_name, emoji) in enumerate(self.TOOLS):
            btn = self._create_tool_button(tool_id, tooltip, icon_name, emoji)
            row = i // 2
            col = i % 2
            tools_grid.attach(btn, col, row, 1, 1)
            self.tool_buttons[tool_id] = btn

        container.append(tools_grid)
        container.append(Gtk.Separator())

        size_label = Gtk.Label(label="Tamano:")
        size_label.set_halign(Gtk.Align.START)
        container.append(size_label)

        self.size_spin = Gtk.SpinButton.new_with_range(1, 50, 1)
        self.size_spin.set_value(3)
        self.size_spin.connect("value-changed", self._on_size_changed)
        container.append(self.size_spin)

        self.size_scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 1, 50, 1)
        self.size_scale.set_value(3)
        self.size_scale.set_draw_value(True)
        self.size_scale.connect("value-changed", self._on_size_changed)
        container.append(self.size_scale)

        frame.set_child(container)
        self.append(frame)
        self._select_tool("pencil")
        self.set_size_request(-1, 200)  # Alto maximo sugerido
        
    def _create_tool_button(self, tool_id, tooltip, icon_name, emoji):
        btn = Gtk.ToggleButton()
        btn.set_size_request(40, 40)
        try:
            icon = Gtk.Image.new_from_icon_name(icon_name)
            icon.set_pixel_size(20)
            if icon.get_paintable() is None:
                raise ValueError("Icono no encontrado")
            btn.set_child(icon)
        except:
            label = Gtk.Label(label=emoji)
            label.set_markup(f"<span size='x-large'>{emoji}</span>")
            btn.set_child(label)
        btn.set_tooltip_text(tooltip)
        btn.connect("toggled", self._on_tool_toggled, tool_id)
        return btn

    def _on_tool_toggled(self, btn, tool_id):
        if btn.get_active():
            self._select_tool(tool_id)

    def _select_tool(self, tool_id):
        self.current_tool = tool_id
        for tid, btn in self.tool_buttons.items():
            btn.set_active(tid == tool_id)
        self.emit("tool-selected", tool_id)

    def _on_size_changed(self, widget):
        size = int(widget.get_value())
        if widget == self.size_spin:
            self.size_scale.set_value(size)
        else:
            self.size_spin.set_value(size)
        self.emit("brush-size-changed", size)

    def get_current_tool(self):
        return self.current_tool
