import subprocess
import sys
import os
import time
from tkinter import messagebox

class Executer:
    @staticmethod
    def lanzar_simple(ruta_archivo):
        """
        Ejecuta un archivo único (.py o .pdf).
        Abre una consola nueva para scripts de Python para ver prints.
        """
        if not os.path.exists(ruta_archivo):
            messagebox.showerror("Error", f"No se encuentra el archivo:\n{ruta_archivo}")
            return

        try:
            # Si es PDF
            if ruta_archivo.lower().endswith('.pdf'):
                if sys.platform == "win32":
                    os.startfile(ruta_archivo)
                else:
                    subprocess.Popen(['open', ruta_archivo])
            # Si es Python
            else:
                # creationflags=subprocess.CREATE_NEW_CONSOLE abre una ventana negra separada en Windows
                if sys.platform == "win32":
                    subprocess.Popen([sys.executable, ruta_archivo], creationflags=subprocess.CREATE_NEW_CONSOLE)
                else:
                    subprocess.Popen([sys.executable, ruta_archivo])
                    
        except Exception as e:
            messagebox.showerror("Error de Ejecución", f"Falló al abrir: {ruta_archivo}\n{e}")

    @staticmethod
    def lanzar_dual(ruta_carpeta, archivo_servidor, archivo_cliente):
        """
        Ejecuta Servidor y Cliente en consolas separadas con delay.
        ruta_carpeta: Ruta absoluta a la carpeta que contiene los scripts.
        """
        path_servidor = os.path.join(ruta_carpeta, archivo_servidor)
        path_cliente = os.path.join(ruta_carpeta, archivo_cliente)

        # Validaciones
        if not os.path.exists(path_servidor):
            messagebox.showerror("Error", f"No se encuentra el SERVIDOR:\n{path_servidor}")
            return
        if not os.path.exists(path_cliente):
            messagebox.showerror("Error", f"No se encuentra el CLIENTE:\n{path_cliente}")
            return

        try:
            # 1. Servidor (Consola Nueva)
            if sys.platform == "win32":
                subprocess.Popen([sys.executable, path_servidor], creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                subprocess.Popen([sys.executable, path_servidor])

            # 2. Espera de seguridad (para que el server arranque)
            time.sleep(1.5) 

            # 3. Cliente (Consola Nueva)
            if sys.platform == "win32":
                subprocess.Popen([sys.executable, path_cliente], creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                subprocess.Popen([sys.executable, path_cliente])
                
        except Exception as e:
            messagebox.showerror("Error Dual", f"Falló la ejecución concurrente:\n{e}")