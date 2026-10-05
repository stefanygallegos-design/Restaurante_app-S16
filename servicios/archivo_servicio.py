import json
from pathlib import Path


class ArchivoServicio:
    """Servicio para leer y guardar información en archivos JSON."""

    def __init__(self, ruta):
        self.ruta = Path(ruta)
        self.ruta.parent.mkdir(parents=True, exist_ok=True)

        if not self.ruta.exists():
            self.guardar([])

    def cargar(self):
        try:
            with self.ruta.open("r", encoding="utf-8") as archivo:
                datos = json.load(archivo)

                if isinstance(datos, list):
                    return datos

                return []

        except (json.JSONDecodeError, OSError):
            return []

    def guardar(self, datos):
        with self.ruta.open("w", encoding="utf-8") as archivo:
            json.dump(
                datos,
                archivo,
                indent=4,
                ensure_ascii=False
            )
