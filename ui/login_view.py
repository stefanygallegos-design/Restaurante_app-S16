import tkinter as tk
from tkinter import ttk, messagebox


class LoginView(tk.Frame):
    """Ventana de inicio de sesión."""

    def __init__(
        self,
        master,
        servicio,
        on_login
    ):

        super().__init__(
            master,
            bg="#eef4f7"
        )

        self.servicio = servicio
        self.on_login = on_login

        self._construir()

    def _construir(self):

        tarjeta = tk.Frame(
            self,
            bg="white",
            highlightthickness=1,
            highlightbackground="#d8e1e7"
        )

        tarjeta.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
            width=430,
            height=430
        )

        tk.Label(
            tarjeta,
            text="RESTAURANTE APP",
            font=("Segoe UI", 22, "bold"),
            bg="white",
            fg="#14566d"
        ).pack(pady=(45, 5))

        tk.Label(
            tarjeta,
            text="Semana 16 • Manejo de eventos",
            font=("Segoe UI", 10),
            bg="white",
            fg="#60727d"
        ).pack(pady=(0, 25))

        tk.Label(
            tarjeta,
            text="Usuario",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#30434d"
        ).pack(
            anchor="w",
            padx=55
        )

        self.usuario_entry = ttk.Entry(
            tarjeta,
            font=("Segoe UI", 11)
        )

        self.usuario_entry.pack(
            fill="x",
            padx=55,
            pady=(5, 15)
        )

        tk.Label(
            tarjeta,
            text="Contraseña",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#30434d"
        ).pack(
            anchor="w",
            padx=55
        )

        self.contrasena_entry = ttk.Entry(
            tarjeta,
            show="*",
            font=("Segoe UI", 11)
        )

        self.contrasena_entry.pack(
            fill="x",
            padx=55,
            pady=(5, 20)
        )

        ttk.Button(
            tarjeta,
            text="Ingresar",
            command=self.iniciar_sesion
        ).pack(
            padx=55,
            fill="x",
            ipady=6
        )

        tk.Label(
            tarjeta,
            text="Administrador: admin / admin123",
            font=("Segoe UI", 9),
            bg="white",
            fg="#74858e"
        ).pack(pady=(22, 2))

        tk.Label(
            tarjeta,
            text="Empleado: empleado / empleado123",
            font=("Segoe UI", 9),
            bg="white",
            fg="#74858e"
        ).pack()

        tk.Label(
            tarjeta,
            text="Cliente: cliente / cliente123",
            font=("Segoe UI", 9),
            bg="white",
            fg="#74858e"
        ).pack()

        # Evento de teclado
        self.usuario_entry.bind(
            "<Return>",
            self.al_presionar_enter
        )

        self.contrasena_entry.bind(
            "<Return>",
            self.al_presionar_enter
        )

        self.usuario_entry.focus_set()

    def al_presionar_enter(self, event):

        self.iniciar_sesion()

    def iniciar_sesion(self):

        usuario = self.usuario_entry.get().strip()

        contrasena = self.contrasena_entry.get()

        if not usuario or not contrasena:

            messagebox.showwarning(
                "Inicio de sesión",
                "Ingrese usuario y contraseña."
            )

            return

        usuario_obj = self.servicio.autenticar(
            usuario,
            contrasena
        )

        if usuario_obj:

            self.on_login(usuario_obj)

        else:

            messagebox.showerror(
                "Acceso denegado",
                "Usuario o contraseña incorrectos."
            )
