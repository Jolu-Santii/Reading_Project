from customtkinter import CTk
from inicio import InicioFrame
from ejercicios import EjerciciosFrame
from base_frame import BaseFrame
from reportes import ReportesFrame


class App(CTk):
    def __init__(self):
        super().__init__()

        self.title("App Principal")
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
        self._set_appearance_mode("light")
        self.configure(fg_color="white")
        
        self.frames = {} 
        self.create_frames()
        self.show_frame("inicio")

    def create_frames(self):
        self.frames["inicio"] = InicioFrame(self, self.show_frame)
        self.frames["ejercicios"] = EjerciciosFrame(self, self.show_frame)
        self.frames["reportes"] = ReportesFrame(self, self.show_frame)

        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()
