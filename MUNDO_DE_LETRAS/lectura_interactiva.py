import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import Canvas
import tkinter as tk
import subprocess
import textwrap
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
        
        self._configurar_estilos()
        self.cargar_datos()
        self.construir_interfaz()

    def _configurar_estilos(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        self.master.configure(fg_color="white")

    def cargar_datos(self):
        try:
            with open(self.lectura_path, encoding="utf-8") as f:
                self.lectura = f.read()
            
            with open(self.preguntas_path, encoding="utf-8") as f:
                self.preguntas = json.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los datos: {str(e)}")
            self.lectura = "Contenido no disponible"
            self.preguntas = []

    def construir_interfaz(self):
        self.master.grid_rowconfigure((0,1,2,3,4,5,6), weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self._crear_titulo()
        
        self._crear_frame_contenido()
        
        self._crear_footer()

    def _crear_titulo(self):
        self.mensaje_label = ctk.CTkLabel(
            self.master, 
            text=self.titulo,
            font=("Comic Sans MS", 25, "italic"),
            text_color="darkred"
        )
        self.mensaje_label.grid(row=0, column=0, pady=(10, 0), sticky="n")

    def _crear_frame_contenido(self):
        contenido_frame = ctk.CTkFrame(self.master, fg_color="white")
        contenido_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        contenido_frame.grid_columnconfigure((0, 1), weight=1)
        contenido_frame.grid_rowconfigure(0, weight=1)

        self._crear_imagen(contenido_frame)
        
        self._crear_texto_lectura(contenido_frame)

    def _crear_imagen(self, parent_frame):
        try:
            if self.imagen_path and os.path.exists(self.imagen_path):
                imagen_pil = Image.open(self.imagen_path)
                imagen_ctk = ctk.CTkImage(light_image=imagen_pil, size=(400, 400))
                self.imagen_label = ctk.CTkLabel(
                    parent_frame, 
                    image=imagen_ctk, 
                    text=""
                )
            else:
                self.imagen_label = ctk.CTkLabel(
                    parent_frame, 
                    text="[Imagen no disponible]", 
                    width=400, 
                    height=400
                )
        except Exception as e:
            print(f"Error al cargar imagen: {e}")
            self.imagen_label = ctk.CTkLabel(
                parent_frame, 
                text="[Error cargando imagen]", 
                width=400, 
                height=400
            )
        
        self.imagen_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    def _crear_texto_lectura(self, parent_frame):
        lectura_frame = ctk.CTkFrame(parent_frame, fg_color="white", corner_radius=8)
        lectura_frame.grid(row=0, column=1, padx=10, pady=15, sticky="nsew")
        
        lectura_label = ctk.CTkLabel(
            lectura_frame, 
            text=self.lectura,
            font=("Comic Sans MS", 18), 
            justify="center", 
            text_color="black", 
            wraplength=900
        )
        lectura_label.pack(padx=10, pady=10)

    def _crear_footer(self):
        self.footer_frame = ctk.CTkFrame(self.master, fg_color="white")
        self.footer_frame.grid(row=6, column=0, pady=(0, 10))
        self.footer_frame.grid_columnconfigure(0, weight=1)

        self.boton_continuar = ctk.CTkButton(
            self.footer_frame, 
            text="⏩ CONTINUAR ⏩",
            font=("Comic Sans MS", 20), 
            command=self.continuar
        )
        self.boton_continuar.grid(row=1, column=0, pady=(180, 22))

        self.boton_regresar = ctk.CTkButton(
            self.footer_frame, 
            text="⏪ REGRESAR A EJERCICIOS ⏪",
            font=("Comic Sans MS", 20), 
            fg_color="#931ea0", 
            command=self.volver
        )
        self.boton_regresar.grid(row=2, column=0, pady=(0, 10))

    def continuar(self):
        # Ocultar botón continuar
        self.boton_continuar.grid_remove()
        
        # Configurar elementos de preguntas
        self._configurar_ui_preguntas()
        
        # Mostrar primera pregunta
        self.mostrar_pregunta()

    def _configurar_ui_preguntas(self):
        # Etiqueta de pregunta
        self.pregunta_label = ctk.CTkLabel(
            self.master, 
            text="", 
            font=("Comic Sans MS", 18),
            justify="left", 
            wraplength=900
        )
        self.pregunta_label.grid(row=2, column=0, pady=(5, 5))

        # Frame para botones de opciones
        self.botones_frame = ctk.CTkFrame(self.master, fg_color="white")
        self.botones_frame.grid(row=4, column=0, pady=5)
        
        # Colores originales para botones
        colores = ["#ff9999", "#99ff99", "#9999ff", "#ffff99"]
        hover_colors = ["#e30000", "#00FF00", "#6666ff", "#f0f075"]
        
        # Crear botones de opciones
        self.botones = []
        for i in range(4):
            btn = ctk.CTkButton(
                self.botones_frame, 
                text="", 
                text_color="black",
                width=210, 
                height=80, 
                fg_color=colores[i], 
                hover_color=hover_colors[i],
                corner_radius=10, 
                command=lambda i=i: self.verificar_respuesta(i)
            )
            btn.grid(row=0, column=i, padx=10)
            self.botones.append(btn)

        # Etiqueta de feedback
        self.feedback_label = ctk.CTkLabel(
            self.master, 
            text="", 
            font=("Comic Sans MS", 14), 
            height=45,
            text_color="blue", 
            wraplength=800
        )
        self.feedback_label.grid(row=5, column=0, pady=(10, 5))

        # Barra de progreso
        self._configurar_barra_progreso()

    def _configurar_barra_progreso(self):
        """Configura la barra de progreso (estilo original)"""
        self.frame_progreso = ctk.CTkFrame(self.footer_frame)
        self.frame_progreso.grid(row=0, column=0, pady=10)
        
        self.progreso = ctk.CTkProgressBar(self.frame_progreso, width=600)
        self.progreso.pack(side="left", padx=10)
        self.progreso.set(0)
        
        self.progreso_text = ctk.CTkLabel(
            self.frame_progreso, 
            text="0/5", 
            font=("Comic Sans MS", 18)
        )
        self.progreso_text.pack(side="left", padx=10)

    def mostrar_pregunta(self):  
        if not self.preguntas or self.pregunta_actual >= len(self.preguntas):
            return
            
        pregunta = self.preguntas[self.pregunta_actual]
        self.pregunta_label.configure(text=pregunta["pregunta"])
        self.feedback_label.configure(text="")
        
        # Configurar botones con texto envuelto (original)
        for i in range(4):
            texto_envuelto = "\n".join(textwrap.wrap(pregunta["opciones"][i], width=22))
            self.botones[i].configure(text=texto_envuelto)

        # Actualizar progreso
        self.progreso.set(self.pregunta_actual / len(self.preguntas))
        self.progreso_text.configure(text=f"{self.pregunta_actual + 1}/{len(self.preguntas)}")

    def verificar_respuesta(self, indice):
        if not self.preguntas or self.pregunta_actual >= len(self.preguntas):
            return
            
        self.respuestas_elegidas.append(indice)
        correcta = self.preguntas[self.pregunta_actual]["respuesta"]
        
        if indice == correcta:
            self.puntaje += 1
            self.feedback_label.configure(text="¡Respuesta correcta!", text_color="green")
            delay = 1350
        else:
            correcta_txt = self.preguntas[self.pregunta_actual]["opciones"][correcta]
            self.feedback_label.configure(
                text=f"INCORRECTO. \nLa respuesta correcta era: {correcta_txt}", 
                text_color="red"
            )
            delay = 2000

        self.pregunta_actual += 1

        # Manejar siguiente pregunta o finalización
        if self.pregunta_actual < len(self.preguntas):
            self.master.after(delay, self.mostrar_pregunta)
        else:
            self.progreso.set(self.pregunta_actual / len(self.preguntas))
            self.master.after(delay, self.finalizacion)

    def finalizacion(self):
        self.guardar_respuestas()
  
        # Limpiar interfaz actual
        for widget in self.master.winfo_children():
            widget.destroy()

        # Configurar pantalla de resultados
        self._configurar_pantalla_resultados()

    def _configurar_pantalla_resultados(self):
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        contenido_frame = ctk.CTkFrame(self.master, fg_color="white")
        contenido_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        contenido_frame.grid_columnconfigure((0, 1), weight=1)
        contenido_frame.grid_rowconfigure(0, weight=1)

        self._crear_frame_imagen(contenido_frame)
        
        self._crear_frame_resultados(contenido_frame)

    def _crear_frame_imagen(self, parent_frame):
        imagen_frame = ctk.CTkFrame(parent_frame, fg_color="white")
        imagen_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=(50, 10))
        imagen_frame.grid_rowconfigure(0, weight=1)
        imagen_frame.grid_columnconfigure(0, weight=1)

        try:
            felicitacion_img = Image.open("recursos/ninoSaltando.png")
            felicitacion_ctk_img = ctk.CTkImage(light_image=felicitacion_img, size=(500, 700))
            imagen_label = ctk.CTkLabel(imagen_frame, image=felicitacion_ctk_img, text="")
            imagen_label.image = felicitacion_ctk_img  # Evitar garbage collection
            imagen_label.grid(row=0, column=0, sticky="n")
        except Exception as e:
            print(f"Error al cargar la imagen de felicitación: {e}")
            imagen_label = ctk.CTkLabel(imagen_frame, text="[Imagen no disponible]", width=300, height=500)
            imagen_label.grid(row=0, column=0, padx=10, pady=10)

    def _crear_frame_resultados(self, parent_frame):
        texto_frame = ctk.CTkFrame(parent_frame, fg_color="white")
        texto_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=(130,20))
        texto_frame.grid_rowconfigure((0, 1, 2, 3), weight=1)
        texto_frame.grid_columnconfigure(0, weight=1)

        # Título animado (estilo original)
        titulo_canvas = tk.Canvas(texto_frame, width=1200, height=150, bg="white", highlightthickness=0)
        titulo_canvas.grid(row=0, column=0, pady=(120, 0), sticky="n")
        self.crear_titulo_felicidades(titulo_canvas, "¡FELICIDADES!", 110)

        # Mensaje motivacional según puntaje (estilo original)
        mensaje, color = self._obtener_mensaje_segun_puntaje()
        
        mensaje_label = ctk.CTkLabel(
            texto_frame,
            text=mensaje,
            font=("Comic Sans MS", 35),
            justify="center",
            text_color=color,
            wraplength=600
        )
        mensaje_label.grid(row=1, column=0, pady=(0, 5), padx=5)

        # Puntaje (estilo original)
        puntaje_label = ctk.CTkLabel(
            texto_frame,
            text=f"Tu puntaje es: {self.puntaje} de {len(self.preguntas)}",
            font=("Comic Sans MS", 30),
            justify="center",
            text_color="black",
            wraplength=600
        )
        puntaje_label.grid(row=2, column=0, pady=(0, 10), padx=5)

        # Botón regresar
        boton_regresar = ctk.CTkButton(
            texto_frame,
            text="⏪ REGRESAR A EJERCICIOS ⏪",
            font=("Comic Sans MS", 25),
            fg_color="#931ea0",
            command=self.volver
        )
        boton_regresar.grid(row=3, column=0, pady=(0, 20))
    
    def _crear_frame_confirmacion(self):
        # Frame que cubre toda la ventana (para efecto de bloqueo)
        self.overlay_frame = ctk.CTkFrame(
            self.master, 
            fg_color="transparent",
            width=self.master.winfo_width(), 
            height=self.master.winfo_height()
        )
        self.overlay_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)

        # Frame de confirmación centrado
        self.confirm_frame = ctk.CTkFrame(
            self.overlay_frame, 
            fg_color="white", 
            width=500, 
            height=300,
            corner_radius=15,
            border_width=5,
            border_color="#931ea0"
        )
        self.confirm_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Configurar grid para el frame de confirmación
        self.confirm_frame.grid_rowconfigure((0, 1, 2), weight=1)
        self.confirm_frame.grid_columnconfigure((0, 1), weight=1)

        # Mensaje de confirmación
        mensaje_label = ctk.CTkLabel(
            self.confirm_frame,
            text="TU PROGRESO SE PERDERÁ 📢‼️\n¿deseas continuar?",
            font=("Comic Sans MS", 25),
            text_color="black",
            justify="center"
        )
        mensaje_label.grid(row=0, column=0, columnspan=2, pady=(20, 0), padx=(60, 25))

        # Botón Sí
        boton_si = ctk.CTkButton(
            self.confirm_frame,
            text="SÍ",
            font=("Comic Sans MS", 20),
            fg_color="gray",
            hover_color="#7a1885",
            command=self._confirmar_salida
        )
        boton_si.grid(row=1, column=0, padx=(20, 10), pady=(10, 20), sticky="e")

        # Botón No
        boton_no = ctk.CTkButton(
            self.confirm_frame,
            text="NO",
            font=("Comic Sans MS", 20),
            fg_color="#931ea0",
            hover_color="#7a1885",
            command=self._cancelar_salida
        )
        boton_no.grid(row=1, column=1, padx=(10, 20), pady=(10, 20), sticky="w")

    def _confirmar_salida(self):
        self.reiniciar_respuestas()
        self._eliminar_frame_confirmacion()
        if self.callback_volver:
            self.callback_volver()

    def _cancelar_salida(self):
        self._eliminar_frame_confirmacion()

    def _eliminar_frame_confirmacion(self):
        #Elimina los frames de confirmación y overlay
        if hasattr(self, 'confirm_frame'):
            self.confirm_frame.destroy()
        if hasattr(self, 'overlay_frame'):
            self.overlay_frame.destroy()

    def volver(self):
        #Maneja el evento de volver con confirmación
        if self.pregunta_actual < len(self.preguntas) and self.pregunta_actual > 0:
            self._crear_frame_confirmacion()
        else:
            if self.callback_volver:
                self.callback_volver()

    def _obtener_mensaje_segun_puntaje(self):
        #Devuelve el mensaje y color según el puntaje (estilo original)
        if self.puntaje < 3:
            return "¡SUERTE PARA LA SIGUIENTE!", "red"
        elif self.puntaje < 5:
            return "¡VAMOS MEJORANDO!", "blue"
        else:
            return "¡PERFECTO, CONTINÚA ASÍ!", "green"

    def crear_titulo_felicidades(self, canvas, texto, tamano_fuente):
        """Crea el título animado (estilo original)"""
        colores = ["#FF5252", "#4FC3F7", "#FFEB3B", "#69F0AE", "#FF4081", "#BA68C8"]
        fuente = ("Comic Sans MS", tamano_fuente, "bold")

        total_ancho = 0
        letras_ancho = []
        for letra in texto:
            id_temp = canvas.create_text(0, 0, text=letra, font=fuente, anchor="w")
            bbox = canvas.bbox(id_temp)
            ancho = bbox[2] - bbox[0]
            letras_ancho.append(ancho)
            total_ancho += ancho
            canvas.delete(id_temp)

        x = (1200 - total_ancho) // 2
        y = 65

        for i, letra in enumerate(texto):
            color = colores[i % len(colores)]

            # Sombra
            canvas.create_text(x + 2, y + 2, text=letra, font=fuente, fill="#AAAAAA", anchor="w")
            # Letra principal
            canvas.create_text(x, y, text=letra, font=fuente, fill=color, anchor="w")

            x += letras_ancho[i]


    def reiniciar_respuestas(self):
        #Reinicia las respuestas guardadas (estilo original)
        carpeta_respuestas = "respuestas"
        os.makedirs(carpeta_respuestas, exist_ok=True)

        nombre_lectura = os.path.splitext(os.path.basename(self.lectura_path))[0]
        archivo_respuestas = os.path.join(carpeta_respuestas, f"{nombre_lectura}.json")

        if os.path.exists(archivo_respuestas):
            os.remove(archivo_respuestas)


    def guardar_respuestas(self):
        #Guarda las respuestas en JSON (estilo original)
        carpeta_respuestas = "respuestas"
        os.makedirs(carpeta_respuestas, exist_ok=True)

        nombre_lectura = os.path.splitext(os.path.basename(self.lectura_path))[0]
        archivo_salida = os.path.join(carpeta_respuestas, f"{nombre_lectura}.json")

        datos = [{
            "lectura": nombre_lectura,
            "titulo": [self.titulo],
            "puntaje": self.puntaje,
            "respuestas": self.respuestas_elegidas,
        }]

        with open(archivo_salida, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)