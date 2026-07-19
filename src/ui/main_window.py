"""Ventana principal"""
import os
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk, Gio, GLib

from src.ui.toolbox import ToolBox
from src.ui.color_box import ColorBox
from src.ui.statusbar import StatusBar
from src.ui.menubar import MenuBar
from src.ui.resize_handle import ResizeHandle
from src.canvas.drawing_area import DrawingArea
from src.core.constants import APP_NAME, VERSION, DEFAULT_CANVAS_WIDTH, DEFAULT_CANVAS_HEIGHT

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_title(APP_NAME)
        self.set_default_size(800, 500)
        self.set_size_request(500, 300)  # Tamano minimo
        self._build_ui()
        self._setup_actions()
        self._setup_accelerators()
        self._connect_signals()

    def _build_ui(self):
        """Construye la interfaz de usuario."""
        # Contenedor principal vertical
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_child(main_box)
        
        # Menu
        self.menubar = MenuBar()
        main_box.append(self.menubar)
        
        # Area de trabajo horizontal
        work_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        work_box.set_vexpand(True)
        main_box.append(work_box)
        
        # Barra de herramientas (izquierda)
        # Barra de herramientas (izquierda) - con scroll si es muy alta
        left_scroll = Gtk.ScrolledWindow()
        left_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        left_scroll.set_size_request(120, 100)  # Ancho fijo, alto minimo pequeno
        
        left_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        left_box.set_margin_start(4)
        left_box.set_margin_top(4)
        left_box.set_margin_bottom(4)
        
        self.toolbox = ToolBox()
        left_box.append(self.toolbox)
        
        self.color_box = ColorBox()
        left_box.append(self.color_box)
        
        left_scroll.set_child(left_box)
        work_box.append(left_scroll)
        work_box.append(Gtk.Separator(orientation=Gtk.Orientation.VERTICAL))
        
        # === CANVAS CON FIXED PARA RESIZE HANDLE ===
        # Box que contiene el fixed (canvas + handle) con scroll
        canvas_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        canvas_outer.set_vexpand(True)
        canvas_outer.set_hexpand(True)
        
        # Scroll para cuando el canvas es mas grande que la ventana
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.set_vexpand(True)
        scroll.set_hexpand(True)
        
        # Fixed con tamano exacto del canvas
# Fixed con tamano exacto del canvas
        self.canvas_fixed = Gtk.Fixed()
        self.canvas_fixed.set_size_request(DEFAULT_CANVAS_WIDTH, DEFAULT_CANVAS_HEIGHT)
        
        # Canvas - tamano exacto igual al fixed
        self.drawing_area = DrawingArea()
        self.drawing_area.set_size_request(DEFAULT_CANVAS_WIDTH, DEFAULT_CANVAS_HEIGHT)
        self.canvas_fixed.put(self.drawing_area, 0, 0)
        
        # Resize handle en la esquina del canvas
# Resize handle FUERA del canvas, en la esquina inferior derecha
        self.resize_handle = ResizeHandle()
        self.resize_handle.set_canvas_size(DEFAULT_CANVAS_WIDTH, DEFAULT_CANVAS_HEIGHT)
        self.canvas_fixed.put(self.resize_handle, DEFAULT_CANVAS_WIDTH, DEFAULT_CANVAS_HEIGHT)
        
        scroll.set_child(self.canvas_fixed)
        canvas_outer.append(scroll)
        
        work_box.append(canvas_outer)
        work_box.append(Gtk.Separator(orientation=Gtk.Orientation.VERTICAL))
                
        # Barra de estado
        self.statusbar = StatusBar()
        main_box.append(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL))
        main_box.append(self.statusbar)
        
        self.statusbar.set_image_size(DEFAULT_CANVAS_WIDTH, DEFAULT_CANVAS_HEIGHT)

    def _update_resize_handle_position(self):
                    """Actualiza la posicion del resize handle."""
                    width, height = self.drawing_area.get_image_dimensions()
                    self.canvas_fixed.set_size_request(width, height)
                    self.drawing_area.set_size_request(width, height)
                    # Handle FUERA del canvas (8x8px, mitad adentro mitad afuera visualmente)
                    self.canvas_fixed.move(self.resize_handle, width - 4, height - 4)        
        
    def _setup_actions(self):
        actions = [
            ("new", self._on_new), ("open", self._on_open), ("save", self._on_save),
            ("save-as", self._on_save_as), ("properties", self._on_properties),
            ("quit", self._on_quit), ("undo", self._on_undo), ("redo", self._on_redo),
            ("cut", self._on_cut), ("copy", self._on_copy), ("paste", self._on_paste),
            ("delete", self._on_delete), ("zoom-in", self._on_zoom_in),
            ("zoom-out", self._on_zoom_out), ("zoom-reset", self._on_zoom_reset),
            ("about", self._on_about),
        ]
        for name, callback in actions:
            action = Gio.SimpleAction.new(name, None)
            action.connect("activate", callback)
            self.add_action(action)

    def _setup_accelerators(self):
        app = self.get_application()
        accelerators = [
            ("win.new", "<Ctrl>n"),
            ("win.open", "<Ctrl>o"),
            ("win.save", "<Ctrl>s"),
            ("win.quit", "<Ctrl>q"),
            ("win.undo", "<Ctrl>z"),
            ("win.redo", "<Ctrl>y"),
            ("win.cut", "<Ctrl>x"),
            ("win.copy", "<Ctrl>c"),
            ("win.paste", "<Ctrl>v"),
            ("win.delete", "Delete"),
            ("win.zoom-in", "<Ctrl>plus"),
            ("win.zoom-out", "<Ctrl>minus"),
            ("win.zoom-reset", "<Ctrl>0"),
        ]
        
        for action, accel in accelerators:
            app.set_accels_for_action(action, [accel])

    def _connect_signals(self):
        self.toolbox.connect("tool-selected", self._on_tool_selected)
        self.toolbox.connect("brush-size-changed", self._on_brush_size_changed)
        self.color_box.connect("primary-color-changed", self._on_primary_color_changed)
        self.color_box.connect("secondary-color-changed", self._on_secondary_color_changed)
        self.drawing_area.connect("coordinates-changed", self._on_coordinates_changed)
        self.drawing_area.connect("image-modified", self._on_image_modified)
        self.drawing_area.connect("resize-request", self._on_resize_request)
        self.resize_handle.connect("resize-request", self._on_handle_resize)

    def _on_tool_selected(self, toolbox, tool_name):
        self.drawing_area.set_tool(tool_name)

    def _on_brush_size_changed(self, toolbox, size):
        self.drawing_area.set_brush_size(size)

    def _on_primary_color_changed(self, color_box, color):
        self.drawing_area.set_primary_color(color)

    def _on_secondary_color_changed(self, color_box, color):
        self.drawing_area.set_secondary_color(color)

    def _on_coordinates_changed(self, canvas, coords):
        self.statusbar.set_coordinates(coords)

    def _on_image_modified(self, canvas, modified):
        self.statusbar.set_modified(modified)
        self.set_title(f"*{APP_NAME}" if modified else APP_NAME)

    def _on_resize_request(self, canvas, width, height):
        self.statusbar.set_image_size(width, height)
        self.resize_handle.set_canvas_size(width, height)
        self._update_resize_handle_position()

    def _on_handle_resize(self, handle, width, height):
        self.drawing_area.resize_image(width, height)
        self.statusbar.set_image_size(width, height)
        self._update_resize_handle_position()
        
    def _on_new(self, action, param):
        if self._check_save_changes():
            self._create_size_dialog().present()

    def _on_open(self, action, param):
        if self._check_save_changes():
            dialog = Gtk.FileDialog()
            dialog.set_title("Abrir imagen")
            filters = Gio.ListStore.new(Gtk.FileFilter)
            all_filter = Gtk.FileFilter()
            all_filter.set_name("Todos los archivos de imagen")
            all_filter.add_pattern("*.png")
            all_filter.add_pattern("*.jpg")
            all_filter.add_pattern("*.jpeg")
            all_filter.add_pattern("*.bmp")
            filters.append(all_filter)
            png_filter = Gtk.FileFilter()
            png_filter.set_name("PNG")
            png_filter.add_pattern("*.png")
            filters.append(png_filter)
            dialog.set_filters(filters)
            dialog.open(self, None, self._on_open_dialog_response)

    def _on_open_dialog_response(self, dialog, result):
        try:
            file = dialog.open_finish(result)
            if file:
                self.drawing_area.open_image(file.get_path())
                self.statusbar.set_image_size(*self.drawing_area.get_image_dimensions())
        except:
            pass

    def _on_save(self, action, param):
        if self.drawing_area.image.filename:
            self.drawing_area.save_image(self.drawing_area.image.filename)
        else:
            self._on_save_as(action, param)

    def _on_save_as(self, action, param):
        dialog = Gtk.FileDialog()
        dialog.set_title("Guardar imagen")
        filters = Gio.ListStore.new(Gtk.FileFilter)
        png_filter = Gtk.FileFilter()
        png_filter.set_name("PNG")
        png_filter.add_pattern("*.png")
        filters.append(png_filter)
        jpg_filter = Gtk.FileFilter()
        jpg_filter.set_name("JPEG")
        jpg_filter.add_pattern("*.jpg")
        filters.append(jpg_filter)
        bmp_filter = Gtk.FileFilter()
        bmp_filter.set_name("BMP")
        bmp_filter.add_pattern("*.bmp")
        filters.append(bmp_filter)
        dialog.set_filters(filters)
        dialog.save(self, None, self._on_save_dialog_response)

    def _on_save_dialog_response(self, dialog, result):
        try:
            file = dialog.save_finish(result)
            if file:
                path = file.get_path()
                if path.lower().endswith((".jpg", ".jpeg")):
                    fmt = "jpg"
                elif path.lower().endswith(".bmp"):
                    fmt = "bmp"
                else:
                    fmt = "png"
                self.drawing_area.save_image(path, fmt)
        except:
            pass

    def _on_properties(self, action, param):
        self._create_properties_dialog().present()

    def _on_quit(self, action, param):
        if self._check_save_changes():
            self.get_application().quit()

    def _on_undo(self, action, param):
        self.drawing_area.undo()

    def _on_redo(self, action, param):
        self.drawing_area.redo()

    def _on_cut(self, action, param):
        pass

    def _on_copy(self, action, param):
        pass

    def _on_paste(self, action, param):
        pass

    def _on_delete(self, action, param):
        pass

    def _on_zoom_in(self, action, param):
        self.drawing_area.zoom_in()
        self.statusbar.set_zoom(self.drawing_area.zoom)

    def _on_zoom_out(self, action, param):
        self.drawing_area.zoom_out()
        self.statusbar.set_zoom(self.drawing_area.zoom)

    def _on_zoom_reset(self, action, param):
        self.drawing_area.zoom_reset()
        self.statusbar.set_zoom(self.drawing_area.zoom)

    def _on_about(self, action, param):
        dialog = Gtk.AboutDialog()
        dialog.set_transient_for(self)
        dialog.set_modal(True)
        dialog.set_program_name(APP_NAME)
        dialog.set_version(VERSION)
        dialog.set_comments("Un clon fiel de Microsoft Paint para Linux")
        dialog.set_license_type(Gtk.License.MIT_X11)
        dialog.set_website("https://github.com/alexistkach/winpaint-linux")
        dialog.present()

    def _check_save_changes(self):
        if not self.drawing_area.is_modified():
            return True
        dialog = Gtk.MessageDialog(
            transient_for=self, modal=True, message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text="La imagen ha sido modificada. Desea guardar los cambios?"
        )
        dialog.add_button("Cancelar", Gtk.ResponseType.CANCEL)
        response = dialog.run()
        dialog.destroy()
        if response == Gtk.ResponseType.YES:
            self._on_save(None, None)
            return not self.drawing_area.is_modified()
        elif response == Gtk.ResponseType.NO:
            return True
        return False

    def _create_size_dialog(self):
        dialog = Gtk.Dialog(title="Nueva imagen", transient_for=self, modal=True)
        dialog.add_button("Cancelar", Gtk.ResponseType.CANCEL)
        dialog.add_button("Crear", Gtk.ResponseType.OK)
        box = dialog.get_content_area()
        box.set_spacing(8)
        box.set_margin_top(12)
        box.set_margin_bottom(12)
        box.set_margin_start(12)
        box.set_margin_end(12)
        width_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        width_box.append(Gtk.Label(label="Ancho:"))
        self.width_spin = Gtk.SpinButton.new_with_range(1, 10000, 1)
        self.width_spin.set_value(DEFAULT_CANVAS_WIDTH)
        width_box.append(self.width_spin)
        width_box.append(Gtk.Label(label="px"))
        box.append(width_box)
        height_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        height_box.append(Gtk.Label(label="Alto:"))
        self.height_spin = Gtk.SpinButton.new_with_range(1, 10000, 1)
        self.height_spin.set_value(DEFAULT_CANVAS_HEIGHT)
        height_box.append(self.height_spin)
        height_box.append(Gtk.Label(label="px"))
        box.append(height_box)
        dialog.connect("response", self._on_size_dialog_response)
        return dialog

    def _on_size_dialog_response(self, dialog, response):
        if response == Gtk.ResponseType.OK:
            width = int(self.width_spin.get_value())
            height = int(self.height_spin.get_value())
            self.drawing_area.new_image(width, height)
            self.statusbar.set_image_size(width, height)
            self.resize_handle.set_canvas_size(width, height)
        dialog.destroy()

    def _create_properties_dialog(self):
        width, height = self.drawing_area.get_image_dimensions()
        dialog = Gtk.MessageDialog(
            transient_for=self, modal=True, message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK, text="Propiedades de la imagen"
        )
        dialog.format_secondary_text(f"Dimensiones: {width} x {height} px\nFormato: PNG/ARGB32")
        return dialog

    def open_file(self, filepath):
        self.drawing_area.open_image(filepath)
        self.statusbar.set_image_size(*self.drawing_area.get_image_dimensions())
