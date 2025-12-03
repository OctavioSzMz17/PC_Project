import socket
import threading

# --- Configuración del Servidor ---
HOST = '127.0.0.1'  # IP Local (localhost)
PORT = 65432        # Puerto para escuchar

# --- Variables para la Votación ---
candidatos = {
    "Candidato Verde": 0,
    "Candidato Blanco": 0,
    "Candidato Rojo": 0,
    "Candidato Azul": 0,
    "Candidato Amarillo": 0
}
votos_recibidos = 0
total_votos = 1000
lock = threading.Lock()  # Lock para evitar que los hilos modifiquen los datos al mismo tiempo

# --- Creación y configuración del Socket UDP ---
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    print(f"Servidor de votaciones UDP iniciado en {HOST}:{PORT}")
    print("Esperando recibir 1000 votos...")

    while votos_recibidos < total_votos:
        data, addr = s.recvfrom(1024)
        voto = data.decode('utf-8')

        # Usamos un lock para garantizar la integridad de los datos compartidos
        with lock:
            if voto in candidatos:
                candidatos[voto] += 1
                votos_recibidos += 1
                print(f"Voto recibido para: {voto} desde {addr}")
            else:
                print(f"Voto inválido recibido desde {addr}: {voto}")

    print("\n----------------------------------------------------")
    print(f"Se han recibido los {total_votos} votos.")
    input("Presione ENTER para mostrar los resultados finales...")
    print("----------------------------------------------------")

    # --- Cálculo y Muestra de Resultados ---
    print("\nResultados de la votación:")
    print("Resultados de la votación:")  # Para emular la doble línea original
    
    ganador = ""
    max_votos = -1

    for candidato, num_votos in candidatos.items():
        print(f"{candidato} : {num_votos} votos")
        if num_votos > max_votos:
            max_votos = num_votos
            ganador = candidato

    print("\n====================================================")
    print(f"El ganador es: {ganador} con {max_votos} votos")
    print("====================================================")

input("\n--- Ejecución finalizada. Presiona ENTER para cerrar ---")
