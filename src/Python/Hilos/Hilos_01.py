import threading
from time import sleep
import random

# Sincronización de hilos en Python
# El hilo principal no espera por el resto de hilos.

def ejecutar():
    print(f'{threading.current_thread().name} inició')
    sleep(random.randint(1, 5))
    print(f'{threading.current_thread().name} terminó')

# --- Creación de los hilos ---
print()
hilo1 = threading.Thread(target=ejecutar, name='Hilo 1')
hilo2 = threading.Thread(target=ejecutar, name='Hilo 2')
hilo3 = threading.Thread(target=ejecutar, name='Hilo 3')
hilo4 = threading.Thread(target=ejecutar, name='Hilo 4')
hilo5 = threading.Thread(target=ejecutar, name='Hilo 5')

# --- Ejecución de los hilos ---
hilo1.start()
hilo2.start()
hilo3.start()
hilo4.start()
hilo5.start()

print()
print('El hilo principal no espera por el resto de hilos.')

input("\n--- Ejecución finalizada. Presiona ENTER para cerrar ---")
