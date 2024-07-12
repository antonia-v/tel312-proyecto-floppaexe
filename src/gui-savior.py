import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageSequence
import os
from floppasaviour import *

class InstallerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Floppa uninstaller")
        self.geometry("800x600")
        
        self.step = 0
        self.steps = [
            ("Bienvenido", self.welcome_step),
            ("¡Tus archivos han sido recuperados por floppasaviour.exe!", self.recovery_step)
        ]
        
        self.create_widgets()

        # Obtén la ruta del directorio donde se encuentra el script actual
        self.script_directory = os.path.dirname(os.path.abspath(__file__))

        # Ruta al archivo de imagen floppajesus.png
        self.image_path = os.path.join(self.script_directory, "floppajesus.png")

    def create_widgets(self):
        self.header_label = ttk.Label(self, text="Recupera tus archivos", font=("Helvetica", 16))
        self.header_label.pack(pady=20)
        
        self.content_frame = ttk.Frame(self)
        self.content_frame.pack(expand=True, fill=tk.BOTH)
        
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(fill=tk.X)
        
        self.back_button = ttk.Button(self.button_frame, text="Atrás", command=self.prev_step, state=tk.DISABLED)
        self.back_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.next_button = ttk.Button(self.button_frame, text="Siguiente", command=self.next_step)
        self.next_button.pack(side=tk.RIGHT, padx=5, pady=5)
        
        self.steps[self.step][1]()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def welcome_step(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="Haga clic en 'Siguiente' para recuperar sus archivos.").pack(pady=10)
    
    def recovery_step(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="¡Tus archivos han sido recuperados por floppasaviour.exe!").pack(pady=10)
        
        # Cargar y mostrar la imagen recuperada
        self.gif = Image.open(self.image_path)
        width, height = 600, 400  # Ajusta el tamaño deseado
        self.gif = self.gif.resize((width, height))
        self.frame = ImageTk.PhotoImage(self.gif.copy().convert("RGBA"))
        self.gif_label = ttk.Label(self.content_frame)
        self.gif_label.pack(pady=10)
        self.gif_label.configure(image=self.frame)

        self.next_button.config(text="Adiós", command=self.quit)
    
    def prev_step(self):
        if self.step > 0:
            self.step -= 1
            self.steps[self.step][1]()
            self.header_label.config(text=self.steps[self.step][0])
        if self.step == 0:
            self.back_button.config(state=tk.DISABLED)
        self.next_button.config(text="Siguiente", command=self.next_step)
    
    def next_step(self):
        if self.step < len(self.steps) - 1:
            self.step += 1
            self.steps[self.step][1]()
            self.header_label.config(text=self.steps[self.step][0])
            restore()  # Llama a la función para desencriptar
        if self.step > 0:
            self.back_button.config(state=tk.NORMAL)
        if self.step == len(self.steps) - 1:
            self.back_button.config(state=tk.DISABLED)
            self.next_button.config(text="Adiós", command=self.quit)

if __name__ == "__main__":
    app = InstallerApp()
    app.mainloop()