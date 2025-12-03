import socket
import random
import threading

# --- Configuración del Cliente ---
SERVER_HOST = '127.0.0.1'  # La IP del servidor
SERVER_PORT = 65432        # El puerto del servidor

# --- Datos de la Votación ---
lista_candidatos = [
    "Candidato Verde",
    "Candidato Blanco",
    "Candidato Rojo",
    "Candidato Azul",
    "Candidato Amarillo"
]
NUM_VOTANTES = 1000

# --- Función que ejecuta cada hilo (votante) ---
def enviar_voto():
    """
    Crea un socket, elige un candidato al azar y envía el voto al servidor.
    """
    try:
        # Cada hilo crea su propio socket para enviar el datagrama
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            candidato_elegido = random.choice(lista_candidatos)
            s.sendto(candidato_elegido.encode('utf-8'), (SERVER_HOST, SERVER_PORT))
    except Exception as e:
        print(f"Error al enviar voto: {e}")

# --- Lógica Principal ---
if __name__ == "__main__":
    hilos = []
    print(f"Simulando el envío de {NUM_VOTANTES} votos al servidor...")

    # Crear y lanzar los 1000 hilos
    for i in range(NUM_VOTANTES):
        hilo = threading.Thread(target=enviar_voto)
        hilos.append(hilo)
        hilo.start()

    # Esperar a que todos los hilos terminen su ejecución
    for hilo in hilos:
        hilo.join()

    print(f"Los {NUM_VOTANTES} votos han sido enviados.")

    input("\n--- Ejecución finalizada. Presiona ENTER para cerrar ---")
