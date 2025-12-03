import subprocess
import sys
import os
import time
from tkinter import messagebox

class Executer:
    @staticmethod
    def get_python_command():
        """
        Determina qué intérprete usar.
        - Si estamos en modo script, usa el mismo intérprete actual (sys.executable).
        - Si estamos en modo EXE (frozen), NO podemos usar sys.executable porque apuntaría
          al propio EXE. Usamos 'python' asumiendo que está en las variables de entorno,
          o una ruta específica si distribuyes una carpeta de python portable.
        """
        if getattr(sys, 'frozen', False):
            # ESTAMOS EN MODO EJECUTABLE (.exe)
            # Opción A: Asumir que el usuario tiene Python instalado en su PATH
            return "python"
            # Opción B (Avanzada): Si entregas una carpeta 'python_embed' junto a tu exe:
            # return os.path.join(os.path.dirname(sys.executable), "python_embed", "python.exe")
        else:
            # ESTAMOS EN MODO SCRIPT (.py)
            return sys.executable

    @staticmethod
    def lanzar_simple(ruta_archivo):
        if not os.path.exists(ruta_archivo):
            messagebox.showerror("Error", f"No se encuentra el archivo:\n{ruta_archivo}")
            return

        python_cmd = Executer.get_python_command()

        try:
            # Si es PDF
            if ruta_archivo.lower().endswith('.pdf'):
                if sys.platform == "win32":
                    os.startfile(ruta_archivo)
                else:
                    subprocess.Popen(['open', ruta_archivo])
            # Si es Python (.py)
            else:
                cmd = [python_cmd, ruta_archivo]
                
                if sys.platform == "win32":
                    subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
                else:
                    subprocess.Popen(cmd)
                    
        except Exception as e:
            messagebox.showerror("Error de Ejecución", f"Falló al abrir: {ruta_archivo}\n{e}")

    @staticmethod
    def lanzar_dual(ruta_carpeta, archivo_servidor, archivo_cliente):
        path_servidor = os.path.join(ruta_carpeta, archivo_servidor)
        path_cliente = os.path.join(ruta_carpeta, archivo_cliente)

        if not os.path.exists(path_servidor):
            messagebox.showerror("Error", f"No se encuentra SERVIDOR en:\n{path_servidor}")
            return
        if not os.path.exists(path_cliente):
            messagebox.showerror("Error", f"No se encuentra CLIENTE en:\n{path_cliente}")
            return

        python_cmd = Executer.get_python_command()

        try:
            # 1. Servidor
            cmd_server = [python_cmd, path_servidor]
            if sys.platform == "win32":
                subprocess.Popen(cmd_server, creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                subprocess.Popen(cmd_server)

            # 2. Espera
            time.sleep(1.5) 

            # 3. Cliente
            cmd_client = [python_cmd, path_cliente]
            if sys.platform == "win32":
                subprocess.Popen(cmd_client, creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                subprocess.Popen(cmd_client)
                
        except Exception as e:
            messagebox.showerror("Error Dual", f"Falló la ejecución concurrente:\n{e}")