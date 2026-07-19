# Subir a GitHub

## Método rápido (script automático)

```bash
cd ~/winpaint-linux
./push-to-github.sh
```

## Método manual

### 1. Crear repo en GitHub

Andá a https://github.com/new y creá un repo llamado `winpaint-linux`.

### 2. Subir desde terminal

```bash
cd ~/winpaint-linux

# Inicializar
git init
git branch -M main

# Configurar (si no lo hiciste antes)
git config user.name "TU_USUARIO"
git config user.email "tu@email.com"

# Agregar todo
git add .

# Commit
git commit -m "Initial commit - WinPaint Linux v0.1.0"

# Conectar con GitHub
git remote add origin https://github.com/TU_USUARIO/winpaint-linux.git

# Subir
git push -u origin main
```

### 3. Autenticación

GitHub ya no acepta contraseñas. Usá un **Personal Access Token**:

1. Andá a https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Marcá el scope `repo`
4. Generá y copiá el token
5. Cuando `git push` pida contraseña, pegá el token

---

## Después de subir

Cuando quieras seguir desarrollando y subir cambios:

```bash
cd ~/winpaint-linux

# Ver cambios
git status

# Agregar modificados
git add .

# Commit
git commit -m "Descripción de los cambios"

# Subir
git push
```
