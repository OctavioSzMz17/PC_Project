import subprocess
import sys
import os
import time
from tkinter import messagebox

class Executer:
    @staticmethod
    def get_python_command():
        """
        Determina el intérprete de Python a utilizar.
        """
        if getattr(sys, 'frozen', False):
            # Modo ejecutable (.exe)
            return "python"
        else:
            # Modo script (.py)
            return sys.executable

    @staticmethod
    def _obtener_ruta_visor():
        """
        Busca el archivo visualPDF.py. 
        Asume que está en 'src/Python/visualPDF.py' relativo al ejecutable/script.
        """
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__)) # Carpeta donde está executer.py
        
        # Opción 1: Si executer.py está en la raíz junto a mainMenu
        # ruta_visor = os.path.join(base_dir, "src", "Python", "visualPDF.py")
        
        # Opción 2: Busqueda relativa si executer.py ya está dentro de alguna estructura
        # Para tu proyecto, asumiremos la estructura estándar:
        # raiz/
        #   mainMenu.py
        #   src/
        #     Python/
        #       visualPDF.py
        
        # Si estamos ejecutando desde mainMenu.py (raiz), la ruta a visualPDF debe construirse:
        # Intentamos localizarlo dinámicamente:
        posibles_rutas = [
            os.path.join(base_dir, "src", "Python", "visualPDF.py"), # Estructura ideal
            os.path.join(base_dir, "visualPDF.py"),                  # En la raiz
            "visualPDF.py"                                           # En path relativo simple
        ]

        for ruta in posibles_rutas:
            if os.path.exists(ruta):
                return ruta
        
        return None

    @staticmethod
    def lanzar_simple(ruta_archivo):
        if not os.path.exists(ruta_archivo):
            messagebox.showerror("Error 404", f"El archivo no existe:\n{ruta_archivo}")
            return

        python_cmd = Executer.get_python_command()

        try:
            # --- CASO 1: ARCHIVOS PDF (Usar nuestro visor personalizado) ---
            if ruta_archivo.lower().endswith('.pdf'):
                ruta_visor = Executer._obtener_ruta_visor()
                
                if ruta_visor and os.path.exists(ruta_visor):
                    # Lanzamos visualPDF.py pasándole la ruta del PDF como argumento
                    cmd = [python_cmd, ruta_visor, ruta_archivo]
                    
                    # No usamos CREATE_NEW_CONSOLE porque es una GUI (Tkinter)
                    subprocess.Popen(cmd)
                else:
                    # Fallback: Si no encuentra visualPDF.py, usa el del sistema
                    print("Advertencia: No se encontró visualPDF.py, usando visor del sistema.")
                    if sys.platform == "win32":
                        os.startfile(ruta_archivo)
                    else:
                        subprocess.Popen(['open', ruta_archivo])

            # --- CASO 2: SCRIPTS DE PYTHON ---
            else:
                cmd = [python_cmd, ruta_archivo]
                
                if sys.platform == "win32":
                    # Abrimos consola nueva para ver prints del script
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
            messagebox.showerror("Error", f"Falta archivo SERVIDOR en:\n{path_servidor}")
            return
        if not os.path.exists(path_cliente):
            messagebox.showerror("Error", f"Falta archivo CLIENTE en:\n{path_cliente}")
            return

        python_cmd = Executer.get_python_command()

        try:
            # 1. Servidor (Consola propia)
            cmd_server = [python_cmd, path_servidor]
            if sys.platform == "win32":
                subprocess.Popen(cmd_server, creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                subprocess.Popen(cmd_server)

            # 2. Pequeña pausa para asegurar que el servidor levante
            time.sleep(1.5) 

            # 3. Cliente (Consola propia)
            cmd_client = [python_cmd, path_cliente]
            if sys.platform == "win32":
                subprocess.Popen(cmd_client, creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                subprocess.Popen(cmd_client)
                
        except Exception as e:
            messagebox.showerror("Error Dual", f"Falló la ejecución concurrente:\n{e}")