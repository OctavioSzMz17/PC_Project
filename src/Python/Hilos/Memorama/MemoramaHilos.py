import random
import time
import datetime
import os
import threading

# Definir la matriz de números y la matriz visible
numeros = [[random.randint(1, 5) for _ in range(3)] for _ in range(3)]
matriz_visible = [["?" for _ in range(3)] for _ in range(3)]

# Variables globales para controlar el juego
juego_terminado = False
tiempo_limite = 60
intentos_limite = 6 # Puedes ajustar este valor

def temporizador():
    global juego_terminado
    time.sleep(tiempo_limite)
    if not juego_terminado:
        print("\n¡Tiempo agotado! El juego ha terminado.")
        juego_terminado = True

def mostrar_matriz():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("+-------+-------+-------+")
    for fila in matriz_visible:
        for numero in fila:
            print(f"| {numero}   ", end='')
        print("|")
        print("+-------+-------+-------+")

# Pedir el nombre del jugador
nombre_jugador = input("Ingrese su nombre: ")

# Iniciar el temporizador en un hilo separado
hilo_temporizador = threading.Thread(target=temporizador)
hilo_temporizador.start()

# Inicializar el número de intentos
intentos = 0
tiempo_inicio = time.time()

# Bucle principal del juego
while not juego_terminado:
    mostrar_matriz()
    
    # Mostrar el estado actual
    tiempo_transcurrido = time.time() - tiempo_inicio
    print(f"Tiempo restante: {tiempo_limite - tiempo_transcurrido:.2f} segundos")
    print(f"Intentos restantes: {intentos_limite - intentos}")

    try:
        fila_revelar = int(input("Ingrese la fila (1-3) para revelar un número: ")) - 1
        columna_revelar = int(input("Ingrese la columna (1-3) para revelar un número: ")) - 1
    except ValueError:
        print("Entrada inválida. Debe ser un número.")
        time.sleep(1)
        continue

    # Verificar si el juego ha terminado antes de continuar
    if juego_terminado:
        break

    if not (0 <= fila_revelar <= 2 and 0 <= columna_revelar <= 2):
        print("Coordenadas fuera de rango. Intente de nuevo.")
        time.sleep(1)
        continue

    if matriz_visible[fila_revelar][columna_revelar] != "?":
        print("Ese número ya está revelado. Intente de nuevo.")
        time.sleep(1)
        continue
    
    # Destapar el primer número
    matriz_visible[fila_revelar][columna_revelar] = numeros[fila_revelar][columna_revelar]
    mostrar_matriz()
    
    try:
        fila_encontrar = int(input("Ingrese la fila (1-3) donde cree que está el mismo número: ")) - 1
        columna_encontrar = int(input("Ingrese la columna (1-3) donde cree que está el mismo número: ")) - 1
    except ValueError:
        print("Entrada inválida. Debe ser un número.")
        time.sleep(1)
        continue

    # Verificar si el juego ha terminado antes de continuar
    if juego_terminado:
        break
    
    if not (0 <= fila_encontrar <= 2 and 0 <= columna_encontrar <= 2):
        print("Coordenadas fuera de rango. Intente de nuevo.")
        time.sleep(1)
        continue

    # Destapar el segundo número
    matriz_visible[fila_encontrar][columna_encontrar] = numeros[fila_encontrar][columna_encontrar]
    mostrar_matriz()
    
    # Comparar los números
    if numeros[fila_revelar][columna_revelar] == numeros[fila_encontrar][columna_encontrar]:
        print("¡Acertaste!")
        time.sleep(1)
    else:
        print("Lo siento, no es el mismo número.")
        time.sleep(1)
        matriz_visible[fila_revelar][columna_revelar] = "?"
        matriz_visible[fila_encontrar][columna_encontrar] = "?"
    
    # Aumentar intentos y verificar el límite
    intentos += 1
    if intentos >= intentos_limite:
        print("\n¡Se te acabaron los intentos! El juego ha terminado.")
        juego_terminado = True

    # Verificar si se han revelado todos los números
    if all(isinstance(numero, int) for fila in matriz_visible for numero in fila):
        juego_terminado = True
        break
    
# Esperar a que el hilo del temporizador termine si el juego acabó antes
if hilo_temporizador.is_alive():
    hilo_temporizador.join(timeout=1)
    
tiempo_fin = time.time()
tiempo_total = tiempo_fin - tiempo_inicio

# Guardar los resultados en un archivo
if juego_terminado:
    with open("resultados.txt", "a") as archivo:
        archivo.write(f"Nombre: {nombre_jugador}\n")
        archivo.write(f"Intentos: {intentos}\n")
        archivo.write(f"Tiempo: {tiempo_total:.2f} segundos\n")
        archivo.write(f"Fecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

    # Mostrar los resultados
    print(f"¡Juego terminado! Tus resultados son:")
    print(f"Nombre: {nombre_jugador}")
    print(f"Intentos: {intentos}")
    print(f"Tiempo: {tiempo_total:.2f} segundos")