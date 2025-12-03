import socket
import threading
import sys

# Configuración Global
global_message_count = 0
message_limit = 0 
mutex = threading.Lock()
server_running = True

def handle_client(client_socket, client_address):
    global global_message_count, server_running
    
    print(f"[+] Conexión aceptada de: {client_address}")
    
    while server_running:
        try:
            # Recibir mensaje (buffer de 1024 bytes)
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            
            print(f"[{client_address[1]}] Dice: {message}")

            # Sección Crítica: Actualizar contador
            with mutex:
                global_message_count += 1
                current_count = global_message_count
                
                if current_count > message_limit:
                    print(f"⚠️ Límite excedido ({current_count}/{message_limit}). Cerrando conexión.")
                    msg_final = "STOP: Limite alcanzado"
                    client_socket.send(msg_final.encode('utf-8'))
                    server_running = False
                    break
            
            # Enviar respuesta normal
            response = f"Servidor procesó tu mensaje #{current_count}"
            client_socket.send(response.encode('utf-8'))
        
        except ConnectionResetError:
            print(f"[-] El cliente {client_address} cerró la conexión forzosamente.")
            break
        except Exception as e:
            print(f"Error con {client_address}: {e}")
            break

    client_socket.close()
    print(f"[-] Conexión cerrada con {client_address}")

def start_server(host='localhost', port=8080):
    global message_limit, server_running
    
    print("=== SERVIDOR DE PROCESAMIENTO ===")
    try:
        entrada = input("Ingrese el límite global de mensajes a procesar: ")
        message_limit = int(entrada)
    except ValueError:
        print("❌ Error: Debes ingresar un número entero.")
        input("Presiona Enter para salir...")
        return

    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"\n🚀 Servidor escuchando en {host}:{port}")
        print("Esperando clientes...")

        # Establecemos un timeout para que el accept no bloquee por siempre y podamos revisar si server_running cambió
        server_socket.settimeout(1.0) 

        while server_running:
            try:
                client_socket, client_address = server_socket.accept()
                # Creamos un hilo para cada cliente
                t = threading.Thread(target=handle_client, args=(client_socket, client_address))
                t.daemon = True # El hilo muere si el principal muere
                t.start()
            except socket.timeout:
                continue
            except Exception as e:
                print(f"Error aceptando conexión: {e}")

    except Exception as e:
        print(f"\n Error fatal en el servidor: {e}")
    finally:
        print("\n Servidor detenido.")
        if 'server_socket' in locals():
            server_socket.close()
        input("\nPresiona Enter para cerrar esta ventana...")

if __name__ == "__main__":
    start_server()