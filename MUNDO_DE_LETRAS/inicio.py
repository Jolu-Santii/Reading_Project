import customtkinter
from PIL import Image, ImageTk
from tkinter import Canvas
from base_frame import BaseFrame
import os

class InicioFrame(BaseFrame):
    def __init__(self, master, show_frame_callback):
        super().__init__(master, show_frame_callback)
        
        # Configuración adicional del grid
        self.grid_rowconfigure(3, weight=6)
        self.grid_rowconfigure(2, weight=1)
        self.master = master
        self.show_frame = show_frame_callback
        self.width = self.master.winfo_screenwidth()
        self.height = self.master.winfo_screenheight()

        self.configure(fg_color="white")

        # Config grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=6)
        self.grid_rowconfigure(2, weight=1)

        # Imágenes
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        # Ruta completa de la imagen
        ruta_imagen = os.path.join(BASE_DIR, "recursos", "nino.png")

        self.nino = Image.open(ruta_imagen)
        self.nino = self.nino.resize((int(self.width/5), int(self.height/1.66)))
        self.tk_nino = ImageTk.PhotoImage(self.nino)

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        # Ruta completa de la imagen
        ruta_imagen = os.path.join(BASE_DIR, "recursos", "globo.png")
        
        self.globo = Image.open(ruta_imagen)
        globo_width = int(self.width/1.72)
        globo_height = int(self.height/2)        
        self.globo = self.globo.resize((globo_width, globo_height))
        self.tk_globo = ImageTk.PhotoImage(self.globo)

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        # Ruta completa de la imagen
        ruta_imagen = os.path.join(BASE_DIR, "recursos", "nina.png")

        self.nina = Image.open(ruta_imagen)
        self.nina = self.nina.resize((int(self.width/5), int(self.height/1.66)))
        self.tk_nina = ImageTk.PhotoImage(self.nina)

        # Contenedores
        self.contenedor_nino = customtkinter.CTkCanvas(self, width=int(self.width/5), height=int(self.height/1.66), bg="white", highlightthickness=0)
        self.contenedor_nino.grid(row=2, column=0, rowspan=2, padx=0, pady=0)
        self.contenedor_nino.create_image(self.contenedor_nino.winfo_reqwidth()//2, self.contenedor_nino.winfo_reqheight()//2, image=self.tk_nino)

        self.contenedor_nina = customtkinter.CTkCanvas(self, width=int(self.width/5), height=int(self.height/1.66), bg="white", highlightthickness=0)
        self.contenedor_nina.grid(row=2, column=2, rowspan=2, padx=0, pady=0)
        self.contenedor_nina.create_image(self.contenedor_nina.winfo_reqwidth()//2, self.contenedor_nina.winfo_reqheight()//2, image=self.tk_nina)


        # Globo

        # Configuración del texto
        self.frame_globo = customtkinter.CTkFrame(self, fg_color="transparent")
        self.frame_globo.grid(row=2, column=1, sticky="nsew")

        # Canvas para el globo con borde de depuración (puedes quitarlo luego)
        self.globo_canvas = Canvas(
            self.frame_globo,
            width=int(self.width/2.2),
            height=int(self.height/2),
            bg="white",
            highlightthickness=0,
            highlightbackground="red"  
        )
        self.globo_canvas.pack(expand=True, fill="both")

        # Imagen de fondo del globo
        self.globo_canvas.create_image(
            int(self.width/3.44),
            int(self.height/4),
            image=self.tk_globo
        )

        def crear_texto_multilinea(canvas, texto, max_width, y_pos, tamano_fuente):
            palabras = texto.split()
            colores = ["#FF5252", "#4FC3F7", "#FFEB3B", "#69F0AE", "#FF4081", "#BA68C8"]
            lineas = []
            linea_actual = []
            ancho_actual = 0
            
            # Calcular espacio por palabra
            temp_font = ("Comic Sans MS", tamano_fuente, "bold")
            espacio_ancho = canvas.create_text(0, 0, text=" ", font=temp_font, anchor="w")
            espacio = canvas.bbox(espacio_ancho)[2] - canvas.bbox(espacio_ancho)[0]
            canvas.delete(espacio_ancho)
            
            # Dividir en líneas
            for palabra in palabras:
                palabra_ancho = canvas.create_text(0, 0, text=palabra, font=temp_font, anchor="w")
                palabra_w = canvas.bbox(palabra_ancho)[2] - canvas.bbox(palabra_ancho)[0]
                canvas.delete(palabra_ancho)
                
                if ancho_actual + palabra_w <= max_width:
                    linea_actual.append(palabra)
                    ancho_actual += palabra_w + espacio
                else:
                    lineas.append(linea_actual)
                    linea_actual = [palabra]
                    ancho_actual = palabra_w + espacio
            
            if linea_actual:
                lineas.append(linea_actual)
            
            # Dibujar cada línea centrada
            for i, linea in enumerate(lineas):
                texto_linea = " ".join(linea)
                ancho_linea = canvas.create_text(0, 0, text=texto_linea, font=temp_font, anchor="w")
                bbox = canvas.bbox(ancho_linea)
                canvas.delete(ancho_linea)
                
                x_pos = (int(self.width/1.72) - (bbox[2]-bbox[0])) // 2
                current_x = x_pos
                
                # Dibujar cada letra con su color
                for palabra in linea:
                    for j, letra in enumerate(palabra):
                        color_idx = (i + j) % len(colores)
                        
                        # Sombra
                        canvas.create_text(
                            current_x + 2, y_pos + i*60 + 2,
                            text=letra,
                            fill="#AAAAAA",
                            font=temp_font,
                            anchor="w"
                        )
                        # Texto principal
                        letra_id = canvas.create_text(
                            current_x, y_pos + i*60,
                            text=letra,
                            fill=colores[color_idx],
                            font=temp_font,
                            anchor="w"
                        )
                        current_x += canvas.bbox(letra_id)[2] - canvas.bbox(letra_id)[0]
                    
                    # Añadir espacio después de cada palabra
                    espacio_id = canvas.create_text(
                        current_x, y_pos + i*60,
                        text=" ",
                        font=temp_font,
                        anchor="w"
                    )
                    current_x += canvas.bbox(espacio_id)[2] - canvas.bbox(espacio_id)[0]
                    canvas.delete(espacio_id)

        # Llamar a la función con el texto
        crear_texto_multilinea(
            self.globo_canvas,
            "¿Qué vamos a hacer hoy aventurero?",
            int(self.width/1.72) * 0.9, 
            int(self.height/4) - 30,     
            50                            # Tamaño de fuente
        )

    def ejercicios_event(self):
        self.show_frame("ejercicios")
