import threading
import time
import tkinter as tk
from tkinter import scrolledtext

sema = threading.Semaphore(1)
contador = 0

def log(msg):
    salida.insert(tk.END, msg + "\n")
    salida.see(tk.END)

def incrementar(nombre):
    global contador

    log(f"{nombre} quiere acceder...")

    sema.acquire()
    log(f"{nombre} ENTRA a la sección crítica.")

    valor_actual = contador
    time.sleep(1)
    contador = valor_actual + 1

    log(f"{nombre} incrementó contador a {contador}")
    log(f"{nombre} SALE de la sección crítica.\n")

    sema.release()

def iniciar_directa():
    t1 = threading.Thread(target=incrementar, args=("Hilo 1",))
    t2 = threading.Thread(target=incrementar, args=("Hilo 2",))
    t3 = threading.Thread(target=incrementar, args=("Hilo 3",))

    t1.start()
    t2.start()
    t3.start()

# ---------------------------
# Tkinter
# ---------------------------

ventana = tk.Tk()
ventana.title("Comunicación Directa con Semáforos")

btn_directa = tk.Button(ventana, text="Iniciar Comunicación Directa", command=iniciar_directa)
btn_directa.pack(pady=10)

salida = scrolledtext.ScrolledText(ventana, width=60, height=20)
salida.pack()

ventana.mainloop()

input("\n--- Ejecución finalizada. Presiona ENTER para cerrar ---")
