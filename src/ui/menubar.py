"""
Barra de menús - Menús Archivo, Editar, Ver, Imagen, Ayuda
"""
import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk, Gio, GObject


class MenuBar(Gtk.Box):
    """Barra de menús estilo Paint."""

    __gsignals__ = {
        "menu-activate": (GObject.SIGNAL_RUN_FIRST, None, (str,)),
    }

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL)

        # Crear menú modelo
        menu_model = Gio.Menu()

        # Menú Archivo
        file_menu = Gio.Menu()
        file_menu.append("Nuevo", "app.new")
        file_menu.append("Abrir...", "app.open")
        file_menu.append("Guardar", "app.save")
        file_menu.append("Guardar como...", "app.save-as")
        file_menu.append("Propiedades...", "app.properties")
        file_menu.append("Salir", "app.quit")
        menu_model.append_submenu("Archivo", file_menu)

        # Menú Editar
        edit_menu = Gio.Menu()
        edit_menu.append("Deshacer", "app.undo")
        edit_menu.append("Rehacer", "app.redo")
        edit_menu.append("Cortar", "app.cut")
        edit_menu.append("Copiar", "app.copy")
        edit_menu.append("Pegar", "app.paste")
        edit_menu.append("Seleccionar todo", "app.select-all")
        edit_menu.append("Borrar selección", "app.delete")
        menu_model.append_submenu("Editar", edit_menu)

        # Menú Ver
        view_menu = Gio.Menu()
        view_menu.append("Zoom in", "app.zoom-in")
        view_menu.append("Zoom out", "app.zoom-out")
        view_menu.append("Zoom 100%", "app.zoom-reset")
        view_menu.append("Barra de estado", "app.toggle-statusbar")
        menu_model.append_submenu("Ver", view_menu)

        # Menú Imagen
        image_menu = Gio.Menu()
        image_menu.append("Voltear horizontal", "app.flip-h")
        image_menu.append("Voltear vertical", "app.flip-v")
        image_menu.append("Rotar 90°", "app.rotate-90")
        image_menu.append("Rotar 180°", "app.rotate-180")
        image_menu.append("Rotar 270°", "app.rotate-270")
        image_menu.append("Atributos...", "app.attributes")
        menu_model.append_submenu("Imagen", image_menu)

        # Menú Colores
        colors_menu = Gio.Menu()
        colors_menu.append("Editar colores...", "app.edit-colors")
        menu_model.append_submenu("Colores", colors_menu)

        # Menú Ayuda
        help_menu = Gio.Menu()
        help_menu.append("Temas de ayuda", "app.help")
        help_menu.append("Acerca de", "app.about")
        menu_model.append_submenu("Ayuda", help_menu)

        # Crear menubar
        menubar = Gtk.PopoverMenuBar.new_from_model(menu_model)
        self.append(menubar)
