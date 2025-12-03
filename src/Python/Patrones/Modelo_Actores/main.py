import socket
import threading
import time
from threading import Semaphore

class Actor:
    def __init__(self, name, port, peer_port):
        self.name = name
        self.port = port
        self.peer_port = peer_port
        self.state = "Disponible"
        self.sem = Semaphore(1)
        self.thread = threading.Thread(target=self.start_actor)

    def start_actor(self):
        threading.Thread(target=self.run_server, daemon=True).start()
        while True:
            self.send_message(f"Hola desde {self.name}")
            time.sleep(5)

    def run_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', self.port))
        server_socket.listen(1)
        print(f"{self.name} escuchando en el puerto {self.port}")

        while True:
            client_socket, _ = server_socket.accept()
            message = client_socket.recv(1024).decode('utf-8')
            self.receive_message(message)
            client_socket.close()

    def send_message(self, message):
        self.sem.acquire()
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('localhost', self.peer_port))
                s.sendall(message.encode('utf-8'))
                print(f"{self.name} envió: {message}")
        except ConnectionRefusedError:
            print(f"{self.name}: No se pudo conectar con el otro actor.")
        finally:
            self.sem.release()

    def receive_message(self, message):
        print(f"{self.name} recibió: {message}")
        self.state = "Ocupado" if "Hola" in message else "Disponible"
        print(f"{self.name} está ahora en estado: {self.state}")

if __name__ == "__main__":
    actor1 = Actor(name="Actor1", port=5001, peer_port=5002)
    actor2 = Actor(name="Actor2", port=5002, peer_port=5001)

    actor1.thread.start()
    actor2.thread.start()

    actor1.thread.join()
    actor2.thread.join()
