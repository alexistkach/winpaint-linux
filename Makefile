# Makefile para WinPaint Linux

.PHONY: install dev test clean run lint format install-deps

# Instalacion completa (dependencias + proyecto)
install: install-deps
	python3 -m venv venv --system-site-packages
	venv/bin/pip install --upgrade pip
	venv/bin/pip install Pillow
	venv/bin/pip install -e . --no-build-isolation

# Instalar solo dependencias del sistema
install-deps:
	@echo "Instalando dependencias del sistema..."
	@bash install.sh || true

# Ejecutar aplicacion
run:
	venv/bin/python -m src.main

# Tests
test:
	venv/bin/python -m pytest tests/ -v

# Linting
lint:
	venv/bin/flake8 src/ tests/

# Formateo
format:
	venv/bin/black src/ tests/

# Limpiar archivos generados
clean:
	rm -rf build/ dist/ *.egg-info __pycache__ .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Crear paquete
package:
	venv/bin/python -m build
