"""Herramienta Texto"""
import cairo
from src.canvas.tools.base_tool import BaseTool

class TextTool(BaseTool):
    def __init__(self):
        super().__init__("Texto", "tool-text")
        self.font_family = "Sans"
        self.font_size = 12
        self.is_bold = False
        self.is_italic = False
        self.text = ""
        self.text_x = 0
        self.text_y = 0
        self.editing = False

    def on_press(self, canvas, x, y, button=1):
        self.text_x = x
        self.text_y = y
        self.editing = True
        self._show_text_dialog(canvas)

    def on_motion(self, canvas, x, y):
        pass

    def on_release(self, canvas, x, y):
        pass

    def _show_text_dialog(self, canvas):
        import gi
        gi.require_version("Gtk", "4.0")
        from gi.repository import Gtk

        dialog = Gtk.Dialog(title="Insertar texto", transient_for=canvas.get_root(), modal=True)
        dialog.add_button("Cancelar", Gtk.ResponseType.CANCEL)
        dialog.add_button("Aceptar", Gtk.ResponseType.OK)

        content = dialog.get_content_area()
        content.set_spacing(8)
        content.set_margin_top(12)
        content.set_margin_bottom(12)
        content.set_margin_start(12)
        content.set_margin_end(12)

        entry = Gtk.Entry()
        entry.set_text("Texto")
        entry.set_width_chars(30)
        content.append(entry)
        entry.grab_focus()

        def on_response(dialog, response):
            if response == Gtk.ResponseType.OK:
                text = entry.get_text()
                if text:
                    self.render_text(canvas, text)
            dialog.destroy()

        dialog.connect("response", on_response)
        dialog.present()

    def render_text(self, canvas, text):
        if not text:
            return
        ctx = canvas.image.context
        color = self._get_color_for_button(1)
        ctx.select_font_face(
            self.font_family,
            cairo.FONT_SLANT_ITALIC if self.is_italic else cairo.FONT_SLANT_NORMAL,
            cairo.FONT_WEIGHT_BOLD if self.is_bold else cairo.FONT_WEIGHT_NORMAL
        )
        ctx.set_font_size(self.font_size)
        self._apply_color(ctx, color)
        ctx.move_to(self.text_x, self.text_y + self.font_size)
        ctx.show_text(text)
        canvas.queue_draw()
        canvas.commit_drawing()
        self.editing = False
