# Guia de Instalacion

## ⚠️ Importante: PyGObject debe venir del sistema

PyGObject **no se puede instalar facilmente desde pip** porque requiere
compilar extensiones C que dependen de bibliotecas del sistema (GTK, GObject, Cairo).

Por eso, **instala PyGObject desde los repositorios de tu distribucion**
y luego instala el proyecto en un entorno virtual con acceso a los paquetes del sistema.

---

## Debian / Ubuntu (Recomendado)

### Metodo rapido (script automatico)

```bash
cd winpaint-linux
./install.sh
```

### Metodo manual paso a paso

```bash
# 1. Instalar dependencias del sistema
sudo apt update
sudo apt install -y \
    python3 python3-pip python3-venv \
    python3-gi python3-gi-cairo \
    gir1.2-gtk-4.0 \
    libcairo2-dev \
    libgirepository1.0-dev \
    libgirepository-2.0-dev \
    python3-pil \
    pkg-config meson cmake

# 2. Verificar que PyGObject del sistema funciona
python3 -c "import gi; print(gi.__version__)"

# 3. Crear entorno virtual CON ACCESO a paquetes del sistema
python3 -m venv venv --system-site-packages

# 4. Activar
source venv/bin/activate

# 5. Instalar solo Pillow (PyGObject ya esta disponible)
pip install Pillow

# 6. Instalar el proyecto
pip install -e . --no-build-isolation

# 7. Ejecutar
winpaint
```

---

## Fedora

```bash
sudo dnf install -y python3-gobject cairo-gobject-devel gtk4-devel \
    python3-pillow gobject-introspection-devel pkg-config meson cmake

python3 -m venv venv --system-site-packages
source venv/bin/activate
pip install Pillow
pip install -e . --no-build-isolation
winpaint
```

---

## Arch Linux

```bash
sudo pacman -S python-gobject gtk4 cairo python-pillow \
    gobject-introspection pkg-config meson cmake

python3 -m venv venv --system-site-packages
source venv/bin/activate
pip install Pillow
pip install -e . --no-build-isolation
winpaint
```

---

## 🔧 Solucion de problemas

### Error: `Dependency 'girepository-2.0' is required but not found`

```bash
# Debian/Ubuntu
sudo apt install libgirepository-2.0-dev

# Fedora
sudo dnf install gobject-introspection-devel

# Arch
sudo pacman -S gobject-introspection
```

### Error: `No module named 'gi'`

Asegurate de crear el venv con `--system-site-packages`:
```bash
python3 -m venv venv --system-site-packages
```

O instala PyGObject directamente en el sistema:
```bash
sudo apt install python3-gi python3-gi-cairo
```

### Error: `Namespace Gtk not available`

```bash
sudo apt install gir1.2-gtk-4.0
```

---

## 🖥️ Requisitos del sistema

| Requisito | Version minima |
|-----------|---------------|
| Python | 3.10+ |
| GTK | 4.0+ |
| GObject Introspection | 1.70+ |
| Cairo | 1.16+ |
| Debian/Ubuntu | 12 (Bookworm)+ |
| Fedora | 36+ |
| Arch Linux | Rolling (actualizado) |
