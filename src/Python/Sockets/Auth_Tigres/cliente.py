import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os
import sys
import socket
import json

# --- CONFIGURACIÓN DE RED ---
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 65432

# --- UTILIDADES ---
def ruta_recursos(ruta_relativa):
    """ Función compatible con PyInstaller para buscar recursos """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, ruta_relativa)

class LoginClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Acceso - Cliente Remoto")
        self.ancho_ventana = 1000
        self.alto_ventana = 800
        
        # Centrar ventana
        x = (self.root.winfo_screenwidth() // 2) - (self.ancho_ventana // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.alto_ventana // 2)
        self.root.geometry(f"{self.ancho_ventana}x{self.alto_ventana}+{x}+{y}")
        self.root.resizable(False, False)

        # 1. Configurar Fondo
        self.configurar_fondo()

        # 2. Entradas de Texto
        # Usuario
        self.entry_user = tk.Entry(self.root, font=("Segoe UI", 12), justify="center", bg="#dfe6e9", bd=0)
        self.entry_user.place(relx=0.5, rely=0.40, width=280, height=35, anchor="center")
        self.entry_user.focus() # Poner foco inicial aquí

        # Contraseña
        self.entry_pass = tk.Entry(self.root, font=("Segoe UI", 12), justify="center", bg="#dfe6e9", bd=0, show="*")
        self.entry_pass.place(relx=0.5, rely=0.52, width=280, height=35, anchor="center")

        # Vincular la tecla ENTER a la función de login
        self.root.bind('<Return>', lambda event: self.solicitar_login())

        # 3. Botón (Simplificado para no depender de mainMenu)
        # Usamos un botón estándar pero estilizado para que se vea bien
        self.btn_login = tk.Button(
            self.root, 
            text="INGRESAR", 
            font=("Segoe UI", 12, "bold"),
            bg="#005DAB", 
            fg="white", 
            activebackground="#003366", 
            activeforeground="white",
            bd=0,
            cursor="hand2",
            command=self.solicitar_login
        )
        self.btn_login.place(relx=0.5, rely=0.65, width=280, height=50, anchor="center")

    def configurar_fondo(self):
        """ Maneja la carga de imagen y el dibujo del panel semitransparente """
        ruta_imagen = ruta_recursos("p.png")
        
        # Fallback si no está en la raíz, buscar en carpetas comunes
        if not os.path.exists(ruta_imagen):
            posibles = [os.path.join("src", "images", "p.png"), "p.png"]
            for p in posibles:
                if os.path.exists(p):
                    ruta_imagen = p
                    break

        try:
            # A. Cargar Imagen Base
            base_img = Image.open(ruta_imagen).convert("RGBA")
            base_img = base_img.resize((self.ancho_ventana, self.alto_ventana), Image.Resampling.LANCZOS)
            
            # B. Crear Capa de Superposición (Overlay)
            overlay = Image.new("RGBA", base_img.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)
            
            # C. Dibujar Rectángulo Semitransparente
            # Coordenadas ajustadas para centrar el panel de login
            draw.rectangle([(280, 150), (720, 650)], fill=(20, 25, 30, 210), outline=None)
            
            # D. Textos en la imagen
            try:
                font_title = ImageFont.truetype("arial.ttf", 32)
                font_label = ImageFont.truetype("arial.ttf", 16)
            except:
                font_title = ImageFont.load_default()
                font_label = ImageFont.load_default()

            draw.text((500, 180), "INICIAR SESIÓN", font=font_title, fill="#FFFFFF", anchor="mt")
            draw.text((500, 360), "Usuario", font=font_label, fill="white", anchor="mb") # Ajustado posición label
            draw.text((500, 456), "Contraseña", font=font_label, fill="white", anchor="mb") # Ajustado posición label

            # E. Fusionar
            final_img = Image.alpha_composite(base_img, overlay)
            self.bg_photo = ImageTk.PhotoImage(final_img)
            
            bg_label = tk.Label(self.root, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        except Exception as e:
            print(f"No se pudo cargar la imagen 'p.png': {e}")
            self.root.configure(bg="#2d3436") # Fondo gris oscuro si falla

    def solicitar_login(self):
        """ Se conecta al servidor para validar credenciales """
        usuario = self.entry_user.get()
        password = self.entry_pass.get()

        if not usuario or not password:
            messagebox.showwarning("Datos incompletos", "Por favor ingresa usuario y contraseña.")
            return

        payload = {
            "user": usuario,
            "pass": password
        }

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(3) # Timeout de 3 segundos
                s.connect((SERVER_HOST, SERVER_PORT))
                
                # Enviar JSON
                s.sendall(json.dumps(payload).encode('utf-8'))
                
                # Recibir respuesta
                response_data = s.recv(1024).decode('utf-8')
                response = json.loads(response_data)

                if response.get("status") == "ok":
                    messagebox.showinfo("Éxito", f"Bienvenido, {usuario}.\nAcceso Correcto.")
                    # AQUÍ TERMINA EL PROGRAMA (No abre nada más, como pediste)
                    self.root.quit() 
                else:
                    messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
                    self.entry_pass.delete(0, tk.END)

        except ConnectionRefusedError:
            messagebox.showerror("Error de Conexión", "No se encontró el servidor de autenticación.")
        except socket.timeout:
            messagebox.showerror("Timeout", "El servidor tardó mucho en responder.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginClient(root)
    root.mainloop()