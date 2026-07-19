# 🎨 WinPaint Linux

Un clon fiel de **Microsoft Paint** para Linux, construido con **Python + GTK4 + Cairo**.

![Estado](https://img.shields.io/badge/estado-en%20desarrollo-yellow)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![GTK](https://img.shields.io/badge/GTK-4.0-green)
![Licencia](https://img.shields.io/badge/licencia-MIT-blue)

## 📋 Características

| Característica | Estado |
|----------------|--------|
| Lápiz y pincel | ✅ |
| Líneas, rectángulos, elipses | ✅ |
| Borrador | ✅ |
| Relleno (bucket fill) | ✅ |
| Texto en canvas | ✅ |
| Selección rectangular/libre | 🔄 |
| Deshacer/Rehacer | ✅ |
| Zoom | 🔄 |
| Abrir/Guardar (PNG, JPG, BMP) | ✅ |
| Portapapeles (copiar/pegar) | 🔄 |
| Paleta de colores clásica | ✅ |
| Atajos de teclado | ✅ |

## 🚀 Instalación

### Debian / Ubuntu

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/winpaint-linux.git
cd winpaint-linux

# 2. Instalar dependencias del sistema
sudo apt update
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 libcairo2-dev python3-pil

# 3. Crear entorno virtual (recomendado)
python3 -m venv venv
source venv/bin/activate

# 4. Instalar el proyecto
pip install -e .

# 5. Ejecutar
winpaint
```

### Fedora

```bash
sudo dnf install python3-gobject cairo-gobject-devel gtk4-devel python3-pillow
```

### Arch Linux

```bash
sudo pacman -S python-gobject gtk4 cairo python-pillow
```

## ⌨️ Atajos de Teclado

| Atajo | Acción |
|-------|--------|
| `Ctrl + N` | Nuevo |
| `Ctrl + O` | Abrir |
| `Ctrl + S` | Guardar |
| `Ctrl + Z` | Deshacer |
| `Ctrl + Y` | Rehacer |
| `Ctrl + C` | Copiar selección |
| `Ctrl + V` | Pegar |
| `Ctrl + X` | Cortar |
| `Ctrl + +` | Zoom in |
| `Ctrl + -` | Zoom out |
| `Ctrl + E` | Propiedades de imagen |
| `Delete` | Borrar selección |

## 🛠️ Arquitectura

```
src/
├── main.py              # Punto de entrada
├── ui/
│   ├── main_window.py   # Ventana principal
│   ├── toolbox.py       # Barra de herramientas
│   ├── color_box.py     # Selector de colores
│   ├── statusbar.py     # Barra de estado
│   └── menubar.py       # Menús
├── canvas/
│   ├── drawing_area.py  # Área de dibujo
│   ├── tools/           # Herramientas de dibujo
│   └── history.py       # Undo/Redo manager
├── core/
│   ├── image.py         # Modelo de imagen
│   ├── selection.py     # Lógica de selección
│   └── clipboard.py     # Portapapeles
└── utils/
    └── helpers.py       # Utilidades
```

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el repositorio
2. Crea una rama (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -am 'Agrega nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 🙏 Agradecimientos

- Inspirado en **Microsoft Paint** (Windows 7/10/11)
- Proyectos de referencia: [Pinta](https://github.com/PintaProject/Pinta), [Drawing](https://github.com/maoschanz/drawing), [JS Paint](https://github.com/1j01/jspaint)
