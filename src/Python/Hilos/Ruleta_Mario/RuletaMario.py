import random
import time
import threading
import sys

# --- Configuración del Juego ---
# Símbolos y sus valores en puntos
SYMBOLS = {
    '🌸': 3,
    '🍄': 2,
    '⭐': 5
}

# Velocidad a la que cambian los símbolos (en segundos)
SPIN_SPEED = 0.2

# --- Variables Globales para la Animación ---
spinning = False
current_symbol = ''

def spinner(slot_number):
    """
    Función que se ejecuta en un hilo separado para mostrar la animación
    de los símbolos cambiando.
    """
    global current_symbol
    symbols_list = list(SYMBOLS.keys())
    
    while spinning:
        chosen_symbol = random.choice(symbols_list)
        current_symbol = chosen_symbol
        
        sys.stdout.write(f"\rApartado {slot_number}: {chosen_symbol}  ")
        sys.stdout.flush()
        
        time.sleep(SPIN_SPEED)

def play_game():
    """Función principal que contiene la lógica del juego."""
    print("Comenzando una nueva ronda...")
    
    results = []
    
    for i in range(1, 4):
        global spinning
        spinning = True
        
        spin_thread = threading.Thread(target=spinner, args=(i,))
        spin_thread.start()
        
        input()  # Detener el apartado
        
        spinning = False
        spin_thread.join()
        
        results.append(current_symbol)
        print()

    # --- Mostrar Resultados Finales ---
    final_result_str = " ".join(results)
    print(f"Resultado final: {final_result_str}")
    
    if results[0] == results[1] == results[2]:
        winning_symbol = results[0]
        points_won = SYMBOLS[winning_symbol]
        print(f"¡Felicidades! Ganaste {points_won} puntos.")
    else:
        print("No ganaste esta vez. ¡Mejor suerte la próxima!")
    
    print()

# --- Bucle Principal ---
if __name__ == "__main__":
    print("¡BIENVENIDO A LA MÁQUINA TRAGAMONEDAS!")
    print("Presiona 'Entrar' para detener cada apartado.")
    
    while True:
        play_game()
        
        again = input("¿Quieres intentarlo de nuevo? (s/n): ").lower()
        if again != 's':
            break
            
    print("\n¡Gracias por jugar! ¡Hasta pronto! 👋")

input("\n--- Ejecución finalizada. Presiona ENTER para cerrar ---")
