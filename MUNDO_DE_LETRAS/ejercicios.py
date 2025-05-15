import customtkinter as ctk
from PIL import Image, ImageTk
from base_frame import BaseFrame
import json, os
from tkinter import Canvas
import tkinter as tk
from lectura_interactiva import LecturaInteractiva

class EjerciciosFrame(BaseFrame):
    def __init__(self, master, show_frame_callback):
        super().__init__(master, show_frame_callback)
        self.lecturas_completadas = self.obtener_lecturas_completadas()
        
        # Configuración del grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(8, weight=1)
        
        # Fondo blanco
        self.configure(bg_color="white", fg_color="white")
        
        # Botones del frame base
        self.update_main_buttons()
        
        # Lista de elementos ocultables
        self.elementos_ocultables = []
        self.botones_ocultables = []
        if hasattr(self, 'header'):
            self.elementos_ocultables.append(self.header)

        # Configurar imagen de fondo
        self._setup_imagen_fondo()
        
        # Agregar título animado
        self._agregar_titulo_animado()
           
        # Crear botones de ejercicios
        self._crear_botones_originales()

        # Frame para lecturas
        self.lectura_frame = None
        self.overlay_frame = None

    def _setup_imagen_fondo(self):
        """Configura la imagen de fondo"""
        self.pensando = Image.open("recursos/Pensando.png")
        self.tk_pensando = ImageTk.PhotoImage(self.pensando)

        self.contenedor_pensando = ctk.CTkCanvas(
            self, 
            width=int(self.width/3), 
            height=int(self.height*0.8), 
            bg="white", 
            highlightthickness=0
        )
        self.contenedor_pensando.grid(row=2, column=0, rowspan=7, padx=0, pady=(0, 110))
        self.contenedor_pensando.create_image(
            int(self.contenedor_pensando.winfo_reqwidth() / 2), 
            int(self.contenedor_pensando.winfo_reqheight() / 2), 
            image=self.tk_pensando
        )
        self.elementos_ocultables.append(self.contenedor_pensando)

    def _agregar_titulo_animado(self):
        """Agrega el título animado"""
        titulo_frame = ctk.CTkFrame(self, fg_color="white")
        titulo_frame.grid(row=2, column=1, columnspan=2, sticky="nsew", pady=(40, 20))
        
        titulo_canvas = Canvas(titulo_frame, width=1200, height=90, bg="white", highlightthickness=0)
        titulo_canvas.pack(expand=True, fill="both")
        
        self.crear_titulo(titulo_canvas, "LECTURAS INTERACTIVAS", 50)
        self.elementos_ocultables.append(titulo_frame)

    def _crear_botones_originales(self):
        """Crea los botones de ejercicios"""

        self.lecturas_completadas = self.obtener_lecturas_completadas()

        button_font = ctk.CTkFont(family="Montserrat", size=22)

        with open("lista_ejercicios/ejercicios.json", encoding="utf-8") as f:
            ejercicios = json.load(f)

        for ejercicio in ejercicios:
            nombre_base = os.path.splitext(os.path.basename(ejercicio["lectura"]))[0]
            esta_completada = nombre_base in self.lecturas_completadas

            texto_boton = f"✓ {ejercicio['titulo']}" if esta_completada else f"🕮 {ejercicio['titulo']}"

            btn = ctk.CTkButton(
                self,
                text=texto_boton,
                height=50,
                corner_radius=20,
                font=button_font,
                text_color="white",
                fg_color=ejercicio["color"],
                hover_color=self._get_hover_color(ejercicio["color"]),
                command=lambda e=ejercicio, nb=nombre_base: self._manejar_clic_lectura(
                    e["titulo"], 
                    e["lectura"],
                    e["preguntas"], 
                    e["imagen"],
                    nb
                )
            )
            btn.grid(
                row=ejercicio["fila"],
                column=ejercicio["columna"],
                padx=(5, 40),
                pady=(0, 10),
                rowspan=1,
                sticky="w"
            )
            self.botones_ocultables.append(btn)
    
    def obtener_lecturas_completadas(self):
        """Obtiene la lista de nombres de lecturas ya completadas"""
        carpeta_respuestas = "respuestas"
        lecturas_completadas = []

        if not os.path.exists(carpeta_respuestas):
            return lecturas_completadas

        for archivo in os.listdir(carpeta_respuestas):
            if archivo.endswith('.json'):
                nombre_lectura = os.path.splitext(archivo)[0]
                lecturas_completadas.append(nombre_lectura)

        return lecturas_completadas

    def _manejar_clic_lectura(self, titulo, lectura_path, preguntas_path, imagen_path, nombre_lectura):
        """Maneja el clic en un botón de lectura"""
        if nombre_lectura in self.lecturas_completadas:
            self._mostrar_advertencia_reinicio(titulo, lectura_path, preguntas_path, imagen_path, nombre_lectura)
        else:
            self.mostrar_lectura(titulo, lectura_path, preguntas_path, imagen_path)

    def _mostrar_advertencia_reinicio(self, titulo, lectura_path, preguntas_path, imagen_path, nombre_lectura):
        """Muestra el diálogo de advertencia para lecturas completadas"""
        # Crear frame de superposición
        self.overlay_frame = ctk.CTkFrame(
            self, 
            fg_color="white",
            width=self.winfo_width(), 
            height=self.winfo_height(),
        )
        self.overlay_frame.configure(bg_color="black")
        self.overlay_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)
        
        # Frame de confirmación
        confirm_frame = ctk.CTkFrame(
            self.overlay_frame,
            fg_color="white",
            width=600,
            height=350,
            corner_radius=20,
            border_width=5,
            border_color="#931ea0"
        )
        confirm_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Configurar grid del frame de confirmación
        confirm_frame.grid_rowconfigure((0, 1, 2), weight=1)
        confirm_frame.grid_columnconfigure((0, 1), weight=1)

        # Mensaje de advertencia
        mensaje = ctk.CTkLabel(
            confirm_frame,
            text="✅ LECTURA YA COMPLETADA ✅\n\n¿Deseas realizarla nuevamente?\nTus respuestas anteriores se perderán.",
            font=("Comic Sans MS", 24, "bold"),
            text_color="#931ea0",
            justify="center",
            wraplength=500
        )
        mensaje.grid(row=0, column=0, columnspan=2, padx=20, pady=(30, 10))

        # Botón de reiniciar
        btn_reiniciar = ctk.CTkButton(
            confirm_frame,
            text="REINICIAR",
            font=("Comic Sans MS", 20, "bold"),
            fg_color="#931ea0",
            hover_color="#7a1885",
            command=lambda: self._reiniciar_lectura(titulo, lectura_path, preguntas_path, imagen_path, nombre_lectura)
        )
        btn_reiniciar.grid(row=1, column=0, padx=(20, 10), pady=20, sticky="e")

        # Botón de cancelar
        btn_cancelar = ctk.CTkButton(
            confirm_frame,
            text="CANCELAR",
            font=("Comic Sans MS", 20, "bold"),
            fg_color="gray",
            hover_color="#5a5a5a",
            command=self._cancelar_advertencia
        )
        btn_cancelar.grid(row=1, column=1, padx=(10, 20), pady=20, sticky="w")

    def _reiniciar_lectura(self, titulo, lectura_path, preguntas_path, imagen_path, nombre_lectura):
        """Elimina respuestas anteriores y muestra la lectura"""        
        self._cancelar_advertencia()
        self.mostrar_lectura(titulo, lectura_path, preguntas_path, imagen_path)

    def _cancelar_advertencia(self):
        """Cierra el diálogo de advertencia"""
        if self.overlay_frame:
            self.overlay_frame.destroy()
            self.overlay_frame = None

    def _get_hover_color(self, color):
        """Devuelve un color más claro para el efecto hover"""
        if color.startswith("#"):
            return f"#{min(255, int(color[1:3], 16)+30):02X}" \
                   f"{min(255, int(color[3:5], 16)+30):02X}" \
                   f"{min(255, int(color[5:7], 16)+30):02X}"
        return f"gray{max(20, min(80, 50))}"  # Para colores nombrados

    def mostrar_lectura(self, titulo, lectura_path, preguntas_path, imagen_path):
        """Muestra una lectura, ocultando otros elementos"""
        self.ocultar_elementos()

        if self.lectura_frame:
            self.lectura_frame.destroy()

        self.lectura_frame = ctk.CTkFrame(self, fg_color="white")
        self.lectura_frame.grid(row=0, column=0, columnspan=3, rowspan=7, sticky="nsew")
        
        LecturaInteractiva(
            master=self.lectura_frame,
            titulo=titulo,
            lectura_path=lectura_path,
            preguntas_path=preguntas_path,
            imagen_path=imagen_path,
            volver_func=self._volver_a_ejercicios
        ).pack(expand=True, fill="both")

    def _volver_a_ejercicios(self):
        """Vuelve a la vista de ejercicios"""
        if self.lectura_frame:
            self.lectura_frame.destroy()
            self.lectura_frame = None
            
        # Actualizar lista de lecturas completadas al volver
        self.lecturas_completadas = self.obtener_lecturas_completadas()

        #crear nuevamente los botones actualizados
        self._crear_botones_originales()

        # Recrear los botones para actualizar los estados
        self.mostrar_elementos()

    def ocultar_elementos(self):
        """Oculta todos los elementos no esenciales"""
        for elemento in self.elementos_ocultables:
            elemento.grid_remove()

        for elemento in self.botones_ocultables:
            elemento.grid_remove()

    def mostrar_elementos(self):
        """Muestra todos los elementos ocultos"""
        for elemento in self.elementos_ocultables:
            elemento.grid()


    def crear_titulo(self, canvas, texto, tamano_fuente):
        """Crea el título animado con colores"""
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

        x = (canvas.winfo_reqwidth() - total_ancho) // 2
        y = canvas.winfo_reqheight() // 2

        for i, letra in enumerate(texto):
            color = colores[i % len(colores)]
            canvas.create_text(x + 2, y + 2, text=letra, font=fuente, fill="#AAAAAA", anchor="w")
            canvas.create_text(x, y, text=letra, font=fuente, fill=color, anchor="w")
            x += letras_ancho[i]