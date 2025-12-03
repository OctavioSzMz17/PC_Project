import sys
import os
import shutil
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import fitz  # PyMuPDF
from PIL import Image, ImageTk  # Necesario: pip install pillow

class PDFViewer:
    def __init__(self, root, pdf_path):
        self.root = root
        self.pdf_path = pdf_path
        
        # Validar ruta
        if not os.path.exists(pdf_path):
            messagebox.showerror("Error", f"No se encontró el archivo:\n{pdf_path}")
            root.destroy()
            return

        # Configuración de ventana
        self.root.title(f"Visor PDF - {os.path.basename(pdf_path)}")
        self.root.geometry("900x700")

        # --- BARRA DE HERRAMIENTAS SUPERIOR ---
        self.toolbar = tk.Frame(root, bd=1, relief=tk.RAISED, bg="#e0e0e0")
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        # Botones
        estilo_btn = {"padx": 10, "pady": 5, "bg": "#2c3e50", "fg": "white", "font": ("Arial", 10, "bold")}
        
        btn_print = tk.Button(self.toolbar, text="🖨️ Imprimir", command=self.print_pdf, **estilo_btn)
        btn_print.pack(side=tk.LEFT, padx=5, pady=5)

        btn_download = tk.Button(self.toolbar, text="💾 Descargar", command=self.download_pdf, **estilo_btn)
        btn_download.pack(side=tk.LEFT, padx=5, pady=5)

        btn_exit = tk.Button(self.toolbar, text="🚪 Salir", command=root.destroy, bg="#c0392b", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5)
        btn_exit.pack(side=tk.RIGHT, padx=5, pady=5)

        # --- ÁREA PRINCIPAL CON SCROLL ---
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Scrollbar Vertical
        self.v_scroll = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL)
        self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Canvas para dibujar las imágenes del PDF
        self.canvas = tk.Canvas(self.main_frame, bg="#505050", yscrollcommand=self.v_scroll.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.v_scroll.config(command=self.canvas.yview)

        # Configurar el scroll con la rueda del mouse
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # --- RENDERIZADO DEL PDF ---
        self.images_ref = []  # Referencia para evitar que el Garbage Collector borre las imágenes
        self.render_pdf()

    def render_pdf(self):
        """Convierte las páginas del PDF a imágenes y las pone en el Canvas"""
        try:
            doc = fitz.open(self.pdf_path)
            y_offset = 20 # Espacio inicial

            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                
                # Aumentamos el zoom para mejor calidad (matrix=2)
                mat = fitz.Matrix(1.5, 1.5)
                pix = page.get_pixmap(matrix=mat)

                # Convertir a imagen compatible con Tkinter
                img_pil = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                img_tk = ImageTk.PhotoImage(img_pil)

                # Guardar referencia
                self.images_ref.append(img_tk)

                # Dibujar en el canvas (centrado horizontalmente)
                canvas_width = 900 # Estimado inicial
                x_pos = max(20, (canvas_width - pix.width) // 2)
                
                self.canvas.create_image(450, y_offset, image=img_tk, anchor=tk.N)
                
                # Añadir un borde o espacio entre páginas
                y_offset += pix.height + 20
            
            # Actualizar la región de scroll para que abarque todo
            self.canvas.config(scrollregion=(0, 0, 900, y_offset))

        except Exception as e:
            messagebox.showerror("Error de Renderizado", f"No se pudo leer el PDF: {e}")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def download_pdf(self):
        """Permite al usuario guardar una copia del PDF en otra ruta"""
        save_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=os.path.basename(self.pdf_path),
            title="Guardar copia como..."
        )
        if save_path:
            try:
                shutil.copy(self.pdf_path, save_path)
                messagebox.showinfo("Éxito", "Archivo guardado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar: {e}")

    def print_pdf(self):
        """Manda a imprimir usando el sistema operativo"""
        try:
            if sys.platform == "win32":
                os.startfile(self.pdf_path, "print")
            else:
                # Linux/Mac (comando genérico, puede variar según distro)
                import subprocess
                subprocess.run(["lp", self.pdf_path])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo enviar a imprimir: {e}")

if __name__ == "__main__":
    # Verificamos si nos enviaron la ruta como argumento
    if len(sys.argv) > 1:
        ruta_recibida = sys.argv[1]
    else:
        # Ruta de prueba por si ejecutas el archivo solo
        ruta_recibida = "ejemplo.pdf" 

    root = tk.Tk()
    app = PDFViewer(root, ruta_recibida)
    root.mainloop()