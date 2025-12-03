import threading
from time import sleep
import random

# sincronizar hilos en Python
# El hilo principal sí espera por el resto de hilos

def ejecutar():
    print(f'Comienza {threading.current_thread().name}')
    sleep(random.random())  # esperamos un tiempo aleatorio entre 0 y 1 segundos
    print(f'Termina {threading.current_thread().name}')

# creamos los hilos
hilo1 = threading.Thread(target=ejecutar, name='Hilo 1')
hilo2 = threading.Thread(target=ejecutar, name='Hilo 2')
hilo3 = threading.Thread(target=ejecutar, name='Hilo 3')
hilo4 = threading.Thread(target=ejecutar, name='Hilo 4')
hilo5 = threading.Thread(target=ejecutar, name='Hilo 5')

# ejecutamos los hilos
hilo1.start()
hilo2.start()
hilo3.start()
hilo4.start()
hilo5.start()

# esperamos a que terminen los hilos
hilo1.join()
hilo2.join()
hilo3.join()
hilo4.join()
hilo5.join()

print('El hilo principal sí espera por el resto de hilos.')

input("\n--- Ejecución finalizada. Presiona ENTER para cerrar ---")
