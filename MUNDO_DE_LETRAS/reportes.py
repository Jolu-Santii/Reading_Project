import customtkinter
import fitz
from base_frame import BaseFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os
import json
import shutil
from PIL import Image
import tkinter as tk
from tkinter import Scrollbar
from PIL import Image, ImageTk
from pathlib import Path


class ReportesFrame(BaseFrame):
    def __init__(self, master, show_frame_callback):
        super().__init__(master, show_frame_callback)

        self.pdf_path = "reporte/reporte_actual.pdf"
        self.imagenes_graficas_dir = "reporte/graficas"
        
        self.mensaje_descarga = None
        # Variables para controlar el visor de PDF
        self.current_page = 0
        self.total_pages = 0
        self.doc = None
        self.pdf_container = None
        
        # Configuración del frame principal
        self.frame_pdf = customtkinter.CTkFrame(self, fg_color="white")
        self.frame_pdf.grid(row=1, column=0, sticky="nsew", padx=40, pady=(120, 20))
        self.frame_pdf.configure(width=int(self.width * 0.6), height=int(self.height * 0.55))
        self.frame_pdf.grid_propagate(False)

    def on_show(self):
        """Método que se ejecuta cuando se muestra el frame de Reportes"""
        self.limpiar_frame_pdf()  # Limpiar completamente el frame primero
        self.generar_pdf()
        self.mostrar_pdf_embed()
        self.update_main_buttons()

    def limpiar_frame_pdf(self):
        """Limpia completamente todos los widgets del frame_pdf"""
        for widget in self.frame_pdf.winfo_children():
            widget.destroy()
        
        # Cerrar cualquier documento PDF abierto
        if hasattr(self, 'doc') and self.doc:
            self.doc.close()
            self.doc = None

    def limpiar_archivos(self):
        """Elimina archivos de reportes anteriores"""
        if os.path.exists("reporte"):
            shutil.rmtree("reporte")
        os.makedirs(self.imagenes_graficas_dir, exist_ok=True)

    def generar_pdf(self):
        json_dir = "respuestas"  # Cambia esta ruta si tienes otra carpeta
        archivos = [f for f in os.listdir(json_dir) if f.endswith(".json")]

        total_correctas = 0
        total_incorrectas = 0
        total_preguntas = 0
        datos_individuales = []

        for archivo in archivos:
            with open(os.path.join(json_dir, archivo), "r", encoding="utf-8") as f:
                data = json.load(f)[0]
                correctas = data["puntaje"]
                total = len(data["respuestas"])
                incorrectas = total - correctas
                total_correctas += correctas
                total_incorrectas += incorrectas
                total_preguntas += total
                datos_individuales.append((data["titulo"][0], correctas, incorrectas))

        total_lecturas = len(archivos)

        os.makedirs(os.path.dirname(self.pdf_path), exist_ok=True)
        with PdfPages(self.pdf_path) as pdf_out:
            # Gráfica resumen general de barras con totales
            fig, ax = plt.subplots(figsize=(7, 5))
            barras = ax.bar(
                ["Correctas", "Incorrectas"], 
                [total_correctas, total_incorrectas], 
                color=["green", "red"]
            )

            # TEXTO DE TOTALES ARRIBA DEL TÍTULO
            ax.text(
                0.5, 1.15,
                f"Total Lecturas: {total_lecturas}    Total Preguntas: {total_preguntas}",
                ha="center",
                va="top",
                transform=ax.transAxes,
                fontsize=14,
                color="black"
            )

            # TÍTULO DEL GRÁFICO
            ax.set_title("Resumen General de Lecturas", fontsize=14)

            ax.set_ylabel("Cantidad", fontsize=12, color="black")

            # Mostrar cantidad encima de cada barra
            for barra in barras:
                height = barra.get_height()
                ax.annotate(
                    f'{height}',
                    xy=(barra.get_x() + barra.get_width() / 2, height),
                    xytext=(0, 3),  # desplazamiento vertical
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=11
                )

            pdf_out.savefig(fig)
            plt.close(fig)

            
            # Gráficas individuales con cantidad en labels
            for idx, (titulo, correctas, incorrectas) in enumerate(datos_individuales):
                fig, ax = plt.subplots(figsize=(5,5))
                labels = [f"Correctas: {correctas}", f"Incorrectas: {incorrectas}"]
                ax.pie(
                    [correctas, incorrectas],
                    labels=labels,
                    colors=["green", "red"],
                    autopct="%1.1f%%",
                    startangle=90
                )
                ax.set_title(titulo, fontsize=13)
                pdf_out.savefig(fig)
                plt.close(fig)



    def descargar_pdf(self):
        try:
            downloads_path = str(Path.home() / "Downloads")
            destino = os.path.join(downloads_path, "reporte_lecturas.pdf")
            shutil.copyfile(self.pdf_path, destino)

            # Crear ventana emergente centrada
            popup = customtkinter.CTkToplevel(self)
            popup.geometry("300x120")
            popup.title("Descarga completada")
            popup.resizable(False, False)

            # Centrar ventana popup en pantalla
            popup.update_idletasks()
            w = popup.winfo_width()
            h = popup.winfo_height()
            ws = popup.winfo_screenwidth()
            hs = popup.winfo_screenheight()
            x = (ws // 2) - (w // 2)
            y = (hs // 2) - (h // 2)
            popup.geometry(f'{w}x{h}+{x}+{y}')

            label = customtkinter.CTkLabel(
                popup,
                text="PDF descargado correctamente.\nUbicación:\n" + destino,
                justify="center"
            )
            label.pack(pady=15, padx=10)

            btn_ok = customtkinter.CTkButton(popup, text="OK", command=popup.destroy)
            btn_ok.pack(pady=(0, 0))

            popup.grab_set()  # Modal

        except Exception as e:
            print(f"Error al descargar PDF: {e}")





    def mostrar_pdf_embed(self):
        if not os.path.exists(self.pdf_path):
            print(f"Error: Archivo PDF no encontrado en {self.pdf_path}")
            return

        try:
            self.doc = fitz.open(self.pdf_path)
            self.total_pages = len(self.doc)
            self.current_page = 0

            btn_descargar = customtkinter.CTkButton(
                self.frame_pdf,
                text="Descargar PDF",
                fg_color="purple",  
                hover_color="purple",
                text_color="white",
                command=self.descargar_pdf
            )
            btn_descargar.pack(pady=(15, 0))

            self.pdf_container = customtkinter.CTkFrame(self.frame_pdf, fg_color="white")
            self.pdf_container.pack(fill="both", expand=True, padx=350, pady=10)


            controls_frame = customtkinter.CTkFrame(self.pdf_container, fg_color="white")
            controls_frame.pack(fill="x", pady=5)

            prev_btn = customtkinter.CTkButton(
                controls_frame,
                text="< Anterior",
                command=lambda: self.show_page(-1),
                width=100
            )
            prev_btn.pack(side="left", padx=10)

            self.page_label = customtkinter.CTkLabel(
                controls_frame,
                text=f"Página {self.current_page + 1} de {self.total_pages}",
                text_color="black"
            )
            self.page_label.pack(side="left", expand=True)

            next_btn = customtkinter.CTkButton(
                controls_frame,
                text="Siguiente >",
                command=lambda: self.show_page(1),
                width=100
            )
            next_btn.pack(side="right", padx=10)

            # === Canvas con Scrollbar para mostrar la imagen ===
            self.canvas_frame = customtkinter.CTkFrame(self.pdf_container, fg_color="white")
            self.canvas_frame.pack(fill="both", expand=True)

            self.canvas = tk.Canvas(self.canvas_frame, background="white")
            self.canvas.pack(side="left", fill="both", expand=True)

            self.image_container = self.canvas.create_window((0, 0), window=tk.Label(self.canvas, bg="white"), anchor="nw")

            self.canvas.bind("<Configure>", self.resize_canvas)

            # Mostrar primera página
            self.show_page(0)

        except Exception as e:
            print(f"Error al mostrar PDF: {e}")
            error_label = customtkinter.CTkLabel(
                self.frame_pdf,
                text=f"No se pudo cargar el PDF\nError: {str(e)}",
                text_color="red"
            )
            error_label.pack()

    def resize_canvas(self, event):
        self.canvas.itemconfig(self.image_container, width=event.width)


    def show_page(self, delta=0):
        if not self.doc:
            return

        self.current_page += delta
        self.current_page = max(0, min(self.current_page, self.total_pages - 1))

        page = self.doc.load_page(self.current_page)
        zoom = 1.8
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)

        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        self.tk_img = ImageTk.PhotoImage(img)  # importante mantener referencia

        label = self.canvas.nametowidget(self.canvas.itemcget(self.image_container, "window"))
        label.configure(image=self.tk_img)
        label.image = self.tk_img
        label.configure(width=pix.width, height=pix.height)

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.page_label.configure(text=f"Página {self.current_page + 1} de {self.total_pages}")

    def update_main_buttons(self):
        # Ocultar el botón Reportes porque ya estás en reportes
        
        """Actualiza los botones principales para esta vista específica"""
        # Botón Completados (normal)
        self.completados.configure(
            fg_color="Blue",
            hover_color="#188fed",
            text="Completados ✅",
            command=lambda: self.show_frame("completados")
        )
        
        # Botón Ejercicios (normal)
        self.ejercicios.configure(
            fg_color="Green",
            hover_color="#2dd30c",
            text="Ejercicios 📚",
            command=lambda: self.show_frame("ejercicios")
        )
        
        # Botón Reportes (ahora será naranja y dirá "Inicio")
        self.reportes.configure(
            fg_color="Orange", 
            hover_color="#FF8C00",
            text="Inicio 🏠",
            command=lambda: self.show_frame("inicio")
        )

    def cambiar_frame(self, destino):
        """Cambia a otro frame"""
        self.limpiar_frame_pdf()  # Limpiar antes de cambiar
        self.show_frame(destino)


        #####
        ###
        ##
        #YA QUEDO ESTE PDF
        ###
        ##