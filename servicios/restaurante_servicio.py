from pathlib import Path
from datetime import datetime

from modelos.usuario import Usuario
from modelos.producto import Producto
from servicios.archivo_servicio import ArchivoServicio


class RestauranteServicio:
    """Centraliza validaciones, reglas y persistencia."""

    def __init__(self, base_dir):

        base_dir = Path(base_dir)

        datos = base_dir / "datos"

        self.usuarios_archivo = ArchivoServicio(
            datos / "usuarios.json"
        )

        self.productos_archivo = ArchivoServicio(
            datos / "productos.json"
        )

        self.ventas_archivo = ArchivoServicio(
            datos / "ventas.json"
        )

    # =========================================================
    # AUTENTICACIÓN
    # =========================================================

    def autenticar(self, usuario, contrasena):

        usuario = usuario.strip()

        for data in self.usuarios_archivo.cargar():

            if (
                data.get("usuario") == usuario
                and data.get("contrasena") == contrasena
            ):
                return Usuario.from_dict(data)

        return None

    # =========================================================
    # USUARIOS
    # =========================================================

    def listar_usuarios(self):

        return [
            Usuario.from_dict(data)
            for data in self.usuarios_archivo.cargar()
        ]

    def buscar_usuario(self, identificador):

        for usuario in self.listar_usuarios():

            if usuario.id == str(identificador):
                return usuario

        return None

    def usuario_existente(
        self,
        usuario_login,
        excluir_id=None
    ):

        usuario_login = usuario_login.strip().lower()

        for usuario in self.listar_usuarios():

            if (
                excluir_id is not None
                and usuario.id == str(excluir_id)
            ):
                continue

            if usuario.usuario.lower() == usuario_login:
                return usuario

        return None

    def registrar_usuario(self, usuario):

        self._validar_usuario(usuario)

        usuarios = self.usuarios_archivo.cargar()

        if self.buscar_usuario(usuario.id):

            raise ValueError(
                "Ya existe un usuario con ese identificador."
            )

        if self.usuario_existente(usuario.usuario):

            raise ValueError(
                "El nombre de usuario ya está registrado."
            )

        usuarios.append(usuario.to_dict())

        self.usuarios_archivo.guardar(usuarios)

    def actualizar_usuario(self, usuario):

        self._validar_usuario(usuario)

        usuarios = self.usuarios_archivo.cargar()

        encontrado = False

        for i, data in enumerate(usuarios):

            if str(data.get("id")) == usuario.id:

                if self.usuario_existente(
                    usuario.usuario,
                    excluir_id=usuario.id
                ):
                    raise ValueError(
                        "El nombre de usuario ya está registrado."
                    )

                usuarios[i] = usuario.to_dict()

                encontrado = True

                break

        if not encontrado:

            raise ValueError(
                "No se encontró el usuario."
            )

        self.usuarios_archivo.guardar(usuarios)

    def eliminar_usuario(
        self,
        identificador,
        usuario_actual
    ):

        if str(identificador) == str(usuario_actual.id):

            raise ValueError(
                "No puede eliminar la cuenta del administrador "
                "que está autenticado."
            )

        usuarios = self.usuarios_archivo.cargar()

        nuevos = [
            usuario
            for usuario in usuarios
            if str(usuario.get("id"))
            != str(identificador)
        ]

        if len(nuevos) == len(usuarios):

            raise ValueError(
                "No se encontró el usuario seleccionado."
            )

        self.usuarios_archivo.guardar(nuevos)

    def _validar_usuario(self, usuario):

        if not all(
            [
                usuario.id,
                usuario.nombre,
                usuario.usuario,
                usuario.contrasena,
                usuario.rol
            ]
        ):

            raise ValueError(
                "Complete todos los campos del usuario."
            )

        if usuario.rol not in Usuario.ROLES:

            raise ValueError(
                "Seleccione un rol válido."
            )

        if len(usuario.contrasena) < 4:

            raise ValueError(
                "La contraseña debe tener al menos 4 caracteres."
            )

    # =========================================================
    # PRODUCTOS
    # =========================================================

    def listar_productos(self):

        return [
            Producto.from_dict(data)
            for data in self.productos_archivo.cargar()
        ]

    def buscar_producto(self, identificador):

        for producto in self.listar_productos():

            if producto.id == str(identificador):

                return producto

        return None

    def registrar_producto(self, producto):

        if not producto.id or not producto.nombre:

            raise ValueError(
                "Complete los datos del producto."
            )

        if producto.precio < 0 or producto.stock < 0:

            raise ValueError(
                "Precio y stock no pueden ser negativos."
            )

        productos = self.productos_archivo.cargar()

        if self.buscar_producto(producto.id):

            raise ValueError(
                "Ya existe un producto con ese identificador."
            )

        productos.append(producto.to_dict())

        self.productos_archivo.guardar(productos)

    def actualizar_producto(self, producto):

        productos = self.productos_archivo.cargar()

        for i, data in enumerate(productos):

            if str(data.get("id")) == producto.id:

                productos[i] = producto.to_dict()

                self.productos_archivo.guardar(productos)

                return

        raise ValueError(
            "No se encontró el producto."
        )

    def eliminar_producto(self, identificador):

        productos = self.productos_archivo.cargar()

        nuevos = [
            producto
            for producto in productos
            if str(producto.get("id"))
            != str(identificador)
        ]

        if len(nuevos) == len(productos):

            raise ValueError(
                "No se encontró el producto."
            )

        self.productos_archivo.guardar(nuevos)

    # =========================================================
    # VENTAS
    # =========================================================

    def listar_ventas(self):

        return self.ventas_archivo.cargar()

    def registrar_venta(
        self,
        producto_id,
        cantidad,
        usuario_login
    ):

        producto = self.buscar_producto(producto_id)

        if not producto:

            raise ValueError(
                "Seleccione un producto válido."
            )

        cantidad = int(cantidad)

        if cantidad <= 0:

            raise ValueError(
                "La cantidad debe ser mayor que cero."
            )

        if cantidad > producto.stock:

            raise ValueError(
                "No existe stock suficiente."
            )

        producto.stock -= cantidad

        self.actualizar_producto(producto)

        ventas = self.ventas_archivo.cargar()

        nuevo_id = f"V{len(ventas) + 1:03d}"

        venta = {

            "id": nuevo_id,

            "producto_id": producto.id,

            "producto": producto.nombre,

            "cantidad": cantidad,

            "total": round(
                producto.precio * cantidad,
                2
            ),

            "usuario": usuario_login,

            "fecha": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

        ventas.append(venta)

        self.ventas_archivo.guardar(ventas)

        return venta
