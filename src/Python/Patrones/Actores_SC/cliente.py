import socket
import threading
import time

# Contador global de mensajes procesados
global_message_count = 0
message_limit = 10  # Límite global de mensajes (se controla en el servidor)

# Mutex para proteger el contador global
mutex = threading.Lock()

# Variable de condición para detener todos los hilos
condition = threading.Condition()

def send_messages_to_server(host='localhost', port=8080):
    global global_message_count
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
    except Exception as e:
        print(f"Error al conectar al servidor: {e}")
        return

    message_counter = 0

    try:
        while True:
            # Verificar si el límite global de mensajes ya ha sido alcanzado
            with mutex:
                if global_message_count >= message_limit:
                    print("Límite de mensajes alcanzado. Deteniendo el cliente.")
                    break
            
            # Enviar mensaje al servidor si el límite no ha sido alcanzado
            message = f"Mensaje {message_counter + 1}"
            client_socket.send(message.encode('utf-8'))
            print(f"Enviado: {message}")

            # Esperar la respuesta del servidor
            response = client_socket.recv(1024).decode('utf-8')
            print(f"Respuesta del servidor: {response}")

            # Incrementar el contador local
            message_counter += 1
            time.sleep(1)  # Esperar 1 segundo antes de enviar el siguiente mensaje

    except Exception as e:
        print(f"Error en la conexión con el servidor: {e}")
    finally:
        client_socket.close()

def start_client():
    threading.Thread(target=send_messages_to_server).start()

# Iniciar el cliente
if __name__ == "__main__":
    start_client()
