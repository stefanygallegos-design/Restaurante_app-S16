class Venta:
    """Modelo para registrar una venta."""

    def __init__(self, id, producto_id, producto, cantidad, total, usuario):
        self.id = str(id)
        self.producto_id = str(producto_id)
        self.producto = str(producto)
        self.cantidad = int(cantidad)
        self.total = float(total)
        self.usuario = str(usuario)

    def to_dict(self):
        return {
            "id": self.id,
            "producto_id": self.producto_id,
            "producto": self.producto,
            "cantidad": self.cantidad,
            "total": self.total,
            "usuario": self.usuario
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get("id", ""),
            data.get("producto_id", ""),
            data.get("producto", ""),
            data.get("cantidad", 0),
            data.get("total", 0),
            data.get("usuario", "")
        )
