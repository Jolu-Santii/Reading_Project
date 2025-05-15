import customtkinter
import json
import os
from tkinter import messagebox
from base_frame import BaseFrame
from PIL import Image, ImageTk


class CompletadosFrame(BaseFrame):
    def __init__(self, master, show_frame_callback):
        super().__init__(master, show_frame_callback)
        self.master = master
        self.show_frame = show_frame_callback
        self.configure(fg_color="white")
        
        # Configurar el grid principal
        self.grid_columnconfigure(0, weight=0)  
        self.grid_columnconfigure(1, weight=1) 
        self.grid_rowconfigure(1, weight=1)
        
        # Actualizar botones principales
        self.update_main_buttons()
        
        # Cargar imagen estática (solo una vez)
        self.mostrar_imagen()
        
        self.titulo_fijo = customtkinter.CTkLabel(
            self,
            text="EJERCICIOS COMPLETADOS",
            font=("Montserrat", 28, "bold"),
            text_color="#931ea0"
        )
        self.titulo_fijo.grid(row=1, column=1, pady=(130, 0), padx=(0, 20), sticky="n")

        # Frame scrollable para resultados
        self.resultados_frame = customtkinter.CTkScrollableFrame(
            self, 
            fg_color="white",
            scrollbar_button_color="#931ea0",
            scrollbar_button_hover_color="#7a1a85"
        )
        self.resultados_frame.grid(row=1, column=1, padx=(0, 20), pady=(180, 220), sticky="nsew")
        self.resultados_frame.grid_columnconfigure(0, weight=1)
          
    def on_show(self):
        """Se ejecuta cada vez que se muestra el frame"""
        # Limpiar resultados anteriores
        for widget in self.resultados_frame.winfo_children():
            widget.destroy()
            
        # Mostrar mensaje de carga
        self.loading_label = customtkinter.CTkLabel(
            self.resultados_frame, 
            text="Cargando ejercicios completados...",
            font=("Montserrat", 16)
        )
        self.loading_label.grid(row=0, column=0, pady=20)
        
        # Forzar actualización de la UI
        self.update()
        
        # Cargar resultados después de mostrar la UI
        self.after(100, self.cargar_resultados_async)

    def cargar_resultados_async(self):
        """Carga los resultados de forma asíncrona"""
        try:
            self.loading_label.destroy()
            self.cargar_resultados()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los resultados: {str(e)}")
        
    def mostrar_imagen(self):
        """Muestra la imagen estática en el lado izquierdo (solo una vez)"""
        try:
            nota_img = Image.open("recursos/nota.png")
            nota_img = nota_img.resize((550, 600))
            self.tk_nota = ImageTk.PhotoImage(nota_img)
            
            img_frame = customtkinter.CTkFrame(
                self, 
                fg_color="white",
                width=650,
                corner_radius=0
            )
            img_frame.grid(row=1, column=0, sticky="nswe", padx=(80, 0), pady=130)
            img_frame.grid_propagate(False)
            
            img_label = customtkinter.CTkLabel(
                img_frame, 
                image=self.tk_nota, 
                text="",
                fg_color="white"
            )
            img_label.pack(expand=True, pady=20, fill="both")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen: {str(e)}")
            customtkinter.CTkFrame(
                self, 
                fg_color="white",
                width=200
            ).grid(row=1, column=0, sticky="nswe")

    def update_main_buttons(self):
        """Actualiza los botones principales"""
        self.completados.configure(
            fg_color="Orange", 
            hover_color="#FF8C00",
            text="Inicio 🏠",
            command=lambda: self.show_frame("inicio")
        )
        
        self.ejercicios.configure(
            fg_color="Green",
            hover_color="#2dd30c",
            text="Ejercicios 📚",
            command=lambda: self.show_frame("ejercicios")
        )
        
        self.reportes.configure(
            fg_color="Red",
            hover_color="#fe7272",
            text="Reportes 📊",
            command=lambda: self.show_frame("reportes")
        )
    
    def cargar_resultados(self):
        """Carga los archivos JSON de respuestas"""
        # Verificar si existe la carpeta de respuestas
        if not os.path.exists("respuestas"):
            self.mostrar_mensaje_vacio()
            return
        
        archivos = [f for f in os.listdir("respuestas") if f.endswith('.json')]
        
        if not archivos:
            self.mostrar_mensaje_vacio()
            return
        
        # Lista de colores para los frames
        colores = ["#4CAF50", "#2196F3", "#9C27B0", "#FF9800", "#607D8B", "#E91E63"]
        
        # Procesar cada archivo JSON
        for i, archivo in enumerate(archivos, start=1):
            try:
                with open(os.path.join("respuestas", archivo), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                for ejercicio in data:
                    color = colores[i % len(colores)]
                    
                    frame_ejercicio = customtkinter.CTkFrame(
                        self.resultados_frame, 
                        fg_color=color,
                        corner_radius=25,
                        height=55,
                    )
                    frame_ejercicio.grid(row=i, column=0, pady=5, padx=(150, 150), sticky="ew")
                    frame_ejercicio.grid_propagate(False)
                    
                    frame_ejercicio.grid_rowconfigure(0, weight=1)
                    frame_ejercicio.grid_columnconfigure(0, weight=1)
                    frame_ejercicio.grid_columnconfigure(1, weight=1)
                    
                    content_frame = customtkinter.CTkFrame(frame_ejercicio, fg_color="transparent")
                    content_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
                    content_frame.grid_rowconfigure(0, weight=1)
                    content_frame.grid_columnconfigure(0, weight=1)
                    content_frame.grid_columnconfigure(1, weight=1)
                    
                    titulo_lectura = ejercicio.get('titulo', ['Sin título'])[0]
                    puntaje = ejercicio.get('puntaje', 0)
                    
                    label_titulo = customtkinter.CTkLabel(
                        content_frame,
                        text=f"{titulo_lectura}",
                        font=("Montserrat", 16),
                        text_color="white",
                        anchor="w"
                    )
                    label_titulo.grid(row=0, column=0, padx=20, sticky="w")
                    
                    label_puntaje = customtkinter.CTkLabel(
                        content_frame,
                        text=f"Puntaje: {puntaje}/5",
                        font=("Montserrat", 16),
                        text_color="white",
                    )
                    label_puntaje.grid(row=0, column=1, padx=20, sticky="e")
                    
            except Exception as e:
                print(f"Error al procesar {archivo}: {str(e)}")
                
        # Ajustar el scroll al inicio
        self.resultados_frame._parent_canvas.yview_moveto(0)
    
    def mostrar_mensaje_vacio(self):
        """Muestra mensaje cuando no hay ejercicios completados"""
        label = customtkinter.CTkLabel(
            self.resultados_frame, 
            text="No hay ejercicios completados aún",
            font=("Montserrat", 20),
            text_color="black"
        )
        label.grid(row=0, column=0, pady=20)