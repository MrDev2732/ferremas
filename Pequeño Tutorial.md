# 🌐 Cómo Conectar al Repositorio
### Primero, iniciar git
```sh
git init
```
### Luego, desde el CMD, pegar el siguiente código
```sh
git clone https://github.com/MrDev2732/ferremas
```

# 🌟 Cómo Iniciar un Proyecto 🌟

## 🏗️ Genera un Monorepo
```sh
npx create-nx-workspace@latest
```

## 👀 Genera un Nuevo Proyecto (Frontend)
```sh
npx nx g @nx/angular:application "Nombre del frontend"
```

## 🚀 Genera un Nuevo Proyecto (Backend)
```sh
npx nx generate @nxlv/python:poetry-project "Nombre del proyecto | backend" \
--projectType application \
--description='My Project 1' \  # ACA VA UNA BREVE DESCRIPCIÓN DEL PROYECTO
--packageName="src o backend" \
--moduleName="src o backend"
```

## 📚 Genera una Nueva Librería para Utilizar de Forma Global entre los Proyectos
```sh
npx nx generate @nxlv/python:poetry-project "Nombre de la libreria" \
--projectType library \
--description='My Library 1' \  # ACA VA UNA BREVE DESCRIPCIÓN DE LA LIBRERIA
--packageName="src o backend" \
--moduleName="src o backend"
```

## 📚 Genera una nueva vista en un Frontend
```sh
npx nx generate @nrwl/angular:component "nombre de la vista" --project="nombre del frontend" --module=app.module.ts --style=scss 
```

## 🏃‍♂️ Cómo Correr los Servidores

### 🖥️ Backend
1. Usando NX:
    ```sh
    npx nx run backend-ferremas:serve
    ```
2. Usando Uvicorn con Poetry:
    ```sh
    poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000 --log-level info --reload
    # - Tienes que estar dentro de la carpeta
    # - Tienes que haber instalado previamente las dependencias
    #     poetry install
    ```
3. Usando Docker Compose:
    ```sh
    docker-compose up "carpeta" --build
    ```

### 🌐 Frontend
```sh
npx nx serve "frontend"
```

## 📦 Cómo Instalar Dependencias

### 📜 Si vas a utilizar `poetry`
Tienes que ir a la carpeta que quieras actualizar dependencias y ejecutar:
```sh
poetry add "dependencia"
```

### 📦 Si vas a utilizar `npx`
No es necesario estar dentro de la carpeta:
```sh
npx nx run "carpeta":add "dependencia"
```

---

### 📋 Notas Adicionales:

- **Poetry** es una herramienta para manejar dependencias en proyectos de Python. Es muy útil para mantener un entorno limpio y ordenado.
- **NX** es un conjunto de herramientas y extensiones para el monorepo que facilita la gestión de aplicaciones y bibliotecas.
- **Uvicorn** es un servidor ASGI para Python, utilizado comúnmente para correr aplicaciones web rápidas y asincrónicas.

🔧 ¡Asegúrate de tener todas las herramientas necesarias instaladas y configuradas antes de comenzar con tu proyecto!