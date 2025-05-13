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
        self.grid_rowconfigure(6, weight=1)

        # Botones del frame base
        self.update_main_buttons()

        # Lista de elementos ocultables
        self.elementos_ocultables = []

        # Añadir header a la lista si existe
        if hasattr(self, 'header'):
            self.elementos_ocultables.append(self.header)

        # Imagen (como un atributo para ocultarla)
        self.pensando = Image.open("recursos/Pensando.png")
        self.pensando = self.pensando.resize((int(self.width/3), int(self.height*0.8)))
        self.tk_pensando = ImageTk.PhotoImage(self.pensando)

        self.contenedor_pensando = ctk.CTkCanvas(self, width=int(self.width/3), height=int(self.height*0.8), bg="white", highlightthickness=0)
        self.contenedor_pensando.grid(row=2, column=0, rowspan=4, padx=0, pady=0)
        self.contenedor_pensando.create_image(int(self.contenedor_pensando.winfo_reqwidth() / 2), 
                                              int(self.contenedor_pensando.winfo_reqheight() / 2), 
                                              image=self.tk_pensando)
        self.elementos_ocultables.append(self.contenedor_pensando)

        titulo1 = "DECIR LO QUE PIENSAS Y PENSAR EN LO QUE DICES"
        self.crear_boton_lectura(titulo1,"lecturas/lectura1.txt", "preguntas/preguntas1.json", "ImagenesLecturas/Lectura1.png", 2,1,"purple")

        titulo2 = "LAS RANAS DE NATA"
        self.crear_boton_lectura(titulo2, "lecturas/lectura2.txt", "preguntas/preguntas2.json","ImagenesLecturas/Lectura2.jpg", 2,2, "blue")

        titulo3 = "LA TORTUGA Y EL ANTÍLOPE"
        self.crear_boton_lectura(titulo3, "lecturas/lectura3.txt", "preguntas/preguntas3.json", "ImagenesLecturas/Lectura3.jpg", 3, 1, "yellow")

        titulo4 = "EL ÚLTIMO MOHICANO"
        self.crear_boton_lectura(titulo4, "lecturas/lectura4.txt", "preguntas/preguntas4.json", "ImagenesLecturas/Lectura4.jpg", 3, 2, "red")

        titulo5 = "EL PRINCIPITO"
        self.crear_boton_lectura(titulo5, "lecturas/lectura5.txt", "preguntas/preguntas5.json", "ImagenesLecturas/Lectura5.jpg", 4, 1, "orange")

        titulo6 = "Y COLORIN COLORADO..."
        self.crear_boton_lectura(titulo6, "lecturas/lectura6.txt", "preguntas/preguntas6.json", "ImagenesLecturas/Lectura6.jpg", 4, 2, "green")

        titulo7 = "MOZART"
        self.crear_boton_lectura(titulo7, "lecturas/lectura7.txt", "preguntas/preguntas7.json", "ImagenesLecturas/Lectura7.jpg", 5, 1, "gray")

        titulo8 = "EL COLMILLO BLANCO"
        self.crear_boton_lectura(titulo8, "lecturas/lectura8.txt", "preguntas/preguntas8.json", "ImagenesLecturas/Lectura8.jpg", 5, 2, "blue")

        titulo9 = "TATIN EL NIÑO AVISPA"
        self.crear_boton_lectura(titulo9, "lecturas/lectura9.txt", "preguntas/preguntas9.json", "ImagenesLecturas/Lectura9.jpg", 6, 1, "pink")

        titulo10 = "LOS PERITIOS"
        self.crear_boton_lectura(titulo10, "lecturas/lectura10.txt", "preguntas/preguntas10.json", "ImagenesLecturas/Lectura10.jpg", 6, 2, "black")


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

        # Crear nuevo frame de lectura que llene todo el espacio
        self.lectura_frame = ctk.CTkFrame(self)
        self.lectura_frame.grid(row=0, column=0, columnspan=2, rowspan=5, sticky="nsew")
        self.lectura_frame.grid_rowconfigure(0, weight=1)
        self.lectura_frame.grid_columnconfigure(0, weight=1)

        # Cargar lectura con expansión completa
        lectura_widget = LecturaInteractiva(
            master=self.lectura_frame,
            titulo=titulo,
            lectura_path=lectura_path,
            preguntas_path=preguntas_path,
            imagen_path=imagen_path,
            volver_func=lambda: self.show_frame("ejercicios")
        )
        lectura_widget.grid(row=0, column=0, sticky="nsew") 


    def crear_boton_lectura(self, titulo, rutaLectura, rutaPregunta, rutaImagen, pLinea, pColumna,color_fg):
        button_font = ctk.CTkFont(family="Montserrat", size=22)

        self.ejercicio = ctk.CTkButton(
            self,
            width=300,
            height=50,
            corner_radius=20,
            fg_color=color_fg,
            hover_color="#d5d5d5",
            font=button_font,
            text=titulo,
            text_color="white",
            command = lambda: self.mostrar_lectura(
                titulo,
                rutaLectura,
                rutaPregunta,
                rutaImagen
            )
        )

        self.ejercicio.grid(
            row=pLinea,
            column=pColumna,
            padx=(40, 40),
            pady=(5, 10),
            sticky="w"
        )
        self.elementos_ocultables.append(self.ejercicio)

"""         titulo = ""
        command = lambda: self.mostrar_lectura(
                "",
                "lecturas/lectura.txt",
                "preguntas/preguntas.json",
                "ImagenesLecturas/Lectura.jpg"
            )
        self.crear_boton_lectura(titulo, command, , )"""