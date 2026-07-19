"""Barra de menús - Menús Archivo, Editar, Ver, Imagen, Ayuda"""
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio, GObject


class MenuBar(Gtk.Box):
    """Barra de menús estilo Paint."""
    
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL)
        
        menu_model = Gio.Menu()
        
        # Menú Archivo
        file_menu = Gio.Menu()
        file_menu.append("Nuevo", "win.new")
        file_menu.append("Abrir...", "win.open")
        file_menu.append("Guardar", "win.save")
        file_menu.append("Guardar como...", "win.save-as")
        file_menu.append("Propiedades...", "win.properties")
        file_menu.append("Salir", "win.quit")
        menu_model.append_submenu("Archivo", file_menu)
        
        # Menú Editar
        edit_menu = Gio.Menu()
        edit_menu.append("Deshacer", "win.undo")
        edit_menu.append("Rehacer", "win.redo")
        edit_menu.append("Cortar", "win.cut")
        edit_menu.append("Copiar", "win.copy")
        edit_menu.append("Pegar", "win.paste")
        edit_menu.append("Seleccionar todo", "win.select-all")
        edit_menu.append("Borrar selección", "win.delete")
        menu_model.append_submenu("Editar", edit_menu)
        
        # Menú Ver
        view_menu = Gio.Menu()
        view_menu.append("Zoom in", "win.zoom-in")
        view_menu.append("Zoom out", "win.zoom-out")
        view_menu.append("Zoom 100%", "win.zoom-reset")
        view_menu.append("Barra de estado", "win.toggle-statusbar")
        menu_model.append_submenu("Ver", view_menu)
        
        # Menú Imagen
        image_menu = Gio.Menu()
        image_menu.append("Voltear horizontal", "win.flip-h")
        image_menu.append("Voltear vertical", "win.flip-v")
        image_menu.append("Rotar 90°", "win.rotate-90")
        image_menu.append("Rotar 180°", "win.rotate-180")
        image_menu.append("Rotar 270°", "win.rotate-270")
        image_menu.append("Atributos...", "win.attributes")
        menu_model.append_submenu("Imagen", image_menu)
        
        # Menú Colores
        colors_menu = Gio.Menu()
        colors_menu.append("Editar colores...", "win.edit-colors")
        menu_model.append_submenu("Colores", colors_menu)
        
        # Menú Ayuda
        help_menu = Gio.Menu()
        help_menu.append("Temas de ayuda", "win.help")
        help_menu.append("Acerca de", "win.about")
        menu_model.append_submenu("Ayuda", help_menu)
        
        menubar = Gtk.PopoverMenuBar.new_from_model(menu_model)
        self.append(menubar)
