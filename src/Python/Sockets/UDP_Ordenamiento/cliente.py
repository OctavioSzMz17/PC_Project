import socket
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
import struct
import threading
import time

HOST = '127.0.0.1'
PORT = 65432
BUFFER_SIZE = 60000 

bars = {}
labels = {}
text_area = None
request_button = None

# --- Recepción Fragmentada UDP ---
def receive_fragmented_udp(sock):
    """Reensambla los paquetes UDP para formar la respuesta completa."""
    received_chunks = {}
    total_packets = None
    
    # IMPORTANTE: Bubble sort con 10k elementos tarda. Damos 60s de espera.
    sock.settimeout(60) 
    
    try:
        while True:
            try:
                packet, _ = sock.recvfrom(BUFFER_SIZE + 100)
            except socket.timeout:
                return None
            
            if len(packet) < 8: continue
            
            index, total = struct.unpack('>II', packet[:8])
            payload = packet[8:]
            
            if total_packets is None:
                total_packets = total
                print(f"Recibiendo {total} paquetes...")
            
            received_chunks[index] = payload
            
            if len(received_chunks) == total_packets:
                break
                
        full_data = b''
        for i in range(total_packets):
            full_data += received_chunks.get(i, b'')
            
        return json.loads(full_data.decode('utf-8'))
        
    except Exception as e:
        print(f"Error en recepción UDP: {e}")
        return None

def send_udp_request(command):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        request = json.dumps({"command": command}).encode('utf-8')
        sock.sendto(request, (HOST, PORT))
        return receive_fragmented_udp(sock)
    finally:
        sock.close()

# --- Funciones GUI ---
def get_original_list():
    def run():
        response = send_udp_request('solicitar_lista')
        if response:
            root.after(0, lambda: update_text_area(response['original']))
    threading.Thread(target=run, daemon=True).start()

def update_text_area(data):
    text_area.insert(tk.END, f"{data}\n")

def request_and_update_times():
    request_button.config(state=tk.DISABLED, text="Calculando (Espere ~30s)...")
    
    def run():
        # Resetear barras
        for algo in ['bubble', 'quick', 'merge', 'insertion']:
             root.after(0, lambda a=algo: bars[a].configure(value=0))
             root.after(0, lambda a=algo: labels[a].configure(text=f"{a.capitalize()}: Calculando..."))

        response = send_udp_request('solicitar_tiempos')
        root.after(0, update_results_ui, response)

    threading.Thread(target=run, daemon=True).start()

def update_results_ui(response):
    request_button.config(state=tk.NORMAL, text="Iniciar Ordenamiento")
    
    if not response:
        messagebox.showerror("Timeout", "El servidor tardó demasiado (Bubble Sort es lento con 10k items) o se perdieron paquetes.")
        return

    times = response['times']
    sorted_lists = response['sorted']
    max_time = max(times.values()) if times else 1
    
    for algo, time_val in times.items():
        if algo in labels:
            labels[algo].config(text=f"{algo.capitalize()}: {time_val:.2f} ms")
            bars[algo]['value'] = (time_val / max_time) * 100
            show_sorted_window(algo, sorted_lists[algo])

def show_sorted_window(algo, arr):
    win = tk.Toplevel(root)
    win.title(f"{algo} - 10,000 Elementos")
    win.geometry("600x400")
    
    l = ttk.Label(win, text=f"{algo} Sort (n={len(arr)})", font=('Arial', 12, 'bold'))
    l.pack(pady=5)
    
    t = scrolledtext.ScrolledText(win, width=70, height=20)
    t.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    t.insert(tk.END, str(arr))

# --- GUI Principal ---
root = tk.Tk()
root.title("Cliente UDP - 10,000 Elementos")
root.geometry("800x600")

ttk.Label(root, text="Ordenamiento UDP (10k Elementos)", font=('Arial', 14, 'bold')).pack(pady=10)

frame_orig = ttk.LabelFrame(root, text="Lista Original (Muestra)")
frame_orig.pack(fill=tk.X, padx=10)
text_area = scrolledtext.ScrolledText(frame_orig, height=5)
text_area.pack(fill=tk.X, padx=5, pady=5)

frame_res = ttk.LabelFrame(root, text="Tiempos de Ejecución")
frame_res.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

for algo in ["bubble", "quick", "merge", "insertion"]:
    f = ttk.Frame(frame_res)
    f.pack(fill=tk.X, padx=10, pady=5)
    labels[algo] = ttk.Label(f, text=f"{algo.capitalize()}: ---", width=20)
    labels[algo].pack(side=tk.LEFT)
    bars[algo] = ttk.Progressbar(f, length=400)
    bars[algo].pack(side=tk.LEFT, fill=tk.X, expand=True)

request_button = ttk.Button(root, text="Iniciar Ordenamiento", command=request_and_update_times)
request_button.pack(pady=20)

get_original_list()
root.mainloop()