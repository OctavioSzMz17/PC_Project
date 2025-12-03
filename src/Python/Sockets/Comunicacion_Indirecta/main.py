import threading
import time
import random
import tkinter as tk
from tkinter import scrolledtext

buffer = []
BUFFER_SIZE = 5

empty = threading.Semaphore(BUFFER_SIZE)
full = threading.Semaphore(0)
mutex = threading.Semaphore(1)

def log(msg):
    salida.insert(tk.END, msg + "\n")
    salida.see(tk.END)

def productor():
    for i in range(10):
        item = random.randint(1, 100)

        empty.acquire()
        mutex.acquire()

        buffer.append(item)
        log(f"Productor produjo: {item} | Buffer: {buffer}")

        mutex.release()
        full.release()

        time.sleep(0.5)

def consumidor():
    for i in range(10):

        full.acquire()
        mutex.acquire()

        item = buffer.pop(0)
        log(f"Consumidor consumió: {item} | Buffer: {buffer}")

        mutex.release()
        empty.release()

        time.sleep(1)

def iniciar_indirecta():
    t_prod = threading.Thread(target=productor)
    t_cons = threading.Thread(target=consumidor)

    t_prod.start()
    t_cons.start()

# ---------------------------
# Tkinter
# ---------------------------

ventana = tk.Tk()
ventana.title("Comunicación Indirecta con Semáforos")

btn_indirecta = tk.Button(ventana, text="Iniciar Comunicación Indirecta", command=iniciar_indirecta)
btn_indirecta.pack(pady=10)

salida = scrolledtext.ScrolledText(ventana, width=60, height=20)
salida.pack()

ventana.mainloop()

input("\n--- Ejecución finalizada. Presiona ENTER para cerrar ---")
