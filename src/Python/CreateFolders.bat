@echo off
echo ==========================================
echo   GENERADOR DE ESTRUCTURA COMPLETA
echo   Proyecto Programacion Concurrente
echo ==========================================
echo.

:: --- A. DOCUMENTACION ---
echo [A] Creando carpeta Documentacion...
if not exist "Documentacion" md "Documentacion"

:: --- B. HILOS ---
echo [B] Creando carpeta Hilos...
if not exist "Hilos" md "Hilos"
:: Subcarpetas Programas
if not exist "Hilos\Memorama" md "Hilos\Memorama"
if not exist "Hilos\Ruleta_Mario" md "Hilos\Ruleta_Mario"
:: (Hilos_01 y Hilos_02 suelen ser archivos sueltos, se quedan en la raiz de Hilos)

:: --- C. SOCKETS ---
echo [C] Creando carpeta Sockets...
if not exist "Sockets" md "Sockets"
:: Subcarpetas Programas
if not exist "Sockets\Mensajes_SC" md "Sockets\Mensajes_SC"
if not exist "Sockets\Productos_Limpieza" md "Sockets\Productos_Limpieza"
if not exist "Sockets\TCP_Ordenamiento" md "Sockets\TCP_Ordenamiento"
if not exist "Sockets\UDP_Ordenamiento" md "Sockets\UDP_Ordenamiento"
if not exist "Sockets\UDP_Votaciones" md "Sockets\UDP_Votaciones"
if not exist "Sockets\Comunicacion_Directa" md "Sockets\Comunicacion_Directa"
if not exist "Sockets\Comunicacion_Indirecta" md "Sockets\Comunicacion_Indirecta"
if not exist "Sockets\Auth_Tigres" md "Sockets\Auth_Tigres"

:: --- D. SEMAFOROS ---
echo [D] Creando carpeta Semaforos...
if not exist "Semaforos" md "Semaforos"
:: Subcarpetas Programas
if not exist "Semaforos\Sincronizacion" md "Semaforos\Sincronizacion"
if not exist "Semaforos\Semaforos_SC" md "Semaforos\Semaforos_SC"
if not exist "Semaforos\Condicion_Carrera" md "Semaforos\Condicion_Carrera"
if not exist "Semaforos\Barbero_Dormilon" md "Semaforos\Barbero_Dormilon"
if not exist "Semaforos\Barbero_UDP" md "Semaforos\Barbero_UDP"
if not exist "Semaforos\Chat_1S3C" md "Semaforos\Chat_1S3C"
if not exist "Semaforos\Chat_Equipos" md "Semaforos\Chat_Equipos"

:: --- E. PATRONES ---
echo [E] Creando carpeta Patrones...
if not exist "Patrones" md "Patrones"
:: Subcarpetas Programas
if not exist "Patrones\Productor_Consumidor" md "Patrones\Productor_Consumidor"
if not exist "Patrones\Futuro_Promesa_01" md "Patrones\Futuro_Promesa_01"
if not exist "Patrones\Futuro_Promesa_02" md "Patrones\Futuro_Promesa_02"
if not exist "Patrones\Modelo_Actores" md "Patrones\Modelo_Actores"
if not exist "Patrones\Actores_SC" md "Patrones\Actores_SC"
if not exist "Patrones\Reactor_Proactor" md "Patrones\Reactor_Proactor"

echo.
echo ==========================================
echo   ESTRUCTURA LISTA.
echo   Ahora guarda tus .py dentro de cada carpeta.
echo ==========================================
pause