from typing import List, Optional

from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio


class RestauranteServicio:
    """Fachada de datos y reglas necesarias para la primera interfaz gráfica."""

    def __init__(self, archivo_servicio: type[ArchivoServicio] = ArchivoServicio) -> None:
        self._archivo_servicio = archivo_servicio
        self._productos: List[Producto] = []
        self._usuarios: List[Usuario] = []

    def cargar_datos(self) -> None:
        self._productos = self._archivo_servicio.cargar_productos()
        self._usuarios = self._archivo_servicio.cargar_usuarios()

    def validar_acceso(self, nombre_usuario: str, contrasena: str) -> Optional[Usuario]:
        """Valida el acceso comparando el nombre de usuario y su contraseña."""
        nombre_usuario_normalizado = nombre_usuario.strip().lower()
        for usuario in self._usuarios:
            if (
                usuario.nombre_usuario.lower() == nombre_usuario_normalizado
                and usuario.contrasena == contrasena.strip()
            ):
                return usuario
        return None

    def listar_productos(self) -> List[Producto]:
        return list(self._productos)

    def recargar_productos(self) -> List[Producto]:
        self._productos = self._archivo_servicio.cargar_productos()
        return self.listar_productos()

    def registrar_producto(
        self,
        id_producto: int,
        nombre: str,
        precio: float,
        categoria: str,
        stock: int,
    ) -> Producto:
        if any(producto.id_producto == int(id_producto) for producto in self._productos):
            raise ValueError("Ya existe un producto con ese identificador.")

        producto = Producto(id_producto, nombre, precio, categoria, stock)
        self._productos.append(producto)
        self._guardar_productos()
        return producto

    def buscar_producto(self, id_producto: int) -> Optional[Producto]:
        id_buscado = int(id_producto)
        return next(
            (producto for producto in self._productos if producto.id_producto == id_buscado),
            None,
        )

    def actualizar_producto(
        self,
        id_producto: int,
        nombre: str,
        precio: float,
        categoria: str,
        stock: int,
    ) -> Producto:
        producto = self.buscar_producto(id_producto)
        if producto is None:
            raise ValueError("No existe un producto con ese identificador.")

        producto_actualizado = Producto(id_producto, nombre, precio, categoria, stock)
        posicion = self._productos.index(producto)
        self._productos[posicion] = producto_actualizado
        self._guardar_productos()
        return producto_actualizado

    def eliminar_producto(self, id_producto: int) -> None:
        producto = self.buscar_producto(id_producto)
        if producto is None:
            raise ValueError("No existe un producto con ese identificador.")

        self._productos.remove(producto)
        self._guardar_productos()

    def _guardar_productos(self) -> None:
        if not self._archivo_servicio.guardar_productos(self._productos):
            raise OSError("No se pudo guardar el catálogo de productos.")

    def listar_usuarios(self) -> List[Usuario]:
        return list(self._usuarios)

    def cantidad_productos(self) -> int:
        return len(self._productos)

    def cantidad_usuarios(self) -> int:
        return len(self._usuarios)
