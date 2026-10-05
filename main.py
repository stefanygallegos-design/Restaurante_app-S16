import tkinter as tk
from pathlib import Path

from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView


class RestauranteApp(tk.Tk):

    def __init__(self):

        super().__init__()

        self.title(
            "Restaurante App - Semana 16"
        )

        self.geometry(
            "1120x720"
        )

        self.minsize(
            980,
            650
        )

        self.configure(
            bg="#eef4f7"
        )

        base_dir = Path(
            __file__
        ).resolve().parent

        self.servicio = RestauranteServicio(
            base_dir
        )

        self.mostrar_login()

    def limpiar_ventana(self):

        for widget in self.winfo_children():

            widget.destroy()

    def mostrar_login(self):

        self.limpiar_ventana()

        login = LoginView(
            self,
            self.servicio,
            self.iniciar_aplicacion
        )

        login.pack(
            fill="both",
            expand=True
        )

    def iniciar_aplicacion(
        self,
        usuario
    ):

        self.usuario_actual = usuario

        self.limpiar_ventana()

        principal = MainView(
            self,
            self.servicio,
            usuario,
            self.cerrar_sesion
        )

        principal.pack(
            fill="both",
            expand=True
        )

    def cerrar_sesion(self):

        self.usuario_actual = None

        self.mostrar_login()


if __name__ == "__main__":

    app = RestauranteApp()

    app.mainloop()
