"""
Gestor de historial para Undo/Redo
"""
import cairo
import io


class HistoryManager:
    """Gestiona el historial de cambios para deshacer/rehacer."""

    def __init__(self, max_history=50):
        self.max_history = max_history
        self.history = []
        self.current_index = -1
        self._is_undoing = False

    def push_state(self, surface):
        """Guarda el estado actual de la superficie."""
        if self._is_undoing:
            return

        # Serializar surface a PNG bytes
        buf = io.BytesIO()
        surface.write_to_png(buf)
        buf.seek(0)

        # Eliminar estados futuros si estamos en medio del historial
        if self.current_index < len(self.history) - 1:
            self.history = self.history[:self.current_index + 1]

        self.history.append(buf.getvalue())

        # Limitar historial
        if len(self.history) > self.max_history:
            self.history.pop(0)
        else:
            self.current_index += 1

    def undo(self, current_surface):
        """Deshace el último cambio."""
        if self.can_undo():
            self.current_index -= 1
            return self._restore_state(current_surface)
        return None

    def redo(self, current_surface):
        """Rehace el último cambio deshecho."""
        if self.can_redo():
            self.current_index += 1
            return self._restore_state(current_surface)
        return None

    def _restore_state(self, current_surface):
        """Restaura un estado desde el historial."""
        if self.current_index < 0 or self.current_index >= len(self.history):
            return None

        self._is_undoing = True

        try:
            buf = io.BytesIO(self.history[self.current_index])
            new_surface = cairo.ImageSurface.create_from_png(buf)

            # Copiar al surface actual
            ctx = cairo.Context(current_surface)
            ctx.set_source_surface(new_surface, 0, 0)
            ctx.paint()

            return new_surface
        finally:
            self._is_undoing = False

    def can_undo(self):
        """Verifica si se puede deshacer."""
        return self.current_index > 0

    def can_redo(self):
        """Verifica si se puede rehacer."""
        return self.current_index < len(self.history) - 1

    def clear(self):
        """Limpia todo el historial."""
        self.history = []
        self.current_index = -1
