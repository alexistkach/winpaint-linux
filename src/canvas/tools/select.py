"""Herramienta Selección"""
import cairo
from src.canvas.tools.base_tool import BaseTool


class SelectRectTool(BaseTool):
    """Herramienta selección rectangular."""
    
    def __init__(self):
        super().__init__("Selección", "tool-select")
        self.start_x = 0
        self.start_y = 0
        self.selection = None  # (x, y, w, h)
        self.has_selection = False
        self.marching_ants_offset = 0
        self.selection_surface = None  # Superficie de la selección extraída
        self.is_moving = False  # Nuevo: moviendo selección
        self.move_offset_x = 0
        self.move_offset_y = 0    
        
    def on_press(self, canvas, x, y, button=1):
        # Si hay selección y se hace click dentro, empezar a mover
        if self.has_selection and self._point_in_selection(x, y):
            self.is_moving = True
            self.move_offset_x = x - self.selection[0]
            self.move_offset_y = y - self.selection[1]
            return
        
        # Si hay selección y click fuera, limpiar
        if self.has_selection:
            self.clear_selection()
            canvas.queue_draw()
        
        # Nueva selección
        self.is_drawing = True
        self.start_x = x
        self.start_y = y
        canvas.image.clear_preview()
    
    def _point_in_selection(self, x, y):
        """Verifica si un punto está dentro de la selección."""
        if not self.selection:
            return False
        sx, sy, sw, sh = self.selection
        return sx <= x <= sx + sw and sy <= y <= sy + sh
    
    def on_motion(self, canvas, x, y):
        if self.is_moving and self.has_selection:
            new_x = x - self.move_offset_x
            new_y = y - self.move_offset_y
            w, h = self.selection[2], self.selection[3]
            self.selection = (new_x, new_y, w, h)
            
            canvas.image.clear_preview()
            if self.selection_surface:
                ctx = canvas.image.preview_context
                ctx.set_source_surface(self.selection_surface, new_x, new_y)
                ctx.paint()
            
            canvas.queue_draw()
            return
        
        if not self.is_drawing:
            return
        
        x1, y1 = int(min(self.start_x, x)), int(min(self.start_y, y))
        w, h = int(abs(x - self.start_x)), int(abs(y - self.start_y))
        
        ctx = canvas.image.preview_context
        canvas.image.clear_preview()
        
        ctx.set_source_rgb(0, 0, 0)
        ctx.set_line_width(1)
        ctx.set_dash([4, 4], self.marching_ants_offset)
        ctx.rectangle(x1, y1, w, h)
        ctx.stroke()
        ctx.set_dash([])
        
        ctx.set_source_rgba(0.2, 0.4, 0.8, 0.1)
        ctx.rectangle(x1, y1, w, h)
        ctx.fill()
        
        self.selection = (x1, y1, w, h)
        self.has_selection = w > 2 and h > 2
        
        canvas.queue_draw()
        
    def on_release(self, canvas, x, y):
        if self.is_moving:
            self.is_moving = False
            # Re-extraer la selección en la nueva posición? 
            # O dejarla como "flotante" hasta que se confirme?
            return
        
        self.is_drawing = False
        if self.has_selection and self.selection:
            self._extract_selection(canvas)
        canvas.image.clear_preview()
        canvas.queue_draw()
    
    def _extract_selection(self, canvas):
        """Extrae la imagen seleccionada del canvas."""
        if not self.selection:
            return
        
        x, y, w, h = self.selection
        x, y, w, h = int(x), int(y), int(w), int(h)
                
        if w <= 0 or h <= 0:
            return
        # Crear superficie con la selección
        self.selection_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        ctx = cairo.Context(self.selection_surface)
        ctx.set_source_surface(canvas.image.surface, -x, -y)
        ctx.paint()
    
    def clear_selection(self):
        """Limpia la selección actual."""
        self.selection = None
        self.has_selection = False
        self.selection_surface = None
    
    def get_selection_surface(self):
        """Devuelve la superficie de la selección."""
        return self.selection_surface
    
    def get_selection_bounds(self):
        """Devuelve los límites de la selección."""
        return self.selection
