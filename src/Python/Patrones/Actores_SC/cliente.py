import tkinter as tk
from tkinter import scrolledtext
import socket
import threading
import time

class ClienteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cliente Mensajería (Tkinter)")
        self.root.geometry("500x400")
        
        self.running = False

        # --- Interfaz Gráfica ---
        frame_top = tk.Frame(root, pady=10)
        frame_top.pack()

        self.btn_connect = tk.Button(frame_top, text="Conectar y Enviar", command=self.start_client_thread, bg="#2196F3", fg="white")
        self.btn_connect.pack(side=tk.LEFT, padx=10)

        self.btn_stop = tk.Button(frame_top, text="Detener", command=self.stop_client, bg="#f44336", fg="white", state=tk.DISABLED)
        self.btn_stop.pack(side=tk.LEFT, padx=10)

        self.log_area = scrolledtext.ScrolledText(root, state='disabled', height=20)
        self.log_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def log(self, mensaje):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, mensaje + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

    def start_client_thread(self):
        self.running = True
        self.btn_connect.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)
        # Hilo separado para no bloquear la ventana
        threading.Thread(target=self.logic_send_messages, daemon=True).start()

    def stop_client(self):
        self.running = False
        self.log("🛑 Deteniendo cliente...")
        self.btn_connect.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)

    def logic_send_messages(self, host='localhost', port=8080):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Intentar conectar con reintentos
        connected = False
        for i in range(5):
            if not self.running: return
            try:
                self.log(f"Intentando conectar a {host}:{port} ({i+1}/5)...")
                client_socket.connect((host, port))
                connected = True
                self.log("✅ Conectado exitosamente.")
                break
            except ConnectionRefusedError:
                self.log("⏳ Servidor no encontrado, reintentando en 1s...")
                time.sleep(1)
        
        if not connected:
            self.log("❌ No se pudo conectar. Asegúrate de encender el servidor.")
            self.stop_client()
            return

        message_counter = 0

        try:
            while self.running:
                message_counter += 1
                msg = f"Mensaje {message_counter}"
                
                client_socket.send(msg.encode('utf-8'))
                self.log(f"📤 Enviado: {msg}")

                # Esperar respuesta (bloqueante, pero está en hilo secundario)
                try:
                    response = client_socket.recv(1024).decode('utf-8')
                    if "STOP" in response or not response:
                        self.log(f"🛑 El servidor finalizó la conexión: {response}")
                        break
                    
                    self.log(f"📥 Respuesta: {response}")
                except:
                    break

                time.sleep(1) # Pausa entre mensajes

        except Exception as e:
            self.log(f"Error de conexión: {e}")
        finally:
            client_socket.close()
            self.log("Fin de la comunicación.")
            # Usamos root.after para modificar la GUI desde el hilo de manera segura
            self.root.after(0, self.stop_client)

    def on_closing(self):
        self.running = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ClienteApp(root)
    root.mainloop()