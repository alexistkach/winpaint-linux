"""Herramienta Relleno (Bucket Fill)"""
import cairo
from collections import deque
from src.canvas.tools.base_tool import BaseTool


class FillTool(BaseTool):
    """Herramienta relleno - rellena areas de color similar."""
    
    def __init__(self):
        super().__init__("Relleno", "tool-fill")
        self.tolerance = 32
    
    def on_press(self, canvas, x, y, button=1):
        x = int(x)
        y = int(y)
        
        if x < 0 or x >= canvas.image.width or y < 0 or y >= canvas.image.height:
            return
        
        color = self._get_color_for_button(button)
        
        target_color = canvas.image.get_pixel_color(x, y)
        
        fill_rgba = (int(color[0] * 255), int(color[1] * 255), int(color[2] * 255), 255)
        target_rgba = (
            int(target_color[0] * 255),
            int(target_color[1] * 255),
            int(target_color[2] * 255),
            int(target_color[3] * 255) if len(target_color) > 3 else 255
        )
        
        if fill_rgba == target_rgba:
            return
        
        self._flood_fill(canvas, x, y, target_rgba, fill_rgba)
        canvas.commit_drawing()
    
    def on_motion(self, canvas, x, y):
        pass
    
    def on_release(self, canvas, x, y):
        pass
    
    def _flood_fill(self, canvas, start_x, start_y, target_color, fill_color):
        """Algoritmo flood fill con tolerancia - FIX: flush antes de modificar buffer."""
        surface = canvas.image.surface
        width = canvas.image.width
        height = canvas.image.height
        
        # FIX: Hacer flush de Cairo antes de modificar el buffer directamente
        # Esto libera cualquier snapshot que Cairo tenga del surface
        surface.flush()
        
        stride = surface.get_stride()
        data = surface.get_data()
        
        queue = deque()
        queue.append((start_x, start_y))
        
        visited = set()
        visited.add((start_x, start_y))
        border = set()
        
        b, g, r, a = fill_color[2], fill_color[1], fill_color[0], fill_color[3]
        
        pixels_changed = 0
        max_pixels = width * height
        
        while queue and pixels_changed < max_pixels:
            cx, cy = queue.popleft()
            
            offset = cy * stride + cx * 4
            data[offset] = b
            data[offset + 1] = g
            data[offset + 2] = r
            data[offset + 3] = a
            pixels_changed += 1
            
            for nx, ny in [(cx-1, cy), (cx+1, cy), (cx, cy-1), (cx, cy+1)]:
                if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in visited:
                    noffset = ny * stride + nx * 4
                    nb, ng, nr, na = data[noffset], data[noffset+1], data[noffset+2], data[noffset+3]
                    
                    if self._color_matches((nr, ng, nb, na), target_color):
                        visited.add((nx, ny))
                        queue.append((nx, ny))
                    else:
                        border.add((nx, ny))
        
        # Segunda pasada: cierra el halo antialiased (1-2 px) del borde con
        # tolerancia mayor pero alcance acotado, para no "fugarse" del borde.
        fringe_tolerance = min(self.tolerance * 5, 200)
        for _ in range(2):
            next_border = set()
            for nx, ny in border:
                if (nx, ny) in visited:
                    continue
                noffset = ny * stride + nx * 4
                nb, ng, nr, na = data[noffset], data[noffset+1], data[noffset+2], data[noffset+3]
                if self._color_matches((nr, ng, nb, na), target_color, fringe_tolerance):
                    data[noffset] = b
                    data[noffset + 1] = g
                    data[noffset + 2] = r
                    data[noffset + 3] = a
                    visited.add((nx, ny))
                    for mx, my in [(nx-1, ny), (nx+1, ny), (nx, ny-1), (nx, ny+1)]:
                        if 0 <= mx < width and 0 <= my < height and (mx, my) not in visited:
                            next_border.add((mx, my))
            border = next_border
        
        # FIX: Marcar dirty DESPUES de modificar todo el buffer
        surface.mark_dirty()
        canvas.queue_draw()
    
    def _color_matches(self, color1, color2, tolerance=None):
        """Verifica si dos colores estan dentro de la tolerancia."""
        tol = self.tolerance if tolerance is None else tolerance
        for c1, c2 in zip(color1[:3], color2[:3]):
            if abs(c1 - c2) > tol:
                return False
        return True
