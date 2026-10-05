import tkinter as tk
from tkinter import ttk, messagebox

from modelos.usuario import Usuario
from modelos.producto import Producto


class MainView(tk.Frame):

    def __init__(
        self,
        master,
        servicio,
        usuario_actual,
        on_logout
    ):

        super().__init__(
            master,
            bg="#eef4f7"
        )

        self.servicio = servicio
        self.usuario_actual = usuario_actual
        self.on_logout = on_logout

        self._configurar_estilos()
        self._construir_encabezado()
        self._construir_contenido()

        self.refrescar_todo()

    # =========================================================
    # ESTILOS
    # =========================================================

    def _configurar_estilos(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "TButton",
            font=("Segoe UI", 10),
            padding=6
        )

        style.configure(
            "Treeview",
            font=("Segoe UI", 9),
            rowheight=28
        )

        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 9, "bold")
        )

        style.configure(
            "TNotebook.Tab",
            font=("Segoe UI", 10, "bold"),
            padding=(15, 8)
        )

    # =========================================================
    # ENCABEZADO
    # =========================================================

    def _construir_encabezado(self):

        header = tk.Frame(
            self,
            bg="#14566d",
            height=78
        )

        header.pack(fill="x")

        header.pack_propagate(False)

        tk.Label(
            header,
            text="RESTAURANTE APP",
            font=("Segoe UI", 20, "bold"),
            bg="#14566d",
            fg="white"
        ).pack(
            side="left",
            padx=25
        )

        info = (
            f"{self.usuario_actual.nombre}  •  "
            f"{self.usuario_actual.rol}"
        )

        tk.Label(
            header,
            text=info,
            font=("Segoe UI", 10),
            bg="#14566d",
            fg="white"
        ).pack(
            side="right",
            padx=(10, 15)
        )

        ttk.Button(
            header,
            text="Cerrar sesión",
            command=self.on_logout
        ).pack(
            side="right",
            padx=10
        )

    # =========================================================
    # CONTENIDO
    # =========================================================

    def _construir_contenido(self):

        contenedor = tk.Frame(
            self,
            bg="#eef4f7"
        )

        contenedor.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=18
        )

        self.notebook = ttk.Notebook(
            contenedor
        )

        self.notebook.pack(
            fill="both",
            expand=True
        )

        self._crear_tab_inicio()
        self._crear_tab_productos()
        self._crear_tab_ventas()

        if self.usuario_actual.rol == "Administrador":

            self._crear_tab_usuarios()

    # =========================================================
    # INICIO
    # =========================================================

    def _crear_tab_inicio(self):

        self.tab_inicio = tk.Frame(
            self.notebook,
            bg="white"
        )

        self.notebook.add(
            self.tab_inicio,
            text="  Inicio  "
        )

        tk.Label(
            self.tab_inicio,
            text="Panel principal",
            font=("Segoe UI", 24, "bold"),
            bg="white",
            fg="#14566d"
        ).pack(
            pady=(70, 10)
        )

        tk.Label(
            self.tab_inicio,
            text=f"Bienvenida/o, {self.usuario_actual.nombre}",
            font=("Segoe UI", 14),
            bg="white",
            fg="#334952"
        ).pack(pady=5)

        tk.Label(
            self.tab_inicio,
            text="Sistema de gestión de restaurante",
            font=("Segoe UI", 11),
            bg="white",
            fg="#687b84"
        ).pack(pady=5)

        tk.Label(
            self.tab_inicio,
            text="Semana 16: manejo de eventos y callbacks",
            font=("Segoe UI", 10, "italic"),
            bg="white",
            fg="#80919a"
        ).pack(pady=10)

    # =========================================================
    # PRODUCTOS
    # =========================================================

    def _crear_tab_productos(self):

        self.tab_productos = tk.Frame(
            self.notebook,
            bg="#f9fbfc"
        )

        self.notebook.add(
            self.tab_productos,
            text="  Productos  "
        )

        form = tk.LabelFrame(
            self.tab_productos,
            text="Datos del producto",
            font=("Segoe UI", 10, "bold"),
            bg="#f9fbfc",
            padx=12,
            pady=12
        )

        form.pack(
            fill="x",
            padx=15,
            pady=15
        )

        self.prod_id = self._campo(
            form,
            "ID:",
            0,
            0
        )

        self.prod_nombre = self._campo(
            form,
            "Nombre:",
            0,
            2
        )

        self.prod_precio = self._campo(
            form,
            "Precio:",
            1,
            0
        )

        self.prod_stock = self._campo(
            form,
            "Stock:",
            1,
            2
        )

        acciones = tk.Frame(
            form,
            bg="#f9fbfc"
        )

        acciones.grid(
            row=2,
            column=0,
            columnspan=4,
            pady=(15, 0),
            sticky="w"
        )

        self.btn_prod_reg = ttk.Button(
            acciones,
            text="Registrar",
            command=self.registrar_producto
        )

        self.btn_prod_act = ttk.Button(
            acciones,
            text="Actualizar",
            command=self.actualizar_producto
        )

        self.btn_prod_del = ttk.Button(
            acciones,
            text="Eliminar",
            command=self.eliminar_producto
        )

        self.btn_prod_lim = ttk.Button(
            acciones,
            text="Limpiar",
            command=self.limpiar_producto
        )

        for boton in [
            self.btn_prod_reg,
            self.btn_prod_act,
            self.btn_prod_del,
            self.btn_prod_lim
        ]:

            boton.pack(
                side="left",
                padx=4
            )

        if self.usuario_actual.rol == "Cliente":

            self.btn_prod_reg.state(["disabled"])
            self.btn_prod_act.state(["disabled"])
            self.btn_prod_del.state(["disabled"])

        tabla_frame = tk.Frame(
            self.tab_productos,
            bg="#f9fbfc"
        )

        tabla_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        columnas = (
            "id",
            "nombre",
            "precio",
            "stock"
        )

        self.tabla_productos = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings",
            selectmode="browse"
        )

        encabezados = {

            "id": "ID",

            "nombre": "Nombre",

            "precio": "Precio",

            "stock": "Stock"
        }

        for columna in columnas:

            self.tabla_productos.heading(
                columna,
                text=encabezados[columna]
            )

        self.tabla_productos.column(
            "id",
            width=100,
            anchor="center"
        )

        self.tabla_productos.column(
            "nombre",
            width=300
        )

        self.tabla_productos.column(
            "precio",
            width=120,
            anchor="center"
        )

        self.tabla_productos.column(
            "stock",
            width=100,
            anchor="center"
        )

        scroll = ttk.Scrollbar(
            tabla_frame,
            orient="vertical",
            command=self.tabla_productos.yview
        )

        self.tabla_productos.configure(
            yscrollcommand=scroll.set
        )

        self.tabla_productos.pack(
            side="left",
            fill="both",
            expand=True
        )

        scroll.pack(
            side="right",
            fill="y"
        )

        self.tabla_productos.bind(
            "<<TreeviewSelect>>",
            self.al_seleccionar_producto
        )

    def registrar_producto(self):

        try:

            producto = Producto(
                self.prod_id.get(),
                self.prod_nombre.get(),
                self.prod_precio.get(),
                self.prod_stock.get()
            )

            self.servicio.registrar_producto(
                producto
            )

            messagebox.showinfo(
                "Producto",
                "Producto registrado correctamente."
            )

            self.refrescar_productos()

            self.limpiar_producto()

        except ValueError as error:

            messagebox.showerror(
                "Producto",
                str(error)
            )

    def actualizar_producto(self):

        try:

            producto = Producto(
                self.prod_id.get(),
                self.prod_nombre.get(),
                self.prod_precio.get(),
                self.prod_stock.get()
            )

            self.servicio.actualizar_producto(
                producto
            )

            messagebox.showinfo(
                "Producto",
                "Producto actualizado correctamente."
            )

            self.refrescar_productos()

        except ValueError as error:

            messagebox.showerror(
                "Producto",
                str(error)
            )

    def eliminar_producto(self):

        seleccion = self.tabla_productos.selection()

        if not seleccion:

            messagebox.showwarning(
                "Producto",
                "Seleccione un producto."
            )

            return

        confirmar = messagebox.askyesno(
            "Confirmar",
            "¿Desea eliminar el producto seleccionado?"
        )

        if not confirmar:
            return

        valores = self.tabla_productos.item(
            seleccion[0],
            "values"
        )

        try:

            self.servicio.eliminar_producto(
                valores[0]
            )

            self.refrescar_productos()

            self.limpiar_producto()

            messagebox.showinfo(
                "Producto",
                "Producto eliminado correctamente."
            )

        except ValueError as error:

            messagebox.showerror(
                "Producto",
                str(error)
            )

    def al_seleccionar_producto(self, event):

        seleccion = self.tabla_productos.selection()

        if not seleccion:
            return

        valores = self.tabla_productos.item(
            seleccion[0],
            "values"
        )

        self.limpiar_producto()

        self.prod_id.insert(
            0,
            valores[0]
        )

        self.prod_nombre.insert(
            0,
            valores[1]
        )

        self.prod_precio.insert(
            0,
            valores[2]
        )

        self.prod_stock.insert(
            0,
            valores[3]
        )

    def limpiar_producto(self):

        for entrada in [
            self.prod_id,
            self.prod_nombre,
            self.prod_precio,
            self.prod_stock
        ]:

            entrada.delete(
                0,
                "end"
            )

    # =========================================================
    # VENTAS
    # =========================================================

    def _crear_tab_ventas(self):

        self.tab_ventas = tk.Frame(
            self.notebook,
            bg="#f9fbfc"
        )

        self.notebook.add(
            self.tab_ventas,
            text="  Ventas  "
        )

        form = tk.LabelFrame(
            self.tab_ventas,
            text="Registrar venta",
            font=("Segoe UI", 10, "bold"),
            bg="#f9fbfc",
            padx=12,
            pady=12
        )

        form.pack(
            fill="x",
            padx=15,
            pady=15
        )

        tk.Label(
            form,
            text="Producto:",
            bg="#f9fbfc"
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=5
        )

        self.venta_producto = ttk.Combobox(
            form,
            state="readonly",
            width=35
        )

        self.venta_producto.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        tk.Label(
            form,
            text="Cantidad:",
            bg="#f9fbfc"
        ).grid(
            row=0,
            column=2,
            padx=5,
            pady=5
        )

        self.venta_cantidad = ttk.Entry(
            form,
            width=12
        )

        self.venta_cantidad.grid(
            row=0,
            column=3,
            padx=5,
            pady=5
        )

        ttk.Button(
            form,
            text="Registrar venta",
            command=self.registrar_venta
        ).grid(
            row=0,
            column=4,
            padx=10
        )

        self.venta_producto.bind(
            "<<ComboboxSelected>>",
            self.al_seleccionar_producto_venta
        )

        tabla_frame = tk.Frame(
            self.tab_ventas,
            bg="#f9fbfc"
        )

        tabla_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        columnas = (
            "id",
            "producto",
            "cantidad",
            "total",
            "usuario",
            "fecha"
        )

        self.tabla_ventas = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings"
        )

        titulos = {

            "id": "ID",

            "producto": "Producto",

            "cantidad": "Cantidad",

            "total": "Total",

            "usuario": "Usuario",

            "fecha": "Fecha"
        }

        for columna in columnas:

            self.tabla_ventas.heading(
                columna,
                text=titulos[columna]
            )

            self.tabla_ventas.column(
                columna,
                width=130,
                anchor="center"
            )

        self.tabla_ventas.pack(
            fill="both",
            expand=True
        )

    def al_seleccionar_producto_venta(self, event):

        producto = self.venta_producto.get()

        if producto:

            self.venta_cantidad.focus_set()

    def registrar_venta(self):

        seleccionado = self.venta_producto.get()

        if not seleccionado:

            messagebox.showwarning(
                "Venta",
                "Seleccione un producto."
            )

            return

        producto_id = seleccionado.split(
            " - ",
            1
        )[0]

        try:

            venta = self.servicio.registrar_venta(
                producto_id,
                self.venta_cantidad.get(),
                self.usuario_actual.usuario
            )

            messagebox.showinfo(
                "Venta",
                f"Venta registrada correctamente.\n"
                f"Total: ${venta['total']:.2f}"
            )

            self.venta_cantidad.delete(
                0,
                "end"
            )

            self.refrescar_productos()

            self.refrescar_ventas()

        except (ValueError, TypeError) as error:

            messagebox.showerror(
                "Venta",
                str(error)
            )

    # =========================================================
    # USUARIOS
    # =========================================================

    def _crear_tab_usuarios(self):

        self.tab_usuarios = tk.Frame(
            self.notebook,
            bg="#f9fbfc"
        )

        self.notebook.add(
            self.tab_usuarios,
            text="  Usuarios  "
        )

        form = tk.LabelFrame(
            self.tab_usuarios,
            text="Gestión de usuarios",
            font=("Segoe UI", 10, "bold"),
            bg="#f9fbfc",
            padx=12,
            pady=12
        )

        form.pack(
            fill="x",
            padx=15,
            pady=15
        )

        self.usr_id = self._campo(
            form,
            "Identificación:",
            0,
            0
        )

        self.usr_nombre = self._campo(
            form,
            "Nombre:",
            0,
            2
        )

        self.usr_usuario = self._campo(
            form,
            "Usuario:",
            1,
            0
        )

        self.usr_contrasena = self._campo(
            form,
            "Contraseña:",
            1,
            2,
            show="*"
        )

        tk.Label(
            form,
            text="Rol:",
            bg="#f9fbfc"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=5,
            pady=5
        )

        self.usr_rol = ttk.Combobox(
            form,
            values=Usuario.ROLES,
            state="readonly",
            width=28
        )

        self.usr_rol.grid(
            row=2,
            column=1,
            sticky="w",
            padx=5,
            pady=5
        )

        self.usr_rol.set(
            "Cliente"
        )

        # EVENTO <<ComboboxSelected>>
        self.usr_rol.bind(
            "<<ComboboxSelected>>",
            self.al_cambiar_rol
        )

        acciones = tk.Frame(
            form,
            bg="#f9fbfc"
        )

        acciones.grid(
            row=3,
            column=0,
            columnspan=4,
            sticky="w",
            pady=(15, 0)
        )

        ttk.Button(
            acciones,
            text="Registrar",
            command=self.registrar_usuario
        ).pack(
            side="left",
            padx=4
        )

        ttk.Button(
            acciones,
            text="Actualizar",
            command=self.actualizar_usuario
        ).pack(
            side="left",
            padx=4
        )

        ttk.Button(
            acciones,
            text="Eliminar",
            command=self.eliminar_usuario
        ).pack(
            side="left",
            padx=4
        )

        ttk.Button(
            acciones,
            text="Limpiar",
            command=self.limpiar_formulario_usuario
        ).pack(
            side="left",
            padx=4
        )

        # EVENTO <Return>
        self.usr_usuario.bind(
            "<Return>",
            self.al_presionar_enter
        )

        self.usr_contrasena.bind(
            "<Return>",
            self.al_presionar_enter
        )

        # EVENTO <Escape>
        self.usr_id.bind(
            "<Escape>",
            self.al_presionar_escape
        )

        self.usr_nombre.bind(
            "<Escape>",
            self.al_presionar_escape
        )

        self.usr_usuario.bind(
            "<Escape>",
            self.al_presionar_escape
        )

        self.usr_contrasena.bind(
            "<Escape>",
            self.al_presionar_escape
        )

        tabla_frame = tk.Frame(
            self.tab_usuarios,
            bg="#f9fbfc"
        )

        tabla_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        columnas = (
            "id",
            "nombre",
            "usuario",
            "rol"
        )

        self.tabla_usuarios = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings",
            selectmode="browse"
        )

        titulos = {

            "id": "Identificación",

            "nombre": "Nombre",

            "usuario": "Usuario",

            "rol": "Rol"
        }

        for columna in columnas:

            self.tabla_usuarios.heading(
                columna,
                text=titulos[columna]
            )

        self.tabla_usuarios.column(
            "id",
            width=130,
            anchor="center"
        )

        self.tabla_usuarios.column(
            "nombre",
            width=280
        )

        self.tabla_usuarios.column(
            "usuario",
            width=160
        )

        self.tabla_usuarios.column(
            "rol",
            width=150,
            anchor="center"
        )

        scroll = ttk.Scrollbar(
            tabla_frame,
            orient="vertical",
            command=self.tabla_usuarios.yview
        )

        self.tabla_usuarios.configure(
            yscrollcommand=scroll.set
        )

        self.tabla_usuarios.pack(
            side="left",
            fill="both",
            expand=True
        )

        scroll.pack(
            side="right",
            fill="y"
        )

        # EVENTO PRINCIPAL DE SEMANA 16
        self.tabla_usuarios.bind(
            "<<TreeviewSelect>>",
            self.al_seleccionar_usuario
        )

    # =========================================================
    # CALLBACK TREEVIEW
    # =========================================================

    def al_seleccionar_usuario(self, event):

        seleccion = self.tabla_usuarios.selection()

        if not seleccion:
            return

        valores = self.tabla_usuarios.item(
            seleccion[0],
            "values"
        )

        identificador = valores[0]

        usuario = self.servicio.buscar_usuario(
            identificador
        )

        if usuario:

            self.cargar_usuario_en_formulario(
                usuario
            )

    def cargar_usuario_en_formulario(
        self,
        usuario
    ):

        self.limpiar_formulario_usuario()

        self.usr_id.insert(
            0,
            usuario.id
        )

        self.usr_nombre.insert(
            0,
            usuario.nombre
        )

        self.usr_usuario.insert(
            0,
            usuario.usuario
        )

        self.usr_contrasena.insert(
            0,
            usuario.contrasena
        )

        self.usr_rol.set(
            usuario.rol
        )

    # =========================================================
    # CALLBACK ENTER
    # =========================================================

    def al_presionar_enter(self, event):

        self.registrar_usuario()

    # =========================================================
    # CALLBACK ESCAPE
    # =========================================================

    def al_presionar_escape(self, event):

        self.limpiar_formulario_usuario()

        self.tabla_usuarios.selection_remove(
            self.tabla_usuarios.selection()
        )

    # =========================================================
    # CALLBACK COMBOBOX
    # =========================================================

    def al_cambiar_rol(self, event):

        rol = self.usr_rol.get()

        if rol == "Administrador":

            self.usr_rol.configure(
                width=28
            )

    # =========================================================
    # REGISTRAR USUARIO
    # =========================================================

    def registrar_usuario(self):

        try:

            usuario = Usuario(

                self.usr_id.get(),

                self.usr_nombre.get(),

                self.usr_usuario.get(),

                self.usr_contrasena.get(),

                self.usr_rol.get()
            )

            self.servicio.registrar_usuario(
                usuario
            )

            self.refrescar_usuarios()

            self.limpiar_formulario_usuario()

            messagebox.showinfo(
                "Usuarios",
                "Usuario registrado correctamente."
            )

        except ValueError as error:

            messagebox.showerror(
                "Usuarios",
                str(error)
            )

    # =========================================================
    # ACTUALIZAR USUARIO
    # =========================================================

    def actualizar_usuario(self):

        try:

            usuario = Usuario(

                self.usr_id.get(),

                self.usr_nombre.get(),

                self.usr_usuario.get(),

                self.usr_contrasena.get(),

                self.usr_rol.get()
            )

            self.servicio.actualizar_usuario(
                usuario
            )

            self.refrescar_usuarios()

            messagebox.showinfo(
                "Usuarios",
                "Usuario actualizado correctamente."
            )

        except ValueError as error:

            messagebox.showerror(
                "Usuarios",
                str(error)
            )

    # =========================================================
    # ELIMINAR USUARIO
    # =========================================================

    def eliminar_usuario(self):

        seleccion = self.tabla_usuarios.selection()

        if not seleccion:

            messagebox.showwarning(
                "Usuarios",
                "Seleccione un usuario."
            )

            return

        valores = self.tabla_usuarios.item(
            seleccion[0],
            "values"
        )

        identificador = valores[0]

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Está seguro de eliminar el usuario seleccionado?"
        )

        if not confirmar:
            return

        try:

            self.servicio.eliminar_usuario(
                identificador,
                self.usuario_actual
            )

            self.refrescar_usuarios()

            self.limpiar_formulario_usuario()

            messagebox.showinfo(
                "Usuarios",
                "Usuario eliminado correctamente."
            )

        except ValueError as error:

            messagebox.showerror(
                "Usuarios",
                str(error)
            )

    # =========================================================
    # LIMPIAR USUARIO
    # =========================================================

    def limpiar_formulario_usuario(self):

        for entrada in [

            self.usr_id,

            self.usr_nombre,

            self.usr_usuario,

            self.usr_contrasena

        ]:

            entrada.delete(
                0,
                "end"
            )

        self.usr_rol.set(
            "Cliente"
        )

        if hasattr(
            self,
            "tabla_usuarios"
        ):

            self.tabla_usuarios.selection_remove(
                self.tabla_usuarios.selection()
            )

    # =========================================================
    # CAMPO
    # =========================================================

    def _campo(
        self,
        parent,
        texto,
        fila,
        columna,
        show=None
    ):

        tk.Label(
            parent,
            text=texto,
            bg="#f9fbfc"
        ).grid(
            row=fila,
            column=columna,
            sticky="w",
            padx=5,
            pady=5
        )

        entrada = ttk.Entry(
            parent,
            width=30,
            show=show
        )

        entrada.grid(
            row=fila,
            column=columna + 1,
            sticky="w",
            padx=5,
            pady=5
        )

        return entrada

    # =========================================================
    # ACTUALIZAR TABLAS
    # =========================================================

    def refrescar_todo(self):

        self.refrescar_productos()

        self.refrescar_ventas()

        if self.usuario_actual.rol == "Administrador":

            self.refrescar_usuarios()

    def refrescar_productos(self):

        if not hasattr(
            self,
            "tabla_productos"
        ):
            return

        for item in self.tabla_productos.get_children():

            self.tabla_productos.delete(
                item
            )

        for producto in self.servicio.listar_productos():

            self.tabla_productos.insert(
                "",
                "end",
                values=(
                    producto.id,
                    producto.nombre,
                    f"{producto.precio:.2f}",
                    producto.stock
                )
            )

        self._actualizar_combo_productos_venta()

    def refrescar_ventas(self):

        if not hasattr(
            self,
            "tabla_ventas"
        ):
            return

        for item in self.tabla_ventas.get_children():

            self.tabla_ventas.delete(
                item
            )

        for venta in self.servicio.listar_ventas():

            self.tabla_ventas.insert(
                "",
                "end",
                values=(

                    venta.get(
                        "id",
                        ""
                    ),

                    venta.get(
                        "producto",
                        ""
                    ),

                    venta.get(
                        "cantidad",
                        ""
                    ),

                    f"${float(venta.get('total', 0)):.2f}",

                    venta.get(
                        "usuario",
                        ""
                    ),

                    venta.get(
                        "fecha",
                        ""
                    )
                )
            )

    def refrescar_usuarios(self):

        if not hasattr(
            self,
            "tabla_usuarios"
        ):
            return

        for item in self.tabla_usuarios.get_children():

            self.tabla_usuarios.delete(
                item
            )

        for usuario in self.servicio.listar_usuarios():

            self.tabla_usuarios.insert(
                "",
                "end",
                values=(

                    usuario.id,

                    usuario.nombre,

                    usuario.usuario,

                    usuario.rol
                )
            )

    def _actualizar_combo_productos_venta(self):

        if not hasattr(
            self,
            "venta_producto"
        ):
            return

        valores = []

        for producto in self.servicio.listar_productos():

            if producto.stock > 0:

                valores.append(
                    f"{producto.id} - {producto.nombre}"
                )

        self.venta_producto["values"] = valores

        if self.venta_producto.get() not in valores:

            self.venta_producto.set("")
