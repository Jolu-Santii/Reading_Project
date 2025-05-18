import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import Canvas
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import os
import datetime


class BaseFrame(ctk.CTkFrame):
    def __init__(self, master, show_frame_callback):
        super().__init__(master)
        self.master = master
        self.show_frame = show_frame_callback
        self.width = self.master.winfo_screenwidth()
        self.height = self.master.winfo_screenheight()
        
        self.configure(fg_color="white")
        
        # Configuración básica del grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Crear rectángulo superior
        self.create_top_rectangle()
        
        # Crear frame para botones
        self.create_button_frame()

    def update_main_buttons(self):
        """Actualiza los botones principales para esta vista específica"""
        self.completados.configure(command=lambda: self.show_frame("completados"))
        self.ejercicios.configure(
            fg_color="Orange", 
            hover_color="#FF8C00",
            text="Inicio 🏠",
            command=lambda: self.show_frame("inicio")
        )
        self.reportes.configure(command=lambda: self.show_frame("reportes"))

    def create_top_rectangle(self):
        """Crea el rectángulo superior morado con la línea decorativa y agrega el ícono y el título"""
        self.rectangulo = ctk.CTkCanvas(
            self, 
            width=self.width+400, 
            height=(self.height/9), 
            bg="#931ea0", 
            highlightthickness=0
        )
        self.rectangulo.grid(row=0, column=0, columnspan=3, sticky="nsew")
        self.rectangulo.create_rectangle(
            0, (self.height/9)+10, 
            self.width+400, (self.height/9)-5, 
            fill="#cbbecc", 
            outline="#cbbecc"
        )

        # Cargar el ícono
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            logo_path = os.path.join(base_dir, "recursos", "book.png")
            if not os.path.exists(logo_path):
                raise FileNotFoundError(f"No se encontró el archivo: {logo_path}")
            
            logo_img = Image.open(logo_path).resize((50, 50))
            logo = ImageTk.PhotoImage(logo_img)  # ✅ volver a usar PhotoImage aquí
            logo = ImageTk.PhotoImage(logo_img)
        except Exception as e:
            print(f"Error al cargar el ícono: {e}")
            logo = None  # Si no se puede cargar el ícono, lo dejamos como None

        if logo:
            self.rectangulo.create_image(75, (self.height/9)/2, image=logo, anchor="w")
            self.rectangulo.image = logo  # Mantener una referencia para evitar que se elimine

        self.rectangulo.create_text(
            140, (self.height/9)/2, 
            text="MUNDO DE LETRAS", 
            font=("Montserrat", 27, "bold"), 
            fill="white", 
            anchor="w"
        )

    def create_button_frame(self):
        """Crea el frame que contendrá los botones principales"""
        self.frame_botones = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botones.grid(row=1, column=0, columnspan=3, sticky="nsew")
        
        # Configurar grid del frame de botones
        self.frame_botones.grid_columnconfigure(0, weight=1)
        self.frame_botones.grid_columnconfigure(1, weight=1)
        self.frame_botones.grid_columnconfigure(2, weight=1)
        
        # Crear botones principales
        self.create_main_buttons()
    
    def create_main_buttons(self):
        """Crea los botones principales (completados, ejercicios, reportes)"""
        # Botón Completados
        self.completados = ctk.CTkButton(
            self.frame_botones, 
            width=250, 
            height=50, 
            corner_radius=20, 
            fg_color="Blue", 
            hover_color="#188fed", 
            font=("Montserrat", 22), 
            text="Completados ✅", 
            command=lambda: self.show_frame("completados")
        )
        self.completados.grid(row=0, column=0, padx=(self.width/6)-125, pady=40)
        
        # Botón Ejercicios
        self.ejercicios = ctk.CTkButton(
            self.frame_botones, 
            width=250, 
            height=50, 
            corner_radius=20, 
            fg_color="Green", 
            hover_color="#2dd30c", 
            font=("Montserrat", 22), 
            text="Ejercicios 📚", 
            command=lambda: self.show_frame("ejercicios")
        )
        self.ejercicios.grid(row=0, column=1, padx=(self.width/6)-125, pady=40)
        
        # Botón Reportes
        self.reportes = ctk.CTkButton(
            self.frame_botones, 
            width=250, 
            height=50, 
            corner_radius=20, 
            fg_color="Red", 
            hover_color="#fe7272", 
            font=("Montserrat", 22), 
            text="Reportes 📊", 
            command=lambda: self.show_frame("reportes")
        )
        self.reportes.grid(row=0, column=2, padx=(self.width/6)-125, pady=40)

   