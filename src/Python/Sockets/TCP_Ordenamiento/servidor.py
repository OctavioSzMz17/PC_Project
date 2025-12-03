import socket
import threading
import time
import random
import json
import struct
import sys

# Ajuste necesario para QuickSort con 10,000 elementos
sys.setrecursionlimit(15000)

HOST = '127.0.0.1'
PORT = 65432
LIST_SIZE = 10000  # Cantidad solicitada

# --- Protocolo TCP: Envío y Recepción Segura ---
def send_msg(sock, msg_dict):
    """Empaqueta el JSON con un encabezado de 4 bytes indicando su tamaño."""
    msg_bytes = json.dumps(msg_dict).encode('utf-8')
    # Header: Longitud del mensaje (Big Endian Unsigned Int)
    header = struct.pack('>I', len(msg_bytes))
    sock.sendall(header + msg_bytes)

def recv_msg(sock):
    """Lee el encabezado para saber cuánto leer, y luego lee el payload completo."""
    # 1. Leer los primeros 4 bytes (tamaño)
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # 2. Leer exactamente esa cantidad de bytes
    data = recvall(sock, msglen)
    return json.loads(data.decode('utf-8'))

def recvall(sock, n):
    """Función auxiliar para asegurar que leemos N bytes completos."""
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

# --- Algoritmos de Ordenamiento ---
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped: break
    return arr

def quick_sort(arr):
    if len(arr) <= 1: return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]; R = arr[mid:]
        merge_sort(L); merge_sort(R)
        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]: arr[k] = L[i]; i += 1
            else: arr[k] = R[j]; j += 1
            k += 1
        while i < len(L): arr[k] = L[i]; i += 1; k += 1
        while j < len(R): arr[k] = R[j]; j += 1; k += 1
    return arr

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]; j -= 1
        arr[j + 1] = key
    return arr

def sort_and_measure(algorithm_name, arr, results, lock):
    # Copia de la lista para no afectar a otros hilos
    arr_copy = list(arr)
    start_time = time.time()
    
    if algorithm_name == 'bubble': bubble_sort(arr_copy)
    elif algorithm_name == 'quick': arr_copy = quick_sort(arr_copy)
    elif algorithm_name == 'merge': merge_sort(arr_copy)
    elif algorithm_name == 'insertion': insertion_sort(arr_copy)
    
    end_time = time.time()
    with lock:
        results[algorithm_name] = {"time": (end_time - start_time) * 1000, "sorted": arr_copy}

# --- Lógica del Servidor ---
print(f"Generando lista de {LIST_SIZE} elementos...")
list_to_sort = [random.randint(0, 100000) for _ in range(LIST_SIZE)]
print("Lista lista.")

def handle_client(conn, addr):
    print(f"[CONEXIÓN] Cliente conectado desde {addr}")
    try:
        req = recv_msg(conn)
        if not req: return

        command = req.get('command')
        
        if command == 'solicitar_lista':
            response = {"original": list_to_sort}
            send_msg(conn, response)
            
        elif command == 'solicitar_tiempos':
            print(f"Iniciando cálculo de ordenamientos para {addr}...")
            results = {}
            threads = []
            lock = threading.Lock()
            
            # Hilos para procesamiento paralelo de algoritmos
            for algo in ['bubble', 'quick', 'merge', 'insertion']:
                t = threading.Thread(target=sort_and_measure, args=(algo, list_to_sort, results, lock))
                threads.append(t)
                t.start()
            
            for t in threads: t.join() # Esperar a que todos terminen
            
            response = {
                "sorted": {algo: results[algo]["sorted"] for algo in results},
                "times": {algo: results[algo]["time"] for algo in results}
            }
            send_msg(conn, response)
            print(f"Resultados enviados a {addr}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[TCP SERVER] Escuchando en {HOST}:{PORT}")
    
    while True:
        conn, addr = server.accept()
        # Cada cliente se maneja en un hilo independiente
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    main()