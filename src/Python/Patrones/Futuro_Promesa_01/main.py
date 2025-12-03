import concurrent.futures
import time

# Función que simula una operación costosa
def operacion_lenta():
    print("Comenzando operación lenta...")
    time.sleep(3)  # Simula un trabajo pesado de 3 segundos
    return "Resultado listo!"

# Usamos ThreadPoolExecutor para manejar la concurrencia
with concurrent.futures.ThreadPoolExecutor() as executor:
    # Enviar una tarea al pool de hilos. El resultado será un futuro.
    futuro = executor.submit(operacion_lenta)

    print("Haciendo otras cosas mientras esperamos el resultado...")

    # Bloquea aquí hasta que el resultado esté disponible
    resultado = futuro.result()
    print(f"El resultado de la operación es: {resultado}")


input("\n--- Ejecución finalizada. Presiona ENTER para cerrar ---")