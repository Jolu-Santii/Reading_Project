# reportes.py
import customtkinter
from base_frame import BaseFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import json

class ReportesFrame(BaseFrame):
    def __init__(self, master, show_frame_callback):
        super().__init__(master, show_frame_callback)

        # Configuración del layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Título
        self.titulo = customtkinter.CTkLabel(
            self,
            text="Reporte de Resultados",
            font=("Montserrat", 24, "bold"),
            text_color="#931ea0"
        )
        self.titulo.grid(row=1, column=0, pady=(20, 10), sticky="n")

        # Contenedor para la gráfica
        self.contenedor_grafica = customtkinter.CTkFrame(self, fg_color="white")
        self.contenedor_grafica.grid(
            row=2, column=0, 
            padx=50, pady=(0, 50), 
            sticky="nsew"
        )

        # Inicializar canvas
        self.canvas = None

        # Mostrar gráfica
        self.actualizar_grafica()

        # Botón para actualizar
        self.actualizar_btn = customtkinter.CTkButton(
            self,
            text="Actualizar Gráfica",
            command=self.actualizar_grafica,
            font=("Montserrat", 16),
            fg_color="#931ea0",
            hover_color="#7a1a85",
            width=200,
            height=40
        )
        self.actualizar_btn.grid(row=3, column=0, pady=(0, 20))

    def actualizar_grafica(self):
        """Actualiza la gráfica con los últimos datos"""

        # Limpiar contenedor (gráfica o mensaje anterior)
        for widget in self.contenedor_grafica.winfo_children():
            widget.destroy()

        datos = self.leer_datos()
        if datos:
            aciertos = datos["aciertos"]
            errores = datos["total"] - aciertos
            etiquetas = ["Correctas", "Incorrectas"]
            valores = [aciertos, errores]
            colores = ["#66bb6a", "#ef5350"]

            fig, ax = plt.subplots(figsize=(5, 5))
            ax.pie(valores, labels=etiquetas, colors=colores, autopct="%1.1f%%", startangle=90)
            ax.axis("equal")  # Para que sea circular

            self.canvas = FigureCanvasTkAgg(fig, master=self.contenedor_grafica)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(expand=True, fill="both")
        else:
            aviso = customtkinter.CTkLabel(
                self.contenedor_grafica, 
                text="No hay resultados aún.\nResponde una encuesta para generar el reporte.",
                font=("Montserrat", 18),
                text_color="gray"
            )
            aviso.pack(pady=40)


    def leer_datos(self):
        """Lee los resultados desde el archivo JSON"""
        ruta = "resultados/lectura1.json"
        if os.path.exists(ruta):
            with open(ruta, "r") as f:
                return json.load(f)
        else:
            return None
