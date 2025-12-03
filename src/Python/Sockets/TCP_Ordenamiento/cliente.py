import socket
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
import struct
import threading

HOST = '127.0.0.1'
PORT = 65432

bars = {}
labels = {}
text_area = None
request_button = None

# --- Protocolo TCP Cliente ---
def send_msg(sock, msg_dict):
    msg_bytes = json.dumps(msg_dict).encode('utf-8')
    header = struct.pack('>I', len(msg_bytes))
    sock.sendall(header + msg_bytes)

def recv_msg(sock):
    raw_msglen = recvall(sock, 4)
    if not raw_msglen: return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    return json.loads(recvall(sock, msglen).decode('utf-8'))

def recvall(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet: return None
        data += packet
    return data

def connect_and_request(command):
    """Abre conexión TCP, envía comando, recibe respuesta y cierra."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        
        send_msg(sock, {"command": command})
        response = recv_msg(sock) # Bloqueante, pero seguro en TCP
        
        sock.close()
        return response
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None

# --- Lógica GUI ---
def get_original_list():
    def run():
        response = connect_and_request('solicitar_lista')
        if response:
            root.after(0, lambda: update_text_area(response['original']))
    threading.Thread(target=run, daemon=True).start()

def update_text_area(data):
    text_area.insert(tk.END, f"{data}\n")

def request_and_update_times():
    request_button.config(state=tk.DISABLED, text="Procesando (Espere Bubble Sort)...")
    
    def run():
        # Limpiar UI
        for algo in ["bubble", "quick", "merge", "insertion"]:
            root.after(0, lambda a=algo: bars[a].configure(value=0))
            root.after(0, lambda a=algo: labels[a].configure(text=f"{a.capitalize()}: Calculando..."))

        # Petición al servidor (Tardará unos segundos por el Bubble Sort de 10k items)
        response = connect_and_request('solicitar_tiempos')
        
        root.after(0, update_results_ui, response)

    threading.Thread(target=run, daemon=True).start()

def update_results_ui(response):
    request_button.config(state=tk.NORMAL, text="Iniciar Ordenamiento")
    
    if not response:
        messagebox.showerror("Error", "No se pudo obtener respuesta del servidor.")
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
    win.title(f"{algo} - 10,000 Elementos (TCP)")
    win.geometry("600x400")
    
    l = ttk.Label(win, text=f"{algo} Sort (n={len(arr)})", font=('Arial', 12, 'bold'))
    l.pack(pady=5)
    
    t = scrolledtext.ScrolledText(win, width=70, height=20)
    t.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    t.insert(tk.END, str(arr))

# --- GUI Principal ---
root = tk.Tk()
root.title("Cliente TCP - 10,000 Elementos")
root.geometry("800x600")

ttk.Label(root, text="Ordenamiento TCP (Socket Stream)", font=('Arial', 14, 'bold')).pack(pady=10)

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