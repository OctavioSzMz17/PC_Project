# servidor.py (Versión Final Corregida)

import socket
import threading
import random
from collections import Counter

# --- Configuración Inicial ---
HOST = '127.0.0.1'
PORT = 65432
productos_limpieza = [
    "Jabon", "Detergente", "Desinfectante", "Limpiador de Ventanas",
    "Limpiador de Pisos", "Esponja", "Trapeador", "Guantes", "Cepillo", "Escoba"
]

# --- Almacenamiento Concurrente de Compras ---
compras_totales = Counter()
compras_lock = threading.Lock()
shutdown_event = threading.Event()

# --- Función para manejar cada cliente (SIN CAMBIOS) ---
def manejar_cliente(conn, addr):
    print(f"Conexión establecida desde: {addr}")
    producto_comprado = random.choice(productos_limpieza)
    
    with compras_lock:
        compras_totales[producto_comprado] += 1
    
    print(f"Compra recibida para: Producto {producto_comprado}")
    
    try:
        conn.sendall(producto_comprado.encode('utf-8'))
    except socket.error as e:
        print(f"Error al enviar datos al cliente {addr}: {e}")
        
    conn.close()

# --- Bucle principal del servidor que acepta conexiones (SIN CAMBIOS) ---
def bucle_servidor(server_socket):
    while not shutdown_event.is_set():
        try:
            conn, addr = server_socket.accept()
            
            client_thread = threading.Thread(
                target=manejar_cliente,
                args=(conn, addr)
            )
            client_thread.start()
        except socket.timeout:
            continue
        except Exception:
            # Si el socket se cierra desde el hilo principal, accept() fallará.
            # No es un error, es nuestra señal para salir del bucle.
            if shutdown_event.is_set():
                break

# --- Función Principal (MODIFICADA PARA USAR TRY/FINALLY) ---
def iniciar_servidor():
    # Creamos el socket fuera de un bloque 'with'
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_thread = None # Inicializamos la variable del hilo

    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        server_socket.settimeout(1.0)
        
        print(f" Servidor iniciado en {HOST}:{PORT}. Esperando clientes...")
        
        # Iniciar el bucle del servidor en un hilo separado
        server_thread = threading.Thread(target=bucle_servidor, args=(server_socket,))
        server_thread.start()
        
        # El hilo principal espera el 'input()'
        input("Presiona ENTER para detener el servidor y ver los resultados...\n")
        
    except Exception as e:
        print(f"Ocurrió un error al iniciar el servidor: {e}")
    finally:
        # Este bloque se ejecuta siempre, ya sea que el 'try' termine
        # normalmente o por un error.
        print("Señal de cierre recibida. Deteniendo el servidor...")
        shutdown_event.set()
        
        # Cerramos el socket aquí. Esto interrumpirá la espera de server_socket.accept()
        # en el hilo del servidor, permitiendo que termine limpiamente.
        server_socket.close()

    # Esperamos a que el hilo del servidor realmente termine
    if server_thread:
        server_thread.join()

    # --- Presentación de Resultados (SIN CAMBIOS) ---
    print("\n--- Resultados de Limpieza Son: ---")
    if not compras_totales:
        print("No se realizó ninguna compra.")
    else:
        for producto, cantidad in compras_totales.most_common():
            print(f"{cantidad} compras de {producto}")
        
        producto_mas_comprado = compras_totales.most_common(1)[0]
        print("\n Producto más comprado ")
        print(f"'{producto_mas_comprado[0]}' con {producto_mas_comprado[1]} unidades.")

# --- Punto de Entrada del Programa (SIN CAMBIOS) ---
if __name__ == "__main__":
    iniciar_servidor()