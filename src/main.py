#!/usr/bin/env python3
"""
WinPaint Linux - Punto de entrada principal
"""
import sys
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")

from gi.repository import Gtk, Gdk, Gio

from src.ui.main_window import MainWindow


class WinPaintApp(Gtk.Application):
    """Aplicación principal de WinPaint."""

    def __init__(self):
        super().__init__(
            application_id="com.github.winpaint.linux",
            flags=Gio.ApplicationFlags.HANDLES_OPEN
        )
        self.window = None

    def do_activate(self):
        """Se llama cuando la aplicación se activa."""
        if not self.window:
            self.window = MainWindow(application=self)
        self.window.present()

    def do_open(self, files, n_files, hint):
        """Abrir archivos desde línea de comandos o DnD."""
        self.do_activate()
        if n_files > 0 and self.window:
            self.window.open_file(files[0].get_path())


def main():
    """Función principal de entrada."""
    app = WinPaintApp()
    return app.run(sys.argv)


if __name__ == "__main__":
    sys.exit(main())
