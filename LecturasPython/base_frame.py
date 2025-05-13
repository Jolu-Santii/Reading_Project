import customtkinter
from PIL import Image, ImageTk
from tkinter import Canvas
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import os
import datetime


class BaseFrame(customtkinter.CTkFrame):
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
            text="Inicio",
            command=lambda: self.show_frame("inicio")
        )
        self.reportes.configure(command=lambda: self.show_frame("reportes"))

    def create_top_rectangle(self):
        """Crea el rectángulo superior morado con la línea decorativa"""
        self.rectangulo = customtkinter.CTkCanvas(
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
    
    def create_button_frame(self):
        """Crea el frame que contendrá los botones principales"""
        self.frame_botones = customtkinter.CTkFrame(self, fg_color="transparent")
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
        self.completados = customtkinter.CTkButton(
            self.frame_botones, 
            width=250, 
            height=50, 
            corner_radius=20, 
            fg_color="Blue", 
            hover_color="#188fed", 
            font=("Montserrat", 22), 
            text="Completados", 
            command=lambda: self.show_frame("completados")
        )
        self.completados.grid(row=0, column=0, padx=(self.width/6)-125, pady=40)
        
        # Botón Ejercicios
        self.ejercicios = customtkinter.CTkButton(
            self.frame_botones, 
            width=250, 
            height=50, 
            corner_radius=20, 
            fg_color="Green", 
            hover_color="#2dd30c", 
            font=("Montserrat", 22), 
            text="Ejercicios", 
            command=lambda: self.show_frame("ejercicios")
        )
        self.ejercicios.grid(row=0, column=1, padx=(self.width/6)-125, pady=40)
        
        # Botón Reportes
        self.reportes = customtkinter.CTkButton(
            self.frame_botones, 
            width=250, 
            height=50, 
            corner_radius=20, 
            fg_color="Red", 
            hover_color="#fe7272", 
            font=("Montserrat", 22), 
            text="Reportes", 
            command=lambda: self.show_frame("reportes")
        )
        self.reportes.grid(row=0, column=2, padx=(self.width/6)-125, pady=40)

    def crear_grafica_pastel(self, contenedor):
            """Crea y muestra una gráfica de pastel con los resultados"""
            try:
                # Cargar resultados
                with open("resultados/lectura1.json", "r") as f:
                    datos = json.load(f)
                
                aciertos = datos["aciertos"]
                errores = datos["total"] - datos["aciertos"]
                
                # Crear figura
                fig, ax = plt.subplots(figsize=(5, 5), facecolor='#f0f0f0')
                
                # Datos y colores
                sizes = [aciertos, errores]
                labels = ['Correctas', 'Incorrectas']
                colors = ['#4CAF50', '#F44336']
                explode = (0.1, 0)  # Resaltar las correctas
                
                # Crear gráfica
                ax.pie(sizes, explode=explode, labels=labels, colors=colors,
                    autopct='%1.1f%%', shadow=True, startangle=90)
                ax.axis('equal')  # Aspecto circular
                ax.set_title('Resultados del Cuestionario', pad=20)
                
                # Mostrar en TKinter
                canvas = FigureCanvasTkAgg(fig, master=contenedor)
                canvas.draw()
                canvas.get_tk_widget().pack(side="top", fill="both", expand=True, padx=20, pady=20)
                
                return canvas
            except Exception as e:
                print(f"Error al crear gráfica: {e}")
                label = customtkinter.CTkLabel(
                    contenedor, 
                    text="No hay datos disponibles\nRealiza el cuestionario primero",
                    font=("Arial", 16),
                    text_color="gray"
                )
                label.pack(pady=50)
                return None