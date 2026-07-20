"""Herramienta Selección Libre (Lasso)"""
import cairo
from src.canvas.tools.base_tool import BaseTool


class SelectFreeTool(BaseTool):
    """Herramienta selección libre - selecciona área con trazo libre."""
    
    def __init__(self):
        super().__init__("Selección libre", "tool-select-free")
        self.points = []  # Lista de puntos del trazo
        self.selection = None  # Bounds de la selección
        self.has_selection = False
        self.marching_ants_offset = 0
        self.selection_surface = None
        self.is_moving = False
        self.move_offset_x = 0
        self.move_offset_y = 0
    
    def on_press(self, canvas, x, y, button=1):
        # Si hay selección y click dentro, empezar a mover
        if self.has_selection and self._point_in_selection(x, y):
            self.is_moving = True
            self.move_offset_x = x
            self.move_offset_y = y
            
            # BORRAR el área original del canvas (dejar blanco)
            if self.selection:
                sx, sy, sw, sh = self.selection
                ctx = canvas.image.context
                ctx.set_source_rgb(1, 1, 1)
                ctx.rectangle(sx, sy, sw, sh)
                ctx.fill()
                canvas.commit_drawing()
            
            return
        
        # Nueva selección libre
        self.is_drawing = True
        self.points = [(x, y)]
        canvas.image.clear_preview()
    
    def _point_in_selection(self, x, y):
        """Verifica si un punto está dentro de los bounds de la selección."""
        if not self.selection:
            return False
        sx, sy, sw, sh = self.selection
        return sx <= x <= sx + sw and sy <= y <= sy + sh
    
    def on_motion(self, canvas, x, y):
        if self.is_moving and self.has_selection:
            dx = x - self.move_offset_x
            dy = y - self.move_offset_y
            self.move_offset_x = x
            self.move_offset_y = y
            
            # Mover todos los puntos
            self.points = [(px + dx, py + dy) for px, py in self.points]
            
            # Mover bounds
            if self.selection:
                sx, sy, sw, sh = self.selection
                self.selection = (sx + dx, sy + dy, sw, sh)
            
            # Dibujar preview movido
            canvas.image.clear_preview()
            if self.selection_surface:
                ctx = canvas.image.preview_context
                ctx.set_source_surface(self.selection_surface, self.selection[0], self.selection[1])
                ctx.paint()
            
            canvas.queue_draw()
            return
        
        if not self.is_drawing:
            return
        
        self.points.append((x, y))
        
        # Dibujar trazo
        ctx = canvas.image.preview_context
        canvas.image.clear_preview()
        
        if len(self.points) > 1:
            ctx.set_source_rgb(0, 0, 0)
            ctx.set_line_width(1)
            ctx.set_dash([4, 4], self.marching_ants_offset)
            ctx.move_to(self.points[0][0], self.points[0][1])
            for px, py in self.points[1:]:
                ctx.line_to(px, py)
            ctx.stroke()
            ctx.set_dash([])
        
        # Calcular bounds
        if len(self.points) > 2:
            xs = [p[0] for p in self.points]
            ys = [p[1] for p in self.points]
            self.selection = (min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys))
            self.has_selection = True
        
        canvas.queue_draw()
    
    def on_release(self, canvas, x, y):
        if self.is_moving:
            self.is_moving = False
            
            # Pegar selección en nueva posición
            if self.selection_surface and self.selection:
                sx, sy, sw, sh = self.selection
                ctx = canvas.image.context
                ctx.set_source_surface(self.selection_surface, sx, sy)
                ctx.paint()
                canvas.commit_drawing()
            
            canvas.queue_draw()
            return
        
        # Terminar de dibujar selección libre
        self.is_drawing = False
        
        if len(self.points) > 2:
            # Cerrar el path
            self.points.append(self.points[0])
            
            # Extraer selección
            self._extract_selection(canvas)
        
        canvas.image.clear_preview()
        canvas.queue_draw()
    
    def _extract_selection(self, canvas):
        """Extrae la imagen seleccionada usando el path libre."""
        if not self.selection or len(self.points) < 3:
            return
        
        x, y, w, h = self.selection
        if w <= 0 or h <= 0:
            return
        
        self.selection_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(w), int(h))
        ctx = cairo.Context(self.selection_surface)
        ctx.set_source_surface(canvas.image.surface, -x, -y)
        
        # Clip por el path
        ctx.move_to(self.points[0][0] - x, self.points[0][1] - y)
        for px, py in self.points[1:]:
            ctx.line_to(px - x, py - y)
        ctx.close_path()
        ctx.clip()
        
        ctx.paint()
    
    def clear_selection(self):
        self.points = []
        self.selection = None
        self.has_selection = False
        self.selection_surface = None
        self.is_moving = False
    
    def get_selection_surface(self):
        return self.selection_surface
    
    def get_selection_bounds(self):
        return self.selection
