"""
Funciones de utilidad
"""
import os


def get_file_extension(filepath):
    """Obtiene la extensión de un archivo."""
    return os.path.splitext(filepath)[1].lower()


def format_file_size(size_bytes):
    """Formatea tamaño de archivo en unidades legibles."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def clamp(value, min_val, max_val):
    """Restringe un valor a un rango."""
    return max(min_val, min(min(max_val, value), max_val))


def rgb_to_hex(r, g, b):
    """Convierte RGB a hexadecimal."""
    return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"


def hex_to_rgb(hex_color):
    """Convierte hexadecimal a RGB."""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))
