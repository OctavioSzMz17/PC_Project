# cliente.py

import socket
import time
import random

HOST = '127.0.0.1'  # Debe ser la misma IP del servidor
PORT = 65432        # Debe ser el mismo puerto del servidor

def realizar_compra():
    """
    Se conecta al servidor, recibe un "producto" y cierra la conexión.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((HOST, PORT))
            producto_recibido = client_socket.recv(1024).decode('utf-8')
            
            return True
        except ConnectionRefusedError:
            print(" El servidor no está disponible. Finalizando cliente...")
            return False
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
            return False

if __name__ == "__main__":
    print("Iniciando simulación de compras...")
    while True:
        if not realizar_compra():
            break  # Sale del bucle si el servidor ya no está disponible
        time.sleep(random.uniform(0.2, 1.0))  # Pausa aleatoria entre compras
    print("Cliente detenido.")
