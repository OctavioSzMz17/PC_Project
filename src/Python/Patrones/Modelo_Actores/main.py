import socket
import threading
import time
from threading import Semaphore, Event

# 1. Definimos el evento maestro para detener todo
stop_event = Event()

class Actor:
    def __init__(self, name, port, peer_port):
        self.name = name
        self.port = port
        self.peer_port = peer_port
        self.state = "Disponible"
        self.sem = Semaphore(1)
        # El hilo principal del actor
        self.thread = threading.Thread(target=self.start_actor)

    def start_actor(self):
        # Iniciamos el servidor en un hilo daemon (se cierra si el principal muere)
        threading.Thread(target=self.run_server, daemon=True).start()
        
        # 2. Reemplazamos 'while True' por chequeo del evento
        print(f"[{self.name}] Iniciado y listo para enviar mensajes.")
        while not stop_event.is_set():
            self.send_message(f"Hola desde {self.name}")
            
            # 3. Usamos wait en vez de sleep.
            # Si presionas Ctrl+C, no espera los 5 segundos, se detiene al instante.
            stop_event.wait(5)

    def run_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Permite reutilizar el puerto inmediatamente (evita error "Address already in use")
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            server_socket.bind(('localhost', self.port))
            server_socket.listen(1)
            # 4. Timeout para que el accept no congele el hilo eternamente
            server_socket.settimeout(1.0)
            print(f"[{self.name}] Servidor escuchando en puerto {self.port}")

            while not stop_event.is_set():
                try:
                    client_socket, _ = server_socket.accept()
                    message = client_socket.recv(1024).decode('utf-8')
                    self.receive_message(message)
                    client_socket.close()
                except socket.timeout:
                    # Cada segundo revisa si stop_event se activó
                    continue
                except OSError:
                    break
        except Exception as e:
            print(f"[{self.name}] Error en servidor: {e}")
        finally:
            server_socket.close()
            print(f"[{self.name}] Servidor detenido.")

    def send_message(self, message):
        # Si ya nos estamos apagando, no intentamos enviar nada
        if stop_event.is_set(): return

        self.sem.acquire()
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2.0) # Timeout de conexión
                s.connect(('localhost', self.peer_port))
                s.sendall(message.encode('utf-8'))
                print(f"📤 {self.name} envió: {message}")
        except (ConnectionRefusedError, socket.timeout):
            # Es normal si el otro actor aún no inicia o ya se cerró
            if not stop_event.is_set():
                print(f"⚠️ {self.name}: No se pudo conectar con el puerto {self.peer_port}.")
        except Exception as e:
            print(f"❌ Error enviando: {e}")
        finally:
            self.sem.release()

    def receive_message(self, message):
        print(f"📥 {self.name} recibió: {message}")
        self.state = "Ocupado" if "Hola" in message else "Disponible"
        # print(f"{self.name} estado: {self.state}")

if __name__ == "__main__":
    print("=== SISTEMA DE ACTORES CONCURRENTES ===")
    print("Presiona Ctrl + C para detener el programa limpiamente.\n")

    actor1 = Actor(name="Actor1", port=5001, peer_port=5002)
    actor2 = Actor(name="Actor2", port=5002, peer_port=5001)

    actor1.thread.start()
    actor2.thread.start()

    try:
        # 5. Mantenemos el hilo principal vivo vigilando interrupciones
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n\n🛑 Interrupción detectada (Ctrl+C). Deteniendo actores...")
        stop_event.set() # ¡Orden global de apagado!

    # Esperamos a que los hilos terminen sus tareas pendientes y cierren
    actor1.thread.join()
    actor2.thread.join()
    
    print("✅ Ejecución finalizada correctamente.")