class Usuario:
    """Modelo de datos para un usuario del sistema."""

    ROLES = ("Administrador", "Empleado", "Cliente")

    def __init__(self, id, nombre, usuario, contrasena, rol):
        self.id = str(id).strip()
        self.nombre = str(nombre).strip()
        self.usuario = str(usuario).strip()
        self.contrasena = str(contrasena)
        self.rol = str(rol).strip()

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "usuario": self.usuario,
            "contrasena": self.contrasena,
            "rol": self.rol
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get("id", ""),
            data.get("nombre", ""),
            data.get("usuario", ""),
            data.get("contrasena", ""),
            data.get("rol", "Cliente")
        )
