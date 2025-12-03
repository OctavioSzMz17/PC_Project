import socket
import threading
import time
import random
import json
import struct
import sys
import math

# Aumentamos recursión para QuickSort con 10,000 elementos
sys.setrecursionlimit(15000)

HOST = '127.0.0.1'
PORT = 65432
BUFFER_SIZE = 60000 # Tamaño seguro por fragmento UDP
LIST_SIZE = 10000   # <--- CANTIDAD SOLICITADA EN TUS INSTRUCCIONES

# --- Lógica de Fragmentación UDP ---
def send_fragmented(sock, data_dict, addr):
    """Divide el JSON en paquetes para soportar 10,000 datos por UDP."""
    try:
        json_bytes = json.dumps(data_dict).encode('utf-8')
        total_len = len(json_bytes)
        
        # Reservamos espacio para encabezado (8 bytes)
        chunk_size = BUFFER_SIZE - 8 
        total_packets = math.ceil(total_len / chunk_size)
        
        print(f"--> Enviando {total_len} bytes en {total_packets} paquetes a {addr}...")

        for i in range(total_packets):
            start = i * chunk_size
            end = start + chunk_size
            chunk = json_bytes[start:end]
            
            # Encabezado: [Indice Actual] [Total Paquetes]
            header = struct.pack('>II', i, total_packets)
            sock.sendto(header + chunk, addr)
            
            # Pausa técnica para evitar desbordamiento de buffer en el receptor
            time.sleep(0.001) 
    except Exception as e:
        print(f"Error enviando fragmentos: {e}")

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
    # Trabajamos con copia para no afectar la lista original
    arr_copy = list(arr)
    start_time = time.time()
    
    if algorithm_name == 'bubble': bubble_sort(arr_copy)
    elif algorithm_name == 'quick': arr_copy = quick_sort(arr_copy)
    elif algorithm_name == 'merge': merge_sort(arr_copy)
    elif algorithm_name == 'insertion': insertion_sort(arr_copy)
    
    end_time = time.time()
    with lock:
        results[algorithm_name] = {"time": (end_time - start_time) * 1000, "sorted": arr_copy}

# --- Generación de lista única ---
print("Generando lista de 10,000 elementos... espere.")
list_to_sort = [random.randint(0, 100000) for _ in range(LIST_SIZE)]
print("Lista generada.")

def process_request(sock, data, addr):
    try:
        command = data.get('command')
        
        if command == 'solicitar_lista':
            response = {"original": list_to_sort}
            send_fragmented(sock, response, addr)

        elif command == 'solicitar_tiempos':
            print(f"Calculando ordenamientos para {addr} (esto tardará por Bubble Sort)...")
            results = {}
            threads = []
            lock = threading.Lock()
            
            # Lanzamos los 4 algoritmos en hilos
            algos = ['bubble', 'quick', 'merge', 'insertion']
            for algo in algos:
                t = threading.Thread(target=sort_and_measure, args=(algo, list_to_sort, results, lock))
                threads.append(t)
                t.start()
            
            for t in threads: t.join()

            # Enviamos respuesta masiva
            response = {
                "sorted": {algo: results[algo]["sorted"] for algo in results},
                "times": {algo: results[algo]["time"] for algo in results}
            }
            send_fragmented(sock, response, addr)
            print("Datos enviados.")
            
    except Exception as e:
        print(f"Error procesando solicitud: {e}")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((HOST, PORT))
    print(f"[UDP SERVER] Escuchando en {HOST}:{PORT}")
    print(f"[CONFIG] Procesando {LIST_SIZE} elementos.")

    while True:
        try:
            data_bytes, addr = server.recvfrom(BUFFER_SIZE)
            try:
                data = json.loads(data_bytes.decode('utf-8'))
                threading.Thread(target=process_request, args=(server, data, addr)).start()
            except:
                pass 
        except Exception as e:
            print(f"Error servidor: {e}")

if __name__ == "__main__":
    main()