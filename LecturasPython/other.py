import customtkinter as ctk
from lectura_interactiva import LecturaInteractiva

# Crear ventana principal
ventana = ctk.CTk()
ventana.title("Lectura interactiva")
ventana.state("zoomed")
ventana.geometry("1920x1080")

# Variables globales
lectura_frame = None
botones_frame = None

def mostrar_lectura(titulo, lectura_path, preguntas_path, imagen_path):
    global lectura_frame, botones_frame

    # Ocultar botones
    botones_frame.pack_forget()

    # Eliminar lectura anterior si existe
    if lectura_frame:
        lectura_frame.destroy()

    # Crear nueva lectura
    lectura_frame = LecturaInteractiva(
        master=ventana,
        titulo=titulo,
        lectura_path=lectura_path,
        preguntas_path=preguntas_path,
        imagen_path=imagen_path
    )
    lectura_frame.pack(fill="both", expand=True)

    # Botón para volver a los botones de lectura
    volver_btn = ctk.CTkButton(
        master=lectura_frame,
        text="Volver a selección de lecturas",
        command=mostrar_botones
    )
    volver_btn.pack(side="bottom", pady=10)

def mostrar_botones():
    global lectura_frame, botones_frame
    
    # Ocultar lectura actual si existe
    if lectura_frame:
        lectura_frame.pack_forget()
    
    # Mostrar botones
    botones_frame.pack(side="top", pady=20)

# Frame para botones
botones_frame = ctk.CTkFrame(master=ventana)

# Botón 1
btn1 = ctk.CTkButton(
    master=botones_frame,
    text="Lectura 1",
    command=lambda: mostrar_lectura(
        "EL ÚLTIMO MOHICANO",
        "lecturas/lectura4.txt",
        "preguntas/preguntas4.json",
        "ImagenesLecturas/Lectura4.jpg"
    )
)
btn1.pack(side="left", padx=10)

# Botón 2
btn2 = ctk.CTkButton(
    master=botones_frame,
    text="Lectura 2",
    command=lambda: mostrar_lectura(
        "EL PRINCIPITO",
        "lecturas/lectura5.txt",
        "preguntas/preguntas5.json",
        "ImagenesLecturas/Lectura5.jpg"
    )
)
btn2.pack(side="left", padx=10)

# Botón 3
btn3 = ctk.CTkButton(
    master=botones_frame,
    text="Lectura 3",
    command=lambda: mostrar_lectura(
        "Y COLORIN COLORADO...",
        "lecturas/lectura6.txt",
        "preguntas/preguntas6.json",
        "ImagenesLecturas/Lectura6.jpg"
    )
)
btn3.pack(side="left", padx=10)

# Mostrar botones inicialmente
mostrar_botones()

# Ejecutar la aplicación
ventana.mainloop()