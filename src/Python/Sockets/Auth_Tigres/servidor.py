import socket
import threading
import json

# Configuración de red
HOST = '127.0.0.1'
PORT = 65432

# Base de datos simulada
USUARIOS_VALIDOS = {
    "tigres": "1234",
    "admin": "admin",
    "usuario": "pass"
}

def manejar_cliente(conn, addr):
    print(f"[CONEXIÓN] Nuevo intento desde: {addr}")
    try:
        data = conn.recv(1024).decode('utf-8')
        if not data:
            return

        # Procesar datos recibidos (JSON)
        credenciales = json.loads(data)
        usuario = credenciales.get("user")
        password = credenciales.get("pass")

        print(f"[AUTH] Verificando usuario: {usuario}")

        # Lógica de validación
        response = {"status": "error", "msg": "Credenciales incorrectas"}
        
        if usuario in USUARIOS_VALIDOS:
            if USUARIOS_VALIDOS[usuario] == password:
                response = {"status": "ok", "msg": "Acceso concedido"}
                print(f"[AUTH] ¡Login exitoso para {usuario}!")
            else:
                print(f"[AUTH] Contraseña incorrecta para {usuario}")
        else:
            print(f"[AUTH] Usuario no encontrado")

        # Enviar respuesta
        conn.sendall(json.dumps(response).encode('utf-8'))

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()

def iniciar_servidor():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"--- SERVIDOR DE AUTENTICACIÓN ---")
    print(f"Escuchando en {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=manejar_cliente, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    iniciar_servidor()