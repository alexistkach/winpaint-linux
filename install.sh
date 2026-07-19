#!/bin/bash
# install.sh - Script de instalacion para WinPaint Linux

set -e

echo "=========================================="
echo "  WinPaint Linux - Instalador"
echo "=========================================="

# Detectar distribucion
if [ -f /etc/debian_version ]; then
    DISTRO="debian"
elif [ -f /etc/fedora-release ]; then
    DISTRO="fedora"
elif [ -f /etc/arch-release ]; then
    DISTRO="arch"
else
    echo "⚠️ Distribucion no detectada. Intentando con Debian/Ubuntu..."
    DISTRO="debian"
fi

echo "📦 Distribucion detectada: $DISTRO"

# Instalar dependencias del sistema
case $DISTRO in
    debian|ubuntu)
        echo "🔧 Instalando dependencias del sistema (Debian/Ubuntu)..."
        sudo apt update
        sudo apt install -y \
            python3 \
            python3-pip \
            python3-venv \
            python3-gi \
            python3-gi-cairo \
            gir1.2-gtk-4.0 \
            libcairo2-dev \
            libgirepository1.0-dev \
            libgirepository-2.0-dev \
            python3-pil \
            pkg-config \
            meson \
            cmake
        ;;
    fedora)
        echo "🔧 Instalando dependencias del sistema (Fedora)..."
        sudo dnf install -y \
            python3 \
            python3-pip \
            python3-gobject \
            cairo-gobject-devel \
            gtk4-devel \
            python3-pillow \
            gobject-introspection-devel \
            pkg-config \
            meson \
            cmake
        ;;
    arch)
        echo "🔧 Instalando dependencias del sistema (Arch)..."
        sudo pacman -S --needed \
            python \
            python-pip \
            python-gobject \
            gtk4 \
            cairo \
            python-pillow \
            gobject-introspection \
            pkg-config \
            meson \
            cmake
        ;;
esac

# Verificar que python3-gi esta disponible
echo "🔍 Verificando PyGObject del sistema..."
python3 -c "import gi; print(f'✅ PyGObject {gi.__version__} disponible')" || {
    echo "❌ Error: PyGObject no esta disponible en el sistema."
    echo "   Por favor instala python3-gi manualmente."
    exit 1
}

# Crear entorno virtual CON ACCESO a paquetes del sistema
echo "🐍 Creando entorno virtual..."
python3 -m venv venv --system-site-packages
source venv/bin/activate

# Instalar dependencias de Python
echo "📥 Instalando dependencias de Python..."
pip install --upgrade pip
pip install Pillow

# Instalar el proyecto en modo editable
echo "🔨 Instalando WinPaint Linux..."
pip install -e . --no-build-isolation

echo ""
echo "=========================================="
echo "✅ Instalacion completada!"
echo "=========================================="
echo ""
echo "Para ejecutar:"
echo "  source venv/bin/activate"
echo "  winpaint"
echo ""
echo "O directamente:"
echo "  python -m src.main"
echo ""
