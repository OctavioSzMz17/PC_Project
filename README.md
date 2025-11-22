# 🐯 Dashboard de Programación Concurrente (Proyecto Final)

Este repositorio contiene el código fuente del **Dashboard de Prácticas**, una interfaz gráfica desarrollada en Python (Tkinter) diseñada para centralizar y ejecutar de manera automatizada todas las prácticas de la materia de Programación Concurrente.

El sistema gestiona la ejecución de scripts simples y sistemas distribuidos (Cliente/Servidor) abriendo consolas independientes automáticamente.

## 📋 Tabla de Contenidos
1. [Instalación y Requisitos](#-instalación-y-requisitos)
2. [Cómo Descargar (Clone)](#-cómo-descargar-clone)
3. [Cómo Ejecutar](#-cómo-ejecutar)
4. [Manual de Integración (Para el Equipo)](#-manual-de-integración-para-el-equipo)
5. [Autores](#-autores)

---

## 🚀 Instalación y Requisitos

Para que el proyecto funcione en tu computadora (si vas a editar el código), necesitas tener instalado lo siguiente:

1. **Python 3.x** instalado y agregado al PATH.
2. **Librería Pillow** (para el manejo de imágenes).

Instala la librería ejecutando este comando en tu terminal:
```bash
pip install Pillow

-------------------------------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------------------------------


📥 Cómo Descargar (Clone)
Si eres miembro del equipo o el profesor, descarga el código con este comando:

git clone https://github.com/OctavioSzMz17/PC_Project.git
cd PC_Project




-------------------------------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------------------------------


▶️ Cómo Ejecutar
El punto de entrada de la aplicación es el archivo launcher.py (el Login).

Abre la terminal en la carpeta del proyecto.

Ejecuta:

Bash

python launcher.py
Ingresa las credenciales por defecto:

Usuario: tigres

Contraseña: 1234



-------------------------------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------------------------------




🛠 Manual de Integración (Para el Equipo)
Si necesitas agregar una nueva práctica (Sockets, Hilos, etc.) al menú, sigue estrictamente estos pasos para no romper el sistema.

Paso 1: Dónde guardar tus archivos
Todo el código fuente vive dentro de la carpeta src/Python. Nunca dejes archivos sueltos fuera de las categorías.

Entra a src/Python/{Categoría} (ej. Hilos, Sockets).

Si tu programa es 1 solo archivo: Pégalo directamente (ej. src/Python/Hilos/MiTarea.py).

Si es Cliente/Servidor: Crea una carpeta con el nombre de la práctica y mete dentro servidor.py y cliente.py.

Paso 2: Configurar el mainMenu.py
Abre mainMenu.py con tu editor de código (VS Code, etc.), busca el diccionario self.file_map (aprox. línea 100) y asigna tu archivo al botón correspondiente.

CASO A: Programa Simple (1 Archivo) Solo pon la ruta como texto (String).

Python

"Nombre del Botón": "Categoria/NombreArchivo.py"
CASO B: Programa Dual (Cliente/Servidor) Usa un diccionario para indicar la carpeta y los nombres de los scripts. El sistema abrirá dos consolas automáticamente.

Python

"Nombre del Botón": {
    "tipo": "dual",
    "carpeta": "Categoria/Nombre_De_Tu_Carpeta",
    "server": "servidor.py",
    "client": "cliente.py"
},
⚠️ REGLA DE ORO: Evitar cierre de ventana
Para que el profesor pueda ver los resultados en la consola negra antes de que se cierre automáticamente al terminar el proceso, agrega siempre esta línea al final de tus scripts (tanto en cliente como en servidor):

Python

input("\n--- Ejecución finalizada. Presiona ENTER para cerrar ---")




-------------------------------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------------------------------




👥 Autores
Hernández Alarcón Kimberly Anette

Carpio Callejas Diana Ximena

Hernández Cruz Julio Hazel

Jiménez Ángeles Victor Jesús

Calderón López Mario Daniel

Sanchez Mendoza Octavio











