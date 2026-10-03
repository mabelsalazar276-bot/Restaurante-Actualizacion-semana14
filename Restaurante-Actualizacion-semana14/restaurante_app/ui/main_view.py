import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable

from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.restaurante_servicio import RestauranteServicio


class MainView(ttk.Frame):
    """Panel principal para consultar usuarios y productos."""

    def __init__(
        self,
        master: tk.Misc,
        servicio: RestauranteServicio,
        usuario: Usuario,
        cerrar_sesion: Callable[[], None],
    ) -> None:
        super().__init__(master, padding=24)
        self.servicio = servicio
        self.usuario = usuario
        self.cerrar_sesion = cerrar_sesion
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        self._crear_variables_producto()

        encabezado = ttk.Frame(self)
        encabezado.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        encabezado.columnconfigure(0, weight=1)
        ttk.Label(encabezado, text="Sabores de Casa By Mabela", foreground="#29352f", font=("Segoe UI", 22, "bold")).grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(encabezado, text=f"Sesion: {usuario.nombre_usuario}", foreground="#6c756e").grid(
            row=0, column=1, padx=16
        )
        ttk.Button(encabezado, text="Cerrar sesión", command=self.cerrar_sesion).grid(
            row=0, column=2
        )

        menu = ttk.Frame(self)
        menu.grid(row=1, column=0, sticky="ns", padx=(0, 24))
        ttk.Label(menu, text="SECCIONES", foreground="#6c756e", font=("Segoe UI", 9, "bold")).pack(
            anchor="w", pady=(0, 8)
        )
        ttk.Button(menu, text="Productos", command=self.mostrar_productos).pack(fill="x", pady=2)
        ttk.Button(menu, text="Usuarios", command=self.mostrar_usuarios).pack(fill="x", pady=2)
        ttk.Button(menu, text="Ventas (pendiente)", state="disabled").pack(fill="x", pady=2)

        self.contenido = ttk.Frame(self)
        self.contenido.grid(row=1, column=1, sticky="nsew")
        self.contenido.columnconfigure(0, weight=1)
        self.contenido.rowconfigure(1, weight=1)
        self.mostrar_productos()

    def _limpiar_contenido(self) -> None:
        for widget in self.contenido.winfo_children():
            widget.destroy()

    def mostrar_productos(self) -> None:
        self._limpiar_contenido()
        self.contenido.columnconfigure(0, weight=1)
        self.contenido.rowconfigure(2, weight=1)
        ttk.Label(
            self.contenido,
            text="Productos registrados",
            foreground="#1f2937",
            font=("Segoe UI", 16, "bold"),
        ).grid(row=0, column=0, sticky="w", pady=(0, 12))
        self._crear_formulario_producto()
        self._crear_tabla_productos()
        self._refrescar_tabla_productos()

    def _crear_variables_producto(self) -> None:
        self.id_producto_var = tk.StringVar()
        self.nombre_producto_var = tk.StringVar()
        self.precio_producto_var = tk.StringVar()
        self.categoria_producto_var = tk.StringVar()
        self.stock_producto_var = tk.StringVar()

    def _crear_formulario_producto(self) -> None:
        formulario = ttk.LabelFrame(self.contenido, text="Datos del producto", padding=12)
        formulario.grid(row=1, column=0, sticky="ew", pady=(0, 16))
        for columna in range(5):
            formulario.columnconfigure(columna, weight=1)

        campos = (
            ("ID", self.id_producto_var, 0),
            ("Nombre", self.nombre_producto_var, 1),
            ("Precio", self.precio_producto_var, 2),
            ("Categoría", self.categoria_producto_var, 3),
            ("Stock", self.stock_producto_var, 4),
        )
        for etiqueta, variable, columna in campos:
            ttk.Label(formulario, text=etiqueta).grid(row=0, column=columna, sticky="w", padx=4)
            ttk.Entry(formulario, textvariable=variable).grid(
                row=1, column=columna, sticky="ew", padx=4, pady=(4, 0)
            )

        acciones = ttk.Frame(formulario)
        acciones.grid(row=2, column=0, columnspan=5, sticky="ew", pady=(12, 0))
        ttk.Button(acciones, text="Registrar", command=self._registrar_producto).pack(side="left", padx=(0, 6))
        ttk.Button(acciones, text="Cargar / Consultar", command=self._consultar_producto).pack(side="left", padx=6)
        ttk.Button(acciones, text="Actualizar", command=self._actualizar_producto).pack(side="left", padx=6)
        ttk.Button(acciones, text="Eliminar", command=self._eliminar_producto).pack(side="left", padx=6)
        ttk.Button(acciones, text="Limpiar", command=self._limpiar_formulario_producto).pack(side="right")

    def _crear_tabla_productos(self) -> None:
        contenedor = ttk.Frame(self.contenido)
        contenedor.grid(row=2, column=0, sticky="nsew")
        contenedor.columnconfigure(0, weight=1)
        contenedor.rowconfigure(0, weight=1)
        self.tabla_productos = ttk.Treeview(
            contenedor,
            columns=("id", "nombre", "categoria", "precio", "stock"),
            show="headings",
            height=12,
        )
        for columna, encabezado in zip(
            ("id", "nombre", "categoria", "precio", "stock"),
            ("ID", "Nombre", "Categoría", "Precio", "Cantidad"),
        ):
            self.tabla_productos.heading(columna, text=encabezado)
            self.tabla_productos.column(columna, width=120, anchor="center")
        self.tabla_productos.grid(row=0, column=0, sticky="nsew")
        barra = ttk.Scrollbar(contenedor, orient="vertical", command=self.tabla_productos.yview)
        barra.grid(row=0, column=1, sticky="ns")
        self.tabla_productos.configure(yscrollcommand=barra.set)

    def _refrescar_tabla_productos(self) -> None:
        for fila in self.tabla_productos.get_children():
            self.tabla_productos.delete(fila)
        for producto in self.servicio.listar_productos():
            self.tabla_productos.insert(
                "",
                "end",
                values=(
                    producto.id_producto,
                    producto.nombre,
                    producto.categoria,
                    f"${producto.precio:.2f}",
                    producto.stock,
                ),
            )

    def _datos_producto(self) -> tuple[int, str, float, str, int]:
        return (
            int(self.id_producto_var.get().strip()),
            self.nombre_producto_var.get(),
            float(self.precio_producto_var.get().strip()),
            self.categoria_producto_var.get(),
            int(self.stock_producto_var.get().strip()),
        )

    def _registrar_producto(self) -> None:
        try:
            self.servicio.registrar_producto(*self._datos_producto())
            self._refrescar_tabla_productos()
            self._limpiar_formulario_producto()
            messagebox.showinfo("Producto registrado", "El producto se guardó correctamente.")
        except (ValueError, OSError) as error:
            messagebox.showerror("No se pudo registrar", str(error))

    def _consultar_producto(self) -> None:
        try:
            producto = self.servicio.buscar_producto(int(self.id_producto_var.get().strip()))
            if producto is None:
                raise ValueError("No existe un producto con ese identificador.")
            self._mostrar_producto_en_formulario(producto)
        except ValueError as error:
            messagebox.showerror("Consulta no disponible", str(error))

    def _actualizar_producto(self) -> None:
        try:
            self.servicio.actualizar_producto(*self._datos_producto())
            self._refrescar_tabla_productos()
            messagebox.showinfo("Producto actualizado", "Los cambios se guardaron correctamente.")
        except (ValueError, OSError) as error:
            messagebox.showerror("No se pudo actualizar", str(error))

    def _eliminar_producto(self) -> None:
        try:
            id_producto = int(self.id_producto_var.get().strip())
            self.servicio.eliminar_producto(id_producto)
            self._refrescar_tabla_productos()
            self._limpiar_formulario_producto()
            messagebox.showinfo("Producto eliminado", "El producto dejó de estar disponible.")
        except (ValueError, OSError) as error:
            messagebox.showerror("No se pudo eliminar", str(error))

    def _mostrar_producto_en_formulario(self, producto: Producto) -> None:
        self.nombre_producto_var.set(producto.nombre)
        self.precio_producto_var.set(str(producto.precio))
        self.categoria_producto_var.set(producto.categoria)
        self.stock_producto_var.set(str(producto.stock))

    def _limpiar_formulario_producto(self) -> None:
        for variable in (
            self.id_producto_var,
            self.nombre_producto_var,
            self.precio_producto_var,
            self.categoria_producto_var,
            self.stock_producto_var,
        ):
            variable.set("")

    def mostrar_usuarios(self) -> None:
        self._limpiar_contenido()
        self.contenido.columnconfigure(0, weight=1)
        self.contenido.rowconfigure(1, weight=1)
        encabezado = ttk.Frame(self.contenido)
        encabezado.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        encabezado.columnconfigure(0, weight=1)
        ttk.Label(
            encabezado,
            text="Usuarios registrados",
            foreground="#1f2937",
            font=("Segoe UI", 16, "bold"),
        ).grid(row=0, column=0, sticky="w")
        ttk.Button(
            encabezado,
            text="+ Agregar usuario",
            command=self._abrir_registro_usuario,
        ).grid(row=0, column=1, sticky="e")

        columnas = (
            "id", "nombre", "apellido", "nombre_usuario", "correo",
            "fecha_nacimiento", "rango",
        )
        tabla = ttk.Treeview(self.contenido, columns=columnas, show="headings", height=14)
        encabezados = (
            "ID", "Nombre", "Apellido", "Usuario", "Correo electrónico",
            "Nacimiento", "Puesto",
        )
        for columna, titulo in zip(columnas, encabezados):
            tabla.heading(columna, text=titulo)
            tabla.column(columna, width=130, anchor="center")
        tabla.grid(row=1, column=0, sticky="nsew")
        barra = ttk.Scrollbar(self.contenido, orient="vertical", command=tabla.yview)
        barra.grid(row=1, column=1, sticky="ns")
        tabla.configure(yscrollcommand=barra.set)
        for usuario in self.servicio.listar_usuarios():
            tabla.insert(
                "",
                "end",
                values=(
                    usuario.id_usuario,
                    usuario.nombre,
                    usuario.apellido,
                    usuario.nombre_usuario,
                    usuario.correo_electronico,
                    usuario.fecha_nacimiento,
                    usuario.rango,
                ),
            )

    def _abrir_registro_usuario(self) -> None:
        ventana = tk.Toplevel(self)
        ventana.title("Agregar usuario")
        ventana.transient(self.winfo_toplevel())
        ventana.resizable(False, False)
        ventana.grab_set()

        formulario = ttk.Frame(ventana, padding=22)
        formulario.grid(row=0, column=0, sticky="nsew")
        formulario.columnconfigure(0, weight=1)
        ttk.Label(
            formulario,
            text="Registrar nuevo usuario",
            font=("Segoe UI", 16, "bold"),
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 14))

        campos = (
            ("Nombre", "nombre"),
            ("Apellido", "apellido"),
            ("Nombre de usuario", "nombre_usuario"),
            ("Correo electrónico", "correo"),
            ("Contraseña", "contrasena"),
            ("Fecha de nacimiento (AAAA-MM-DD)", "fecha_nacimiento"),
        )
        variables = {clave: tk.StringVar() for _, clave in campos}
        for indice, (etiqueta, clave) in enumerate(campos):
            fila = indice + 1
            ttk.Label(formulario, text=etiqueta).grid(
                row=fila * 2 - 1, column=0, columnspan=2, sticky="w",
                pady=(4, 3),
            )
            ttk.Entry(
                formulario,
                textvariable=variables[clave],
                show="*" if clave == "contrasena" else "",
                width=38,
            ).grid(row=fila * 2, column=0, columnspan=2, sticky="ew")

        fila_puesto = len(campos) * 2 + 1
        ttk.Label(formulario, text="Puesto").grid(
            row=fila_puesto, column=0, columnspan=2, sticky="w",
            pady=(10, 3),
        )
        puesto_var = tk.StringVar(value="Mesero/a")
        ttk.Combobox(
            formulario,
            textvariable=puesto_var,
            values=(
                "Cocinero/a",
                "Cajero/a",
                "Mesero/a",
                "Encargado/a",
                "Bartender",
                "Anfitrión/a",
                "Personal de limpieza",
                "Otro",
            ),
            state="readonly",
        ).grid(row=fila_puesto + 1, column=0, columnspan=2, sticky="ew")

        def guardar_usuario() -> None:
            datos = {clave: variable.get().strip() for clave, variable in variables.items()}
            if any(not valor for valor in datos.values()):
                messagebox.showwarning(
                    "Datos incompletos",
                    "Completa todos los campos antes de registrar el usuario.",
                    parent=ventana,
                )
                return
            try:
                self.servicio.registrar_usuario(
                    nombre=datos["nombre"],
                    apellido=datos["apellido"],
                    nombre_usuario=datos["nombre_usuario"],
                    contrasena=datos["contrasena"],
                    correo_electronico=datos["correo"],
                    fecha_nacimiento=datos["fecha_nacimiento"],
                    rango=puesto_var.get(),
                )
            except ValueError as error:
                messagebox.showerror("No se pudo registrar", str(error), parent=ventana)
                return
            except OSError as error:
                messagebox.showerror("Error al guardar", str(error), parent=ventana)
                return

            ventana.destroy()
            self.mostrar_usuarios()
            messagebox.showinfo(
                "Usuario registrado",
                "El nuevo usuario ya aparece en la lista y puede iniciar sesión.",
                parent=self.winfo_toplevel(),
            )

        ttk.Button(
            formulario, text="Guardar usuario", command=guardar_usuario,
        ).grid(
            row=fila_puesto + 2, column=0, columnspan=2, sticky="ew",
            pady=(16, 6),
        )
        ttk.Button(
            formulario, text="Cancelar", command=ventana.destroy,
        ).grid(row=fila_puesto + 3, column=0, columnspan=2, sticky="ew")

    def _mostrar_tabla(
        self,
        titulo: str,
        columnas: tuple[str, ...],
        encabezados: tuple[str, ...],
        filas: list[tuple[object, ...]],
    ) -> None:
        self._limpiar_contenido()
        ttk.Label(self.contenido, text=titulo, foreground="#1f2937", font=("Segoe UI", 16, "bold")).grid(
            row=0, column=0, sticky="w", pady=(0, 12)
        )
        tabla = ttk.Treeview(self.contenido, columns=columnas, show="headings", height=14)
        for columna, encabezado in zip(columnas, encabezados):
            tabla.heading(columna, text=encabezado)
            tabla.column(columna, width=130, anchor="center")
        tabla.grid(row=1, column=0, sticky="nsew")
        barra = ttk.Scrollbar(self.contenido, orient="vertical", command=tabla.yview)
        barra.grid(row=1, column=1, sticky="ns")
        tabla.configure(yscrollcommand=barra.set)
        for fila in filas:
            tabla.insert("", "end", values=fila)
