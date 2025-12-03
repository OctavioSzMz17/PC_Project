import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import sys
from PIL import Image, ImageTk, ImageDraw

# Importamos el executer
from executer import Executer 

def obtener_ruta_base():
    """
    Devuelve la ruta raíz del proyecto.
    """
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

# =============================================================================
# COMPONENTE: BOTÓN MODERNO
# =============================================================================
class BotonModerno(tk.Canvas):
    def __init__(self, parent, text, command, fill_color_inicio, fill_color_fin, 
                 border_color, width=260, height=55, corner_radius=25, bg_color="#1e272e"):
        super().__init__(parent, width=width, height=height, bg=bg_color, highlightthickness=0)
        self.command = command
        self.text = text
        self.fill_color_inicio = fill_color_inicio
        self.fill_color_fin = fill_color_fin
        self.border_color = border_color
        self.width = width
        self.height = height
        self.corner_radius = min(corner_radius, height // 2)
        
        self.draw_button()
        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def rgb_to_hex(self, rgb):
        return '#%02x%02x%02x' % rgb

    def draw_button(self):
        self.delete("all")
        w, h, r = self.width, self.height, self.corner_radius
        bw, off = 3, 2
        
        # Degradado
        self.create_arc(off, off, r*2, h-off, start=90, extent=180, fill=self.fill_color_inicio, outline="")
        self.create_arc(w-r*2, off, w-off, h-off, start=270, extent=180, fill=self.fill_color_fin, outline="")

        rgb_start, rgb_end = self.hex_to_rgb(self.fill_color_inicio), self.hex_to_rgb(self.fill_color_fin)
        start_x, end_x = r, w - r
        total_dist = end_x - start_x
        if total_dist > 0:
            for i in range(int(total_dist) + 1):
                factor = i / total_dist
                c = [int(s + (e - s) * factor) for s, e in zip(rgb_start, rgb_end)]
                self.create_line(start_x + i, off, start_x + i, h-off, fill=self.rgb_to_hex(tuple(c)), width=1)

        # Bordes
        self.create_line(r, off, w-r, off, fill=self.border_color, width=bw)
        self.create_line(r, h-off, w-r, h-off, fill=self.border_color, width=bw)
        self.create_arc(off, off, r*2, h-off, start=90, extent=180, style="arc", outline=self.border_color, width=bw)
        self.create_arc(w-r*2, off, w-off, h-off, start=270, extent=180, style="arc", outline=self.border_color, width=bw)

        # Texto
        self.create_text((w/2)+1, (h/2)+1, text=self.text, fill="#2d3436", font=("Segoe UI", 11, "bold"))
        self.create_text(w/2, h/2, text=self.text, fill="white", font=("Segoe UI", 11, "bold"))

    def on_enter(self, event):
        self.config(cursor="hand2")
        w, h, r, off = self.width, self.height, self.corner_radius, 2
        # Efecto brillo
        self.create_rectangle(r, off, w-r, h-off, fill="#ffffff", stipple="gray25", outline="", tags="highlight")

    def on_leave(self, event):
        self.delete("highlight")

    def on_click(self, event):
        if self.command: self.command()

# =============================================================================
# CLASE PRINCIPAL UI
# =============================================================================
class ProyectoFinalUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Proyecto Final - Programación Concurrente")
        self.root.geometry("900x700")
        self.root.resizable(False, False)

        # Paleta de Colores Tigres UANL
        self.tigres_azul_oscuro = "#005DAB"
        self.tigres_azul_claro = "#003366" 
        self.tigres_amarillo_oscuro = "#FDB913"
        self.tigres_amarillo_claro = "#D89504" 
        self.rojo_salir_claro = "#ff6b6b"
        self.rojo_salir_oscuro = "#eb4d4b"
        self.button_bg_color = "#1e272e" 

        # Fondo
        ruta_base = obtener_ruta_base()
        # Aseguramos que la ruta sea compatible con diferentes OS
        ruta_imagen = os.path.join(ruta_base, "src", "images", "Fondo Tigres.png") 
        self.load_background_with_overlay(ruta_imagen)

        # --- MAPA DE ARCHIVOS ---
        # Nota: Todas las rutas son relativas a 'src/Python/'
        self.file_map = {
            # DOCUMENTACION (Se abrirán con visualPDF.py)
            #"Apunte de Introducción de Concurrencia": "Documentacion/Intro_Concurrencia.pdf",
            "Apunte de Introducción de Concurrencia": "Documentacion/AD.pdf",
            "Apunte de Hilos": "Documentacion/Apunte_Hilos.pdf",
            "Apunte de Sockets, TCP y UDP": "Documentacion/Apunte_Sockets.pdf",
            "Apunte de Semáforos": "Documentacion/Apunte_Semaforos.pdf",
            "Apunte de Tkinter": "Documentacion/Apunte_Tkinter.pdf",
            "Apunte de Sala de Chat Simple": "Documentacion/Apunte_Chat.pdf",
            "Apunte de Patrón de Future y Promesa": "Documentacion/Apunte_Future.pdf",
            "Apunte de Patrón de Productor-Consumidor": "Documentacion/Apunte_ProdCons.pdf",
            "Apunte de Patrón de Modelo de Actores": "Documentacion/Apunte_Actores.pdf",
            "Apunte de Patrón de Reactor y Proactor": "Documentacion/Apunte_Reactor.pdf",
            "Apunte de Expectativas de la Materia": "Documentacion/Expectativas.pdf",
            "Documentación del Proyecto Final": "Documentacion/Proyecto_Final.pdf",

            # HILOS
            "Hilos_01": "Hilos/Hilos_01.py",
            "Hilos_02": "Hilos/Hilos_02.py",
            "Memorama con Hilos": "Hilos/Memorama/MemoramaHilos.py",
            "Ruleta de Mario Bros": "Hilos/Ruleta_Mario/RuletaMario.py",

            # SOCKETS
            "Mensajes con Servidor/Cliente": {"tipo": "dual", "carpeta": "Sockets/Mensajes_SC", "server": "servidor.py", "client": "cliente.py"},
            "Productos de limpieza": {"tipo": "dual", "carpeta": "Sockets/Productos_Limpieza", "server": "servidor.py", "client": "cliente.py"},
            "Programa TCP Algoritmos de Ordenamiento con Servidor/Cliente": {"tipo": "dual", "carpeta": "Sockets/TCP_Ordenamiento", "server": "servidor.py", "client": "cliente.py"},
            "Programa UDP Algoritmos de Ordenamiento con Servidor/Cliente": {"tipo": "dual", "carpeta": "Sockets/UDP_Ordenamiento", "server": "servidor.py", "client": "cliente.py"},
            "Programa UDP Sistema de Votaciones con Servidor/Cliente": {"tipo": "dual", "carpeta": "Sockets/UDP_Votaciones", "server": "servidor.py", "client": "cliente.py"},
            "Programa de Comunicación Directa": "Sockets/Comunicacion_Directa/main.py",
            "Programa de Comunicación Indirecta": "Sockets/Comunicacion_Indirecta/main.py",
            "Programa de Autentificación Servidor/Cliente Tigres": {"tipo": "dual", "carpeta": "Sockets/Auth_Tigres", "server": "servidor.py", "client": "cliente.py"},

            # SEMAFOROS
            "Semáforos con Sincronización": "Semaforos/Sincronizacion/main.py",
            "Semáforos con Servidor/Cliente": {"tipo": "dual", "carpeta": "Semaforos/Semaforos_SC", "server": "servidor.py", "client": "cliente.py"},
            "Programa de Condición de Carrera": "Semaforos/Condicion_Carrera/main.py",
            "Programa de Barbero Dormilón": {"tipo": "dual", "carpeta": "Semaforos/Barbero_Dormilon", "server": "servidor.py", "client": "cliente.py"},
            "Programa de Barbero Dormilón con UDP Servidor/Cliente": {"tipo": "dual", "carpeta": "Semaforos/Barbero_UDP", "server": "servidor.py", "client": "cliente.py"},
            "Programa de Sala de Chat (Por lo menos un servidor y 3 Clientes)": {"tipo": "dual", "carpeta": "Semaforos/Chat_1S3C", "server": "servidor.py", "client": "cliente.py"},
            "Programa de Sala de Chat (Con un equipo de Servidor/Cliente y otros dos equipos externos como clientes)": {"tipo": "dual", "carpeta": "Semaforos/Chat_Equipos", "server": "servidor.py", "client": "cliente.py"},

            # PATRONES
            "Programa de Patrón Productor/Consumidor (fábrica de ensamblaje de Productos)": {"tipo": "dual", "carpeta": "Patrones/Productor_Consumidor", "server": "servidor.py", "client": "cliente.py"},
            "Programa de Patrón Futuro/Promesa _01": "Patrones/Futuro_Promesa_01/main.py",
            "Programa de Patrón Futuro/Promesa _02": "Patrones/Futuro_Promesa_02/main.py",
            "Programa de Patrón Modelo de Actores": "Patrones/Modelo_Actores/main.py",
            "Programa de Patrón Modelo de Actores Servidor/Cliente": {"tipo": "dual", "carpeta": "Patrones/Actores_SC", "server": "servidor.py", "client": "cliente.py"},
            "Programa de Patrón Reactor/Proactor": "Patrones/Reactor_Proactor/main.py",

            # EXTRAS
            "Nombre de los alumnos": "CREDITOS",
            "Matricula de los Alumnos": "MATRICULAS"
        }

        self.menu_structure = {
            "A.- Documentación": ["Apunte de Introducción de Concurrencia", "Apunte de Hilos", "Apunte de Sockets, TCP y UDP", "Apunte de Semáforos", "Apunte de Tkinter", "Apunte de Sala de Chat Simple", "Apunte de Patrón de Future y Promesa", "Apunte de Patrón de Productor-Consumidor", "Apunte de Patrón de Modelo de Actores", "Apunte de Patrón de Reactor y Proactor", "Apunte de Expectativas de la Materia", "Documentación del Proyecto Final"],
            "B.- Menu de Hilos": ["Hilos_01", "Hilos_02", "Memorama con Hilos", "Ruleta de Mario Bros"],
            "C.- Menu de Sockets": ["Mensajes con Servidor/Cliente", "Productos de limpieza", "Programa TCP Algoritmos de Ordenamiento con Servidor/Cliente", "Programa UDP Algoritmos de Ordenamiento con Servidor/Cliente", "Programa UDP Sistema de Votaciones con Servidor/Cliente", "Programa de Comunicación Directa", "Programa de Comunicación Indirecta", "Programa de Autentificación Servidor/Cliente Tigres"],
            "D.- Menu de Semáforos": ["Semáforos con Sincronización", "Semáforos con Servidor/Cliente", "Programa de Condición de Carrera", "Programa de Barbero Dormilón", "Programa de Barbero Dormilón con UDP Servidor/Cliente", "Programa de Sala de Chat (Por lo menos un servidor y 3 Clientes)", "Programa de Sala de Chat (Con un equipo de Servidor/Cliente y otros dos equipos externos como clientes)"],
            "E.- Menu de Patrones": ["Programa de Patrón Productor/Consumidor (fábrica de ensamblaje de Productos)", "Programa de Patrón Futuro/Promesa _01", "Programa de Patrón Futuro/Promesa _02", "Programa de Patrón Modelo de Actores", "Programa de Patrón Modelo de Actores Servidor/Cliente", "Programa de Patrón Reactor/Proactor"],
            "F.- Menu de Ayuda": ["Nombre de los alumnos", "Matricula de los Alumnos"]
        }
        self.crear_interfaz()

    def load_background_with_overlay(self, image_path):
        try:
            if not os.path.exists(image_path):
                print(f"Advertencia: No se encontró fondo en {image_path}")

            img = Image.open(image_path).convert("RGBA")
            img = img.resize((900, 700), Image.LANCZOS)
            
            # Crear overlay oscuro semitransparente
            overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)
            center_x = img.width // 2
            ancho_panel = 700
            # Rectángulo oscuro al centro
            draw.rectangle([(center_x - ancho_panel//2, 50), (center_x + ancho_panel//2, img.height - 50)], fill=(20, 20, 30, 180))
            
            img = Image.alpha_composite(img, overlay)
            self.bg_photo = ImageTk.PhotoImage(img)
            
            self.main_canvas = tk.Canvas(self.root, width=900, height=700, highlightthickness=0)
            self.main_canvas.pack(fill="both", expand=True)
            self.main_canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        except Exception as e:
            # Fallback si falla la imagen (pantalla gris oscura elegante)
            self.root.configure(bg="#1e272e")
            self.main_canvas = tk.Canvas(self.root, width=900, height=700, bg="#1e272e", highlightthickness=0)
            self.main_canvas.pack()

    def crear_interfaz(self):
        # Títulos
        self.main_canvas.create_text(453, 63, text="Programación Concurrente", font=("Segoe UI", 28, "bold"), fill="black")
        self.main_canvas.create_text(450, 60, text="Programación Concurrente", font=("Segoe UI", 28, "bold"), fill="white")
        self.main_canvas.create_text(450, 110, text="Menú Principal del Proyecto", font=("Segoe UI", 14), fill="#dfe6e9")

        # Botones Principales (Izquierda)
        btn_a = BotonModerno(self.main_canvas, "A.- Documentación", lambda: self.abrir_submenu("A.- Documentación"), self.tigres_azul_oscuro, self.tigres_azul_claro, self.tigres_amarillo_oscuro, bg_color=self.button_bg_color)
        btn_a.place(x=160, y=300)
        btn_c = BotonModerno(self.main_canvas, "C.- Menú de Sockets", lambda: self.abrir_submenu("C.- Menu de Sockets"), self.tigres_azul_oscuro, self.tigres_azul_claro, self.tigres_amarillo_oscuro, bg_color=self.button_bg_color)
        btn_c.place(x=160, y=380)
        btn_e = BotonModerno(self.main_canvas, "E.- Menú de Patrones", lambda: self.abrir_submenu("E.- Menu de Patrones"), self.tigres_azul_oscuro, self.tigres_azul_claro, self.tigres_amarillo_oscuro, bg_color=self.button_bg_color)
        btn_e.place(x=160, y=460)

        # Botones Principales (Derecha)
        btn_b = BotonModerno(self.main_canvas, "B.- Menú de Hilos", lambda: self.abrir_submenu("B.- Menu de Hilos"), self.tigres_amarillo_oscuro, self.tigres_amarillo_claro, self.tigres_azul_oscuro, bg_color=self.button_bg_color)
        btn_b.place(x=480, y=300)
        btn_d = BotonModerno(self.main_canvas, "D.- Menú de Semáforos", lambda: self.abrir_submenu("D.- Menu de Semáforos"), self.tigres_amarillo_oscuro, self.tigres_amarillo_claro, self.tigres_azul_oscuro, bg_color=self.button_bg_color)
        btn_d.place(x=480, y=380)
        btn_f = BotonModerno(self.main_canvas, "F.- Menú de Ayuda", lambda: self.abrir_submenu("F.- Menu de Ayuda"), self.tigres_amarillo_oscuro, self.tigres_amarillo_claro, self.tigres_azul_oscuro, bg_color=self.button_bg_color)
        btn_f.place(x=480, y=460)

        # Botón Salir
        btn_g = BotonModerno(self.main_canvas, "G.- Salir", self.root.quit, self.rojo_salir_claro, self.rojo_salir_oscuro, self.tigres_azul_oscuro, width=300, bg_color=self.button_bg_color)
        btn_g.place(x=300, y=550)

    def abrir_submenu(self, key_seccion):
        items = self.menu_structure.get(key_seccion, [])
        sub = tk.Toplevel(self.root)
        sub.title(key_seccion)
        sub.geometry("650x650")
        sub.resizable(False, False)
        sub.transient(self.root)
        sub.grab_set()

        # Reutilizamos fondo en submenú
        bg_canvas = tk.Canvas(sub, width=650, height=650, bg="#2d3436", highlightthickness=0)
        bg_canvas.pack(fill="both", expand=True)

        # Título Submenú
        bg_canvas.create_text(328, 63, text=key_seccion, font=("Segoe UI", 16, "bold"), fill="black")
        bg_canvas.create_text(325, 60, text=key_seccion, font=("Segoe UI", 16, "bold"), fill=self.tigres_amarillo_oscuro)

        # Frame contenedor para Scroll
        panel_frame = tk.Frame(bg_canvas, bg="#2d3436")
        bg_canvas.create_window(325, 360, window=panel_frame, width=600, height=460)

        # Scrollbar logic
        canvas = tk.Canvas(panel_frame, bg="#2d3436", highlightthickness=0)
        scrollbar = ttk.Scrollbar(panel_frame, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="#2d3436")

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw", width=580)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")

        # Generar botones del submenú
        for i, item in enumerate(items):
            # Alternar colores
            if i % 2 == 0:
                fill_s, fill_e, border = self.tigres_azul_oscuro, self.tigres_azul_claro, self.tigres_amarillo_oscuro
            else:
                fill_s, fill_e, border = self.tigres_amarillo_oscuro, self.tigres_amarillo_claro, self.tigres_azul_oscuro

            btn = BotonModerno(scroll_frame, item, lambda i=item: self.ejecutar_programa(i),
                               fill_s, fill_e, border, width=580, height=45, corner_radius=10, bg_color="#2d3436")
            btn.pack(pady=5)

        # Botón Regresar
        btn_close = BotonModerno(bg_canvas, "Regresar", sub.destroy,
                                 self.tigres_azul_oscuro, self.tigres_azul_claro, self.tigres_amarillo_oscuro,
                                 width=150, height=40, corner_radius=15, bg_color="#2d3436")
        bg_canvas.create_window(325, 620, window=btn_close)

    def ejecutar_programa(self, nombre_programa):
        # Lógica de créditos
        if nombre_programa == "Nombre de los alumnos":
            messagebox.showinfo("Equipo", "Integrantes:\n- Sanchez Mendoza Octavio\n- Hernández Alarcón Kimberly Anette \n-Carpio Callejas Diana Ximena\n- Hernández Cruz Julio Hazel \n-Jiménez Ángeles Victor Jesús \n-Calderón López Mario Daniel")
            return
        if nombre_programa == "Matricula de los Alumnos":
            messagebox.showinfo("Matrículas", " - 2209003 \n - 2321123265 \n - 2331123258 \n - 2331123268 \n - 2231123631 \n - 2331123264") 
            return
        
        config = self.file_map.get(nombre_programa)
        if not config:
            messagebox.showwarning("Aviso", f"No hay archivo asignado para: {nombre_programa}")
            return

        # Construcción robusta de rutas absolutas
        ruta_base = obtener_ruta_base()
        
        if isinstance(config, dict) and config.get("tipo") == "dual":
            ruta_carpeta = os.path.join(ruta_base, "src", "Python", config["carpeta"])
            Executer.lanzar_dual(ruta_carpeta, config["server"], config["client"])

        elif isinstance(config, str):
            # Aquí es donde ocurre la magia para los PDFs
            ruta_archivo = os.path.join(ruta_base, "src", "Python", config)
            # Llamamos a lanzar_simple, el cual ahora sabe detectar si es PDF y llamar al visualPDF.py
            Executer.lanzar_simple(ruta_archivo)

if __name__ == "__main__":
    root = tk.Tk()
    app = ProyectoFinalUI(root)
    root.mainloop()