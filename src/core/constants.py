"""
Constantes globales del proyecto
"""

# Versión
VERSION = "0.1.0"
APP_NAME = "WinPaint Linux"
APP_ID = "com.github.winpaint.linux"

# Dimensiones por defecto
DEFAULT_WIDTH = 800
DEFAULT_HEIGHT = 600
DEFAULT_CANVAS_WIDTH = 640
DEFAULT_CANVAS_HEIGHT = 480

# Colores por defecto (Paint clásico)
DEFAULT_PRIMARY_COLOR = (0, 0, 0)       # Negro
DEFAULT_SECONDARY_COLOR = (255, 255, 255)  # Blanco

# Tamaños de herramientas
MIN_BRUSH_SIZE = 1
MAX_BRUSH_SIZE = 50
DEFAULT_BRUSH_SIZE = 3

# Zoom
MIN_ZOOM = 0.125
MAX_ZOOM = 8.0
ZOOM_STEP = 2.0

# Formatos soportados
SUPPORTED_OPEN_FORMATS = [
    ("PNG", ["*.png"]),
    ("JPEG", ["*.jpg", "*.jpeg"]),
    ("BMP", ["*.bmp"]),
    ("GIF", ["*.gif"]),
    ("TIFF", ["*.tiff", "*.tif"]),
    ("Todos los archivos de imagen", ["*.png", "*.jpg", "*.jpeg", "*.bmp", "*.gif", "*.tiff"]),
]

SUPPORTED_SAVE_FORMATS = [
    ("PNG", ["*.png"]),
    ("JPEG", ["*.jpg", "*.jpeg"]),
    ("BMP", ["*.bmp"]),
]

# Paleta de colores clásica de Paint (28 colores)
CLASSIC_PALETTE = [
    (0, 0, 0),         # Negro
    (128, 128, 128),   # Gris oscuro
    (128, 0, 0),       # Rojo oscuro
    (128, 128, 0),     # Amarillo oscuro
    (0, 128, 0),       # Verde oscuro
    (0, 128, 128),     # Cyan oscuro
    (0, 0, 128),       # Azul oscuro
    (128, 0, 128),     # Magenta oscuro
    (192, 192, 192),   # Gris claro
    (255, 255, 255),   # Blanco
    (255, 0, 0),       # Rojo
    (255, 255, 0),     # Amarillo
    (0, 255, 0),       # Verde
    (0, 255, 255),     # Cyan
    (0, 0, 255),       # Azul
    (255, 0, 255),     # Magenta
    (255, 128, 0),     # Naranja
    (255, 192, 128),   # Melocotón
    (128, 255, 0),     # Lima
    (128, 255, 128),   # Verde claro
    (0, 255, 128),     # Turquesa
    (128, 255, 255),   # Cyan claro
    (0, 128, 255),     # Azul cielo
    (128, 128, 255),   # Azul claro
    (128, 0, 255),     # Violeta
    (255, 128, 255),   # Rosa
    (255, 0, 128),     # Fucsia
    (255, 128, 128),   # Rosa claro
]

# Tipos de herramientas
class ToolType:
    PENCIL = "pencil"
    BRUSH = "brush"
    LINE = "line"
    RECTANGLE = "rectangle"
    ELLIPSE = "ellipse"
    ERASER = "eraser"
    FILL = "fill"
    TEXT = "text"
    SELECT_RECT = "select_rect"
    SELECT_FREE = "select_free"
