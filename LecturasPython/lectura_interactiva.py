import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import subprocess
from base_frame import BaseFrame
from  inicio import InicioFrame
import json
import os

class LecturaInteractiva:
    def __init__(self, master, titulo, lectura_path, preguntas_path, imagen_path=None, volver_func=None):
        self.master = master
        self.titulo = titulo
        self.lectura_path = lectura_path
        self.preguntas_path = preguntas_path
        self.imagen_path = imagen_path
        self.callback_volver = volver_func 
        self.preguntas = []
        self.puntaje = 0
        self.pregunta_actual = 0
        self.respuestas_elegidas = []  
        self.cargar_datos()
        self.construir_interfaz()

    def cargar_datos(self):
        with open(self.lectura_path, encoding="utf-8") as f:
            self.lectura = f.read()
        with open(self.preguntas_path, encoding="utf-8") as f:
            self.preguntas = json.load(f)

    def construir_interfaz(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.master.configure(fg_color="white")
        self.master.grid_rowconfigure((0,1,2,3,4,5,6), weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.mensaje_label = ctk.CTkLabel(self.master, text=self.titulo,
                                 font=("Comic Sans MS", 18, "italic"),
                                 text_color="darkred")
        self.mensaje_label.grid(row=0, column=0, pady=(10, 0), sticky="n")

        contenido_frame = ctk.CTkFrame(self.master, fg_color="white")
        contenido_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        contenido_frame.grid_columnconfigure((0, 1), weight=1)
        contenido_frame.grid_rowconfigure(0, weight=1)

        if self.imagen_path and os.path.exists(self.imagen_path):
            try:
                imagen_pil = Image.open(self.imagen_path)
                imagen_ctk = ctk.CTkImage(light_image=imagen_pil, size=(400, 400))
                imagen_label = ctk.CTkLabel(contenido_frame, image=imagen_ctk, text="")
                imagen_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
            except Exception as e:
                print(f"Error al cargar imagen: {e}")
        else:
            imagen_label = ctk.CTkLabel(contenido_frame, text="[Imagen no disponible]", width=400, height=400)
            imagen_label.grid(row=0, column=0, padx=10, pady=10)

        lectura_frame = ctk.CTkFrame(contenido_frame, fg_color="white", corner_radius=8)
        lectura_frame.grid(row=0, column=1, padx=10, pady=15, sticky="nsew")
        lectura_label = ctk.CTkLabel(lectura_frame, text=self.lectura,
                                     font=("Comic Sans MS", 18), justify="center", text_color="black", wraplength=800)
        lectura_label.pack(padx=10, pady=10)

        self.pregunta_label = ctk.CTkLabel(self.master, text="", font=("Comic Sans MS", 18),
                                           justify="left", wraplength=900)
        self.pregunta_label.grid(row=2, column=0, pady=(10, 0))

        self.pista_label = ctk.CTkLabel(self.master, text="", font=("Comic Sans MS", 14, "italic"),
                                        text_color="gray", wraplength=800, justify="center")
        self.pista_label.grid(row=3, column=0, pady=(0, 5))

        self.botones_frame = ctk.CTkFrame(self.master, fg_color="white")
        self.botones_frame.grid(row=4, column=0, pady=10)
        colores = ["#ff9999", "#99ff99", "#9999ff", "#ffff99"]
        hover_colors = ["#e30000", "#00FF00", "#6666ff", "#f0f075"]
        self.botones = []
        for i in range(4):
            b = ctk.CTkButton(self.botones_frame, text="", text_color="black",
                              width=180, height=80, fg_color=colores[i], hover_color=hover_colors[i],
                              corner_radius=10, command=lambda i=i: self.verificar_respuesta(i))
            b.grid(row=0, column=i, padx=10)
            self.botones.append(b)

        self.feedback_label = ctk.CTkLabel(self.master, text="", font=("Comic Sans MS", 14),
                                           text_color="blue", wraplength=800)
        self.feedback_label.grid(row=5, column=0, pady=(0, 10))

        self.footer_frame = ctk.CTkFrame(self.master, fg_color="white")
        self.footer_frame.grid(row=6, column=0, pady=(0, 10))
        self.footer_frame.grid_columnconfigure(0, weight=1)

        self.frame_progreso = ctk.CTkFrame(self.footer_frame)
        self.frame_progreso.grid(row=0, column=0, pady=10)
        self.progreso = ctk.CTkProgressBar(self.frame_progreso, width=600)
        self.progreso.pack(side="left", padx=10)
        self.progreso.set(0)
        self.progreso_text = ctk.CTkLabel(self.frame_progreso, text="0/5", font=("Comic Sans MS", 18))
        self.progreso_text.pack(side="left", padx=10)

        self.boton_continuar = ctk.CTkButton(self.footer_frame, text="Continuar",
                                             font=("Comic Sans MS", 14), command=self.continuar)
        self.boton_continuar.grid(row=1, column=0, pady=10)

        self.boton_regresar = ctk.CTkButton(self.footer_frame, text="REGRESAR A EJERCICIOS",
                                    font=("Comic Sans MS", 14), fg_color="gray", 
                                    command=self.volver)
        self.boton_regresar.grid(row=2, column=0, pady=(0, 10))


    def mostrar_pregunta(self):
        pregunta = self.preguntas[self.pregunta_actual]
        self.pregunta_label.configure(text=pregunta["pregunta"])
        self.pista_label.configure(text=pregunta.get("pista", ""))
        self.feedback_label.configure(text="")
        for i in range(4):
            self.botones[i].configure(text=pregunta["opciones"][i])
        self.progreso.set(self.pregunta_actual / len(self.preguntas))
        self.progreso_text.configure(text=f"{self.pregunta_actual + 1}/{len(self.preguntas)}")

    def verificar_respuesta(self, indice):
        #self.respuestas_elegidas.append(indice)
        correcta = self.preguntas[self.pregunta_actual]["respuesta"]
        if indice == correcta:
            self.puntaje += 1
            # GUARDAR RESPUESTA COMO CORRECTA, CAMBIALO SI ES ASÍ QUIERES XD
            self.respuestas_elegidas.append(1)
            self.feedback_label.configure(text="¡Respuesta correcta!", text_color="green")
        else:
            # GUARDAR RESPUESTA COMO INCORRECTA
            self.respuestas_elegidas.append(0)
            correcta_txt = self.preguntas[self.pregunta_actual]["opciones"][correcta]
            self.feedback_label.configure(
                text=f"INCORRECTO. \nLa respuesta correcta era: {correcta_txt}", text_color="red"
            )

        self.pregunta_actual += 1
        if self.pregunta_actual < len(self.preguntas) and indice == correcta:
            self.master.after(1350,self.mostrar_pregunta)
        elif self.pregunta_actual < len(self.preguntas):
            self.master.after(2000, self.mostrar_pregunta)
        else:
            self.guardar_respuestas()  # Nuevo
            self.progreso.set(1.0)
            self.progreso_text.configure(text=f"{len(self.preguntas)}/{len(self.preguntas)}")
            self.master.after(1500, lambda: messagebox.showinfo("Resultado", f"Has obtenido {self.puntaje} de {len(self.preguntas)} puntos."))
            self.master.after(2000, self.master.quit)

    def continuar(self):
        self.boton_continuar.grid_remove()
        self.mostrar_pregunta()

    def volver(self):
        self.callback_volver = lambda: self.show_frame("ejercicios")
        if self.callback_volver:
            self.callback_volver()

    def guardar_respuestas(self):
        # Crear la carpeta 'respuestas' si no existe
        carpeta_respuestas = "respuestas"
        os.makedirs(carpeta_respuestas, exist_ok=True)

        # Obtener el nombre base del archivo de lectura
        nombre_lectura = os.path.splitext(os.path.basename(self.lectura_path))[0]  # lectura1.txt → lectura1

        # Construir la ruta completa del archivo de salida dentro de la carpeta 'respuestas'
        archivo_salida = os.path.join(carpeta_respuestas, f"{nombre_lectura}.json")

        # Preparar los datos a guardar
        datos = [
            {
                "Lectura": nombre_lectura,
                "titulo": [self.titulo],
                "respuestas": self.respuestas_elegidas
            }
        ]

        # Guardar el archivo JSON
        with open(archivo_salida, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)

        # Opcional: Mostrar mensaje de confirmación
        print(f"Respuestas guardadas en: {archivo_salida}")


