import socket

# Dirección y puerto del servidor
HOST = '127.0.0.1'   # Dirección local (localhost)
PORT = 65432         # Puerto al que conectarse

# Crear un socket TCP/IP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))  # Conectarse al servidor
    mensaje = "Hola desde el cliente!"
    s.sendall(mensaje.encode())  # Enviar un mensaje al servidor
    data = s.recv(1024)          # Recibir la respuesta del servidor

print()
print(f"Cliente recibe: {data.decode()}")

input("\n--- Ejecución finalizada. Presiona ENTER para cerrar ---")
