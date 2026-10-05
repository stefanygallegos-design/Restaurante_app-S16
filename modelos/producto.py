class Producto:
    """Modelo de datos para un producto."""

    def __init__(self, id, nombre, precio, stock):
        self.id = str(id).strip()
        self.nombre = str(nombre).strip()
        self.precio = float(precio)
        self.stock = int(stock)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get("id", ""),
            data.get("nombre", ""),
            data.get("precio", 0),
            data.get("stock", 0)
        )
