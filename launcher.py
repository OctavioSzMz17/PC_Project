import tkinter as tk
from tkinter import messagebox, font
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os
import sys
# Importamos lo necesario del menú principal
from mainMenu import BotonModerno, obtener_ruta_base, ProyectoFinalUI

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Acceso - Programación Concurrente")
        # --- NUEVAS DIMENSIONES ---
        self.ancho_ventana = 1000
        self.alto_ventana = 800
        self.root.geometry(f"{self.ancho_ventana}x{self.alto_ventana}")
        self.root.resizable(False, False)

        # 1. Preparar la imagen de fondo CON el panel semitransparente
        ruta_base = obtener_ruta_base()
        # Ajusta si tu imagen tiene otro nombre
        ruta_imagen = os.path.join(ruta_base, "src", "images", "p.png") 
        
        self.bg_photo = self.crear_fondo_con_panel(ruta_imagen)
        
        bg_label = tk.Label(self.root, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # --- 2. Colocar los Entradas (Entry) y el Botón ---
        # Ajustamos 'rely' (posición vertical relativa) para que caigan dentro del nuevo cuadro
        
        # Entrada Usuario
        self.entry_user = tk.Entry(self.root, font=("Segoe UI", 12), justify="center", bg="#dfe6e9", bd=0)
        self.entry_user.place(relx=0.5, rely=0.40, width=280, height=35, anchor="center")

        # Entrada Contraseña
        self.entry_pass = tk.Entry(self.root, font=("Segoe UI", 12), justify="center", bg="#dfe6e9", bd=0, show="*")
        self.entry_pass.place(relx=0.5, rely=0.52, width=280, height=35, anchor="center")

        # --- 3. Botón Ingresar ---
        c_azul = "#005DAB"
        c_azul_c = "#003366"
        c_amarillo = "#FDB913"
        
        self.btn_login = BotonModerno(self.root, "INGRESAR", self.validar_login, 
                                      c_azul, c_azul_c, c_amarillo, 
                                      width=280, height=50, corner_radius=25, bg_color="#15191d") 
        # Posición vertical del botón (rely)
        self.btn_login.place(relx=0.5, rely=0.65, anchor="center")

    def crear_fondo_con_panel(self, image_path):
        try:
            # A. Cargar y redimensionar al NUEVO tamaño (1000x800)
            base_img = Image.open(image_path).convert("RGBA")
            base_img = base_img.resize((self.ancho_ventana, self.alto_ventana), Image.LANCZOS)
            
            # B. Capa transparente
            overlay = Image.new("RGBA", base_img.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)
            
            # C. DIBUJAR EL RECUADRO (Calculado para 1000x800)
            # Centro X = 500
            # Queremos un cuadro de unos 400px de ancho x 500px de alto
            # X: 500 - 220 = 280  |  500 + 220 = 720
            # Y: Empezar en 150   |  Terminar en 650
            draw.rectangle([(280, 150), (720, 650)], fill=(20, 25, 30, 210), outline=None)
            
            # D. Fuentes (Hice la letra del título un poco más grande)
            try:
                font_title = ImageFont.truetype("arial.ttf", 32) # Título más grande
                font_label = ImageFont.truetype("arial.ttf", 16) # Etiquetas
            except:
                font_title = ImageFont.load_default()
                font_label = ImageFont.load_default()

            # E. Textos (Centrados en X = 500)
            # Título
            draw.text((500, 180), "INICIAR SESIÓN", font=font_title, fill="#FFFFFF", anchor="mt")
            
            # Etiquetas (Calculadas para estar arriba de los Entries)
            # Entry User está en rely 0.40 (~320px) -> Ponemos texto en 290
            draw.text((500, 290), "Usuario", font=font_label, fill="white", anchor="mb")
            
            # Entry Pass está en rely 0.52 (~416px) -> Ponemos texto en 386
            draw.text((500, 386), "Contraseña", font=font_label, fill="white", anchor="mb")

            # F. Fusionar
            final_img = Image.alpha_composite(base_img, overlay)
            return ImageTk.PhotoImage(final_img)

        except Exception as e:
            print(f"Error: {e}")
            bg = Image.new("RGB", (self.ancho_ventana, self.alto_ventana), "#2d3436")
            return ImageTk.PhotoImage(bg)

    def validar_login(self):
        user = self.entry_user.get()
        password = self.entry_pass.get()

        if user == "tigres" and password == "1234":
            self.abrir_menu()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas.\nIntenta: tigres / 1234")

    def abrir_menu(self):
        self.root.destroy() 
        nueva_root = tk.Tk()
        
        # Centrar el menú principal también
        w_menu, h_menu = 900, 700
        x = nueva_root.winfo_screenwidth() // 2 - w_menu // 2
        y = nueva_root.winfo_screenheight() // 2 - h_menu // 2
        nueva_root.geometry(f"{w_menu}x{h_menu}+{x}+{y}")
        
        app = ProyectoFinalUI(nueva_root)
        nueva_root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    # Centrar la ventana de login (1000x800) en tu pantalla
    w, h = 1000, 800
    x = root.winfo_screenwidth() // 2 - w // 2
    y = root.winfo_screenheight() // 2 - h // 2
    root.geometry(f"{w}x{h}+{x}+{y}")
    
    app = LoginApp(root)
    root.mainloop()