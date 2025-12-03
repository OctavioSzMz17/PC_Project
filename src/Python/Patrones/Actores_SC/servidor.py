import tkinter as tk
from tkinter import scrolledtext, messagebox
import socket
import threading

class ServidorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Servidor Concurrente (Tkinter)")
        self.root.geometry("600x450")
        
        # --- Configuración de Estado ---
        self.server_running = False
        self.server_socket = None
        self.global_message_count = 0
        self.message_limit = 0
        self.mutex = threading.Lock()

        # --- Interfaz Gráfica ---
        # Frame superior para configuración
        frame_top = tk.Frame(root, pady=10)
        frame_top.pack()

        tk.Label(frame_top, text="Límite de mensajes:").pack(side=tk.LEFT, padx=5)
        
        self.entry_limit = tk.Entry(frame_top, width=10)
        self.entry_limit.insert(0, "10") # Valor por defecto
        self.entry_limit.pack(side=tk.LEFT, padx=5)

        self.btn_start = tk.Button(frame_top, text="Iniciar Servidor", command=self.iniciar_servidor, bg="#4CAF50", fg="white")
        self.btn_start.pack(side=tk.LEFT, padx=10)

        self.btn_stop = tk.Button(frame_top, text="Detener", command=self.detener_servidor, bg="#f44336", fg="white", state=tk.DISABLED)
        self.btn_stop.pack(side=tk.LEFT, padx=5)

        # Área de logs (Simula la terminal)
        self.log_area = scrolledtext.ScrolledText(root, state='disabled', height=20)
        self.log_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Manejo de cierre de ventana
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def log(self, mensaje):
        """Escribe en el área de texto de manera segura para hilos."""
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, mensaje + "\n")
        self.log_area.see(tk.END) # Auto-scroll al final
        self.log_area.config(state='disabled')

    def iniciar_servidor(self):
        try:
            limit = int(self.entry_limit.get())
            if limit <= 0: raise ValueError
            self.message_limit = limit
        except ValueError:
            messagebox.showerror("Error", "El límite debe ser un número entero positivo.")
            return

        self.server_running = True
        self.global_message_count = 0
        
        # Actualizar botones
        self.btn_start.config(state=tk.DISABLED)
        self.entry_limit.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)
        
        self.log(f"=== INICIANDO SERVIDOR (Límite: {limit}) ===")
        
        # Lanzar el servidor en un hilo aparte para no congelar la GUI
        threading.Thread(target=self.run_server_logic, daemon=True).start()

    def detener_servidor(self):
        self.server_running = False
        if self.server_socket:
            try:
                self.server_socket.close() # Esto forzará una excepción en el accept() y romperá el bucle
            except:
                pass
        self.log("🛑 Servidor detenido manualmente.")
        self.reset_ui()

    def reset_ui(self):
        self.btn_start.config(state=tk.NORMAL)
        self.entry_limit.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)

    def handle_client(self, client_socket, client_address):
        self.log(f"[+] Conexión aceptada de: {client_address}")
        
        while self.server_running:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if not message: break
                
                self.log(f"[{client_address[1]}] Dice: {message}")

                with self.mutex:
                    self.global_message_count += 1
                    current_count = self.global_message_count
                    
                    self.log(f"   -> Procesados: {current_count}/{self.message_limit}")

                    if current_count > self.message_limit:
                        self.log(f"⚠️ Límite excedido. Cerrando conexión con {client_address}.")
                        msg_final = "STOP: Limite alcanzado"
                        client_socket.send(msg_final.encode('utf-8'))
                        # Opcional: Detener todo el servidor si se alcanza el límite global
                        # self.server_running = False 
                        break
                
                response = f"Servidor procesó tu mensaje #{current_count}"
                client_socket.send(response.encode('utf-8'))

            except ConnectionResetError:
                break
            except Exception as e:
                self.log(f"Error con cliente: {e}")
                break
        
        client_socket.close()
        self.log(f"[-] Conexión cerrada con {client_address}")

    def run_server_logic(self):
        host = 'localhost'
        port = 8080
        
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Permite reusar el puerto si cierras y abres rápido
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((host, port))
            self.server_socket.listen(5)
            self.log(f"🚀 Escuchando en {host}:{port}")

            self.server_socket.settimeout(1.0) # Importante para poder detener el bucle

            while self.server_running:
                try:
                    client_sock, addr = self.server_socket.accept()
                    t = threading.Thread(target=self.handle_client, args=(client_sock, addr))
                    t.daemon = True
                    t.start()
                except socket.timeout:
                    continue
                except OSError:
                    break # Socket cerrado
        except Exception as e:
            self.log(f"Error fatal: {e}")
        finally:
            if self.server_socket: self.server_socket.close()

    def on_closing(self):
        self.detener_servidor()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ServidorApp(root)
    root.mainloop()