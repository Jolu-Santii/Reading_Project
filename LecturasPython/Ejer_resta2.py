import customtkinter as ctk
import subprocess
from PIL import Image, ImageTk
from base_frame import BaseFrame
from lectura_interactiva import LecturaInteractiva  # Asegúrate de tener esta clase implementada

class EjerciciosFrame(BaseFrame):
    def __init__(self, master, show_frame_callback):
        super().__init__(master, show_frame_callback)

        # Configuración adicional del grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Botones del frame base
        self.update_main_buttons()

        # Lista de elementos ocultables
        self.elementos_ocultables = []

        # Añadir header a la lista si existe
        if hasattr(self, 'header'):
            self.elementos_ocultables.append(self.header)

        # Imagen (como un atributo para ocultarla)
        self.pensando = Image.open("C:\\Users\\RODRIGUEZMLDO\\Documents\\LecturasPython\\recursos\\Pensando.png")
        self.pensando = self.pensando.resize((int(self.width/3), int(self.height*0.8)))
        self.tk_pensando = ImageTk.PhotoImage(self.pensando)

        self.contenedor_pensando = ctk.CTkCanvas(self, width=int(self.width/3), height=int(self.height*0.8), bg="white", highlightthickness=0)
        self.contenedor_pensando.grid(row=2, column=0, rowspan=4, padx=0, pady=0)
        self.contenedor_pensando.create_image(int(self.contenedor_pensando.winfo_reqwidth() / 2), 
                                              int(self.contenedor_pensando.winfo_reqheight() / 2), 
                                              image=self.tk_pensando)
        self.elementos_ocultables.append(self.contenedor_pensando)

        # Crear botones de ejercicios
        self.create_exercise_button()
        self.create_second_exercise_button()

        # Frame para lecturas (se destruye al volver)
        self.lectura_frame = None

    def ocultar_elementos(self):
        """Oculta todos los elementos no esenciales"""
        for elemento in self.elementos_ocultables:
            elemento.grid_remove()

    def mostrar_elementos(self):
        """Muestra todos los elementos ocultos"""
        for elemento in self.elementos_ocultables:
            elemento.grid()

    def mostrar_lectura(self, titulo, lectura_path, preguntas_path, imagen_path):
        """Muestra una lectura, ocultando otros elementos"""
        self.ocultar_elementos()

        # Destruir lectura anterior si existe
        if self.lectura_frame:
            self.lectura_frame.destroy()

        # Crear nuevo frame de lectura
        self.lectura_frame = ctk.CTkFrame(self)
        self.lectura_frame.grid(row=0, column=0, columnspan=2, rowspan=5, sticky="nsew", padx=20, pady=20)

        # Widget de lectura
        lectura_widget = LecturaInteractiva(
            master=self.lectura_frame,
            titulo=titulo,
            lectura_path=lectura_path,
            preguntas_path=preguntas_path,
            imagen_path=imagen_path
        )
        lectura_widget.pack(fill="both", expand=True)

        # Botón para volver
        volver_btn = ctk.CTkButton(
            self.lectura_frame,
            text="Volver a ejercicios",
            command=self.volver_a_ejercicios
        )
        volver_btn.pack(side="bottom", pady=20)

    def volver_a_ejercicios(self):
        """Vuelve a la vista de ejercicios"""
        if self.lectura_frame:
            self.lectura_frame.destroy()
            self.lectura_frame = None
        self.mostrar_elementos()

    def create_exercise_button(self):
        button_font = ctk.CTkFont(family="Montserrat", size=22)

        self.ejercicio1 = ctk.CTkButton(
            self,
            width=300,
            height=50,
            corner_radius=20,
            fg_color="grey",
            hover_color="#d5d5d5",
            font=button_font,
            text="Decir lo que piensas y pensar lo que dices",
            text_color="Black",
            command=lambda: self.mostrar_lectura(
                "Decir lo que piensas y pensar lo que dices",
                "lecturas/lectura1.txt",
                "preguntas/preguntas1.json",
                "ImagenesLecturas/Lectura1.jpg"
            )
        )

        self.ejercicio1.grid(
            row=2,
            column=1,
            padx=(40, 40),
            pady=(30, 20),
            sticky="w"
        )
        self.elementos_ocultables.append(self.ejercicio1)

    def create_second_exercise_button(self):
        button_font = ctk.CTkFont(family="Montserrat", size=22)

        self.ejercicio2 = ctk.CTkButton(
            self,
            width=300,
            height=50,
            corner_radius=20,
            fg_color="grey",
            hover_color="#d5d5d5",
            font=button_font,
            text="las ranas de nata",
            text_color="white",
            command=lambda: self.mostrar_lectura(
                "las ranas de nata",
                "lecturas/lectura2.txt",
                "preguntas/preguntas2.json",
                "ImagenesLecturas/Lectura2.jpg"
            )
        )

        self.ejercicio2.grid(
            row=3,
            column=1,
            padx=(40, 40),
            pady=(10, 15),
            sticky="w"
        )
        self.elementos_ocultables.append(self.ejercicio2)

    def abrir_otro_script(self):
        """Función alternativa para abrir script externo"""
        subprocess.run(["python", r"C:\\Users\\RODRIGUEZMLDO\\Documents\\LecturasPython\\Lectura1.py"])
