import socket

# Dirección y puerto del servidor
HOST = '127.0.0.1'   # Dirección local (localhost)
PORT = 65432         # Puerto a escuchar

# Crear un socket TCP/IP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))   # Vincular el socket a la dirección y puerto
    s.listen()             # Comenzar a escuchar conexiones
    print("Servidor: Esperando conexión del cliente...")

    # Aceptar una conexión
    conn, addr = s.accept()
    with conn:
        print(f"Servidor: Conectado por {addr}")
        while True:
            data = conn.recv(1024)  # Recibir datos del cliente
            if not data:
                break
            print(f"Servidor recibe: {data.decode()}")
            conn.sendall(b"Hola desde el servidor!")  # Enviar respuesta al cliente

input("\n--- Ejecución finalizada. Presiona ENTER para cerrar ---")
