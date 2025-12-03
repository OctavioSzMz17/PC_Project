import threading
import time
import random
from queue import Queue
import tkinter as tk
from tkinter import scrolledtext, ttk
from typing import Dict, List, Any

# --- Configuraciones Globales ---
TAMANIO_BUFFER = 5
cinta_transportadora = Queue(TAMANIO_BUFFER)
NUMERO_DE_PIEZAS = 10  # Piezas por cada productor
NUM_PRODUCTORES = 4
NUM_CONSUMIDORES = 4

# Diccionario global para el conteo de piezas empacadas
piezas_empacadas: Dict[str, int] = {}
# Lock para proteger el acceso al diccionario de conteo
piezas_empacadas_lock = threading.Lock()
# Evento para manejar la señal de terminación de la simulación
simulacion_terminada = threading.Event()

# --- Clases de Hilos (Refactorizadas para la GUI) ---

class Productor(threading.Thread):
    """Simula una máquina que ensambla y coloca piezas."""
    def __init__(self, nombre: str, gui_handler: 'GUIHandler'):
        super().__init__()
        self.nombre = nombre
        self.gui_handler = gui_handler
        self.piezas_producidas = 0

    def run(self):
        for i in range(NUMERO_DE_PIEZAS):
            # 1. Generar la pieza
            pieza = f"Pza-{self.nombre.split('-')[1]}-{i+1}"
            
            # 2. Bloquear hasta que haya espacio en la cola (put)
            cinta_transportadora.put(pieza) 
            self.piezas_producidas += 1
            
            # 3. Log y pausa
            self.gui_handler.log(f"{self.nombre} ensambló y colocó: **{pieza}** (Buffer: {cinta_transportadora.qsize()}/{TAMANIO_BUFFER})")
            time.sleep(random.uniform(0.5, 2))

        # 4. Señal de finalización (Solo un productor es responsable de enviar los None)
        # Por simplicidad, solo el último productor iniciado enviará las señales de terminación.
        if int(self.nombre.split('-')[1]) == NUM_PRODUCTORES:
             self.gui_handler.log("**Producción total finalizada.** Enviando señales de parada a Consumidores...")
             for _ in range(NUM_CONSUMIDORES):
                cinta_transportadora.put(None)
                
        self.gui_handler.update_status(f"Máquina {self.nombre} terminó. Total: {self.piezas_producidas}")


class Consumidor(threading.Thread):
    """Simula un empleado que recoge, empaca y cuenta piezas."""
    def __init__(self, nombre: str, gui_handler: 'GUIHandler'):
        super().__init__()
        self.nombre = nombre
        self.gui_handler = gui_handler
        
        # Inicializar conteo seguro
        with piezas_empacadas_lock:
            piezas_empacadas[self.nombre] = 0

    def run(self):
        while True:
            # 1. Esperar por la pieza (get)
            pieza = cinta_transportadora.get()

            # 2. Revisar señal de terminación
            if pieza is None:
                # Re-colocar None para el siguiente consumidor
                cinta_transportadora.task_done()
                
                # Usamos `put(None)` para que los otros consumidores
                # puedan recibir la señal de parada.
                # Nota: Una forma más robusta es usar un evento,
                # pero mantendremos tu estructura original.
                cinta_transportadora.put(None) 
                
                self.gui_handler.log(f"{self.nombre} recibió señal de parada y termina.")
                break

            # 3. Procesamiento (Empaque)
            self.gui_handler.log(f"{self.nombre} empacó: **{pieza}** (Buffer: {cinta_transportadora.qsize()}/{TAMANIO_BUFFER})")
            time.sleep(random.uniform(1, 3))
            
            # 4. Actualizar conteo
            with piezas_empacadas_lock:
                piezas_empacadas[self.nombre] += 1
                
            # 5. Señalizar que la tarea está hecha
            cinta_transportadora.task_done()
            
        self.gui_handler.update_status(f"Empleado {self.nombre} terminó.")
        self.gui_handler.check_completion()


# --- Interfaz Gráfica (Tkinter) ---

class GUIHandler:
    """Maneja la interfaz de usuario de Tkinter, asegurando thread-safety."""
    def __init__(self, master: tk.Tk):
        self.master = master
        master.title("Simulación Productor-Consumidor (Fábrica)")
        master.geometry("900x650")

        self.threads: List[threading.Thread] = []
        
        self._setup_ui()

    def _setup_ui(self):
        """Configura los widgets de la interfaz."""
        main_frame = ttk.Frame(self.master, padding="10")
        main_frame.pack(fill="both", expand=True)

        # Marco de Log
        log_frame = ttk.LabelFrame(main_frame, text="Registro de Eventos (Cinta Transportadora)", padding="10")
        log_frame.pack(padx=5, pady=5, fill="both", expand=True)

        self.log_area = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, width=100, height=25, font=('Courier New', 9))
        self.log_area.pack(fill="both", expand=True)

        # Marco de Estado
        status_frame = ttk.LabelFrame(main_frame, text="Resumen y Conteo Final", padding="10")
        status_frame.pack(padx=5, pady=5, fill="x")

        self.status_label = ttk.Label(status_frame, text="Buffer: 0/5 | Simulación no iniciada", anchor="w")
        self.status_label.pack(fill="x", pady=5)
        
        self.result_label = ttk.Label(status_frame, text="Esperando finalización de la simulación...", anchor="w")
        self.result_label.pack(fill="x", pady=5)
        
        # Botón
        self.start_button = ttk.Button(main_frame, text="Iniciar Simulación", command=self.start_simulation)
        self.start_button.pack(pady=10)

    def log(self, message: str):
        """Añade un mensaje al log de forma segura para hilos."""
        # Usa master.after() para ejecutar la actualización en el hilo principal de Tkinter
        self.master.after(0, self._add_log, message)

    def _add_log(self, message: str):
        """Método interno para añadir el log y desplazarse al final."""
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.update_status()

    def update_status(self, custom_message: str = ""):
        """Actualiza la etiqueta de estado del buffer y los hilos activos."""
        total_producir = NUM_PRODUCTORES * NUMERO_DE_PIEZAS
        
        # Contar piezas empacadas de forma segura
        with piezas_empacadas_lock:
            total_empacado = sum(piezas_empacadas.values())
            
        buffer_info = f"Buffer: **{cinta_transportadora.qsize()}** / {TAMANIO_BUFFER} | Total a Producir: **{total_producir}** | Total Empacado: **{total_empacado}**"
        self.status_label.config(text=buffer_info)
        
        if custom_message:
             self.result_label.config(text=custom_message)

    def show_results(self):
        """Muestra los resultados finales de empaque."""
        with piezas_empacadas_lock:
            total_empacado = sum(piezas_empacadas.values())
            
            results = f"**Producción y empaque finalizados.**\nTotal de Piezas Empacadas: **{total_empacado}**\n\nConteo por Empleado:\n"
            
            for name, count in piezas_empacadas.items():
                results += f"  - {name}: **{count}** piezas\n"

        self.result_label.config(text=results)
        self.log_area.insert(tk.END, "\n" + "="*50 + "\n" + "PRODUCCIÓN FINALIZADA" + "\n" + "="*50 + "\n")
        self.log_area.see(tk.END)

        # Deshabilitar botón de inicio
        self.start_button.config(text="Simulación Terminada", state=tk.DISABLED)

        # 🔹Botón para Cerrar la Aplicación
        ttk.Button(self.master, text="Cerrar", command=self.master.destroy).pack(pady=10)


    def start_simulation(self):
        """Inicia los hilos productores y consumidores."""
        self.start_button.config(state=tk.DISABLED, text="Simulación en Curso...")
        self.log_area.delete(1.0, tk.END)
        self.log("▶️ **Iniciando Simulación**...")

        # Iniciar Hilos Productores (Máquinas)
        productores = [Productor(f"Máquina-{i + 1}", self) for i in range(NUM_PRODUCTORES)]
        
        # Iniciar Hilos Consumidores (Empleados)
        consumidores = [Consumidor(f"Empleado-{i + 1}", self) for i in range(NUM_CONSUMIDORES)]

        self.threads = productores + consumidores
        
        for t in self.threads:
            t.start()
            
        # Monitorear la finalización (necesario ya que `join()` bloquearía la GUI)
        self.master.after(100, self.check_completion)
        
    def check_completion(self):
        """Verifica periódicamente si todos los hilos han terminado."""
        # Se verifica si algún hilo de Consumidor sigue activo. 
        # Los Productores terminarán primero.
        if any(isinstance(t, Consumidor) and t.is_alive() for t in self.threads):
            # Programar la próxima verificación
            self.master.after(500, self.check_completion)
        else:
            # Todos los consumidores han terminado
            self.show_results()


# --- Función Principal ---

def main():
    root = tk.Tk()
    gui_handler = GUIHandler(root)
    root.mainloop()


if __name__ == "__main__":
    main()