import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable

from modelos.usuario import Usuario
from servicios.restaurante_servicio import RestauranteServicio


class LoginView(ttk.Frame):
    """Pantalla de acceso y registro de usuarios."""

    def __init__(
        self,
        master: tk.Misc,
        servicio: RestauranteServicio,
        al_ingresar: Callable[[Usuario], None],
    ) -> None:
        super().__init__(master, padding=24)
        self.servicio = servicio
        self.al_ingresar = al_ingresar
        estilos = ttk.Style(self)
        estilos.configure("Acceso.TFrame", background="#f3f5f1")
        estilos.configure("Tarjeta.TFrame", background="#ffffff")
        estilos.configure("Marca.TFrame", background="#23463d")
        estilos.configure("MarcaTitulo.TLabel", background="#23463d", foreground="#ffffff")
        estilos.configure("MarcaTexto.TLabel", background="#23463d", foreground="#d7e5dc")
        estilos.configure("Acceso.TLabel", background="#ffffff", foreground="#253b34")
        estilos.configure("Ayuda.TLabel", background="#ffffff", foreground="#718078")
        estilos.configure("Acceso.TButton", padding=(12, 9), font=("Segoe UI", 10, "bold"))
        estilos.map(
            "Acceso.TButton",
            background=[("!disabled", "#b85c45"), ("active", "#984832")],
            foreground=[("!disabled", "#ffffff")],
        )
        estilos.configure("Secundario.TButton", padding=(10, 7))

        self.configure(style="Acceso.TFrame", padding=28)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        contenedor = ttk.Frame(self, style="Acceso.TFrame")
        contenedor.grid(row=0, column=0)

        marca = ttk.Frame(contenedor, style="Marca.TFrame", padding=(32, 42))
        marca.grid(row=0, column=0, sticky="nsew")
        ttk.Label(
            marca, text="Sabores de Casa\nBy Mabela", style="MarcaTitulo.TLabel",
            font=("Segoe UI", 21, "bold"), justify="left",
        ).pack(anchor="w")
        ttk.Label(
            marca,
            text="Una experiencia sencilla\npara gestionar tu restaurante.",
            style="MarcaTexto.TLabel",
            font=("Segoe UI", 10),
            justify="left",
        ).pack(anchor="w", pady=(14, 0))

        self.tarjeta = ttk.Frame(contenedor, style="Tarjeta.TFrame", padding=(34, 26))
        self.tarjeta.grid(row=0, column=1, sticky="nsew")
        self.tarjeta.columnconfigure(0, weight=1)
        self.contenido = ttk.Frame(self.tarjeta, style="Tarjeta.TFrame")
        self.contenido.grid(row=0, column=0, sticky="nsew")
        self.contenido.columnconfigure(0, weight=1)
        self._mostrar_acceso()

    def _encabezado_formulario(self, titulo: str, subtitulo: str) -> None:
        ttk.Label(
            self.contenido,
            text=titulo,
            style="Acceso.TLabel",
            font=("Segoe UI", 19, "bold"),
        ).grid(row=0, column=0, sticky="w")
        ttk.Label(
            self.contenido, text=subtitulo, style="Ayuda.TLabel",
            font=("Segoe UI", 9),
        ).grid(row=1, column=0, sticky="w", pady=(4, 20))

    def _crear_campo(
        self,
        contenedor: ttk.Frame,
        etiqueta: str,
        variable: tk.StringVar,
        fila: int,
        columna: int = 0,
        *,
        oculto: bool = False,
        ancho: int = 30,
    ) -> ttk.Entry:
        ttk.Label(contenedor, text=etiqueta, style="Acceso.TLabel").grid(
            row=fila, column=columna, sticky="w", pady=(0, 5)
        )
        campo = ttk.Entry(
            contenedor, textvariable=variable, width=ancho,
            show="*" if oculto else "",
        )
        campo.grid(row=fila + 1, column=columna, sticky="ew", padx=(0, 12), pady=(0, 12))
        return campo

    def _mostrar_acceso(self) -> None:
        for widget in self.contenido.winfo_children():
            widget.destroy()
        self.contenido.columnconfigure(0, weight=1)
        self._encabezado_formulario("Bienvenido", "Inicia sesión para continuar")
        self.usuario_var = tk.StringVar()
        self.contrasena_var = tk.StringVar()
        usuario_entry = self._crear_campo(
            self.contenido, "Usuario", self.usuario_var, 2, ancho=34
        )
        contrasena_entry = self._crear_campo(
            self.contenido, "Contraseña", self.contrasena_var, 4,
            oculto=True, ancho=34,
        )
        ttk.Button(
            self.contenido, text="Ingresar al panel",
            command=self._intentar_ingreso,
            style="Acceso.TButton",
        ).grid(row=6, column=0, sticky="ew", pady=(2, 10))
        ttk.Label(
            self.contenido, text="Demo: sofia  ·  menu2026",
            style="Ayuda.TLabel", font=("Segoe UI", 9),
        ).grid(row=7, column=0, pady=(0, 12))
        ttk.Button(
            self.contenido, text="Crear una cuenta nueva",
            command=self._mostrar_registro, style="Secundario.TButton",
        ).grid(row=8, column=0, sticky="ew")
        usuario_entry.focus_set()
        contrasena_entry.bind("<Return>", lambda _evento: self._intentar_ingreso())

    def _mostrar_registro(self) -> None:
        for widget in self.contenido.winfo_children():
            widget.destroy()
        self.contenido.columnconfigure(0, weight=1)
        self.contenido.columnconfigure(1, weight=1)
        self._encabezado_formulario(
            "Crear cuenta", "Completa tus datos para registrarte"
        )
        self.registro_vars = {
            "nombre": tk.StringVar(),
            "apellido": tk.StringVar(),
            "nombre_usuario": tk.StringVar(),
            "correo": tk.StringVar(),
            "contrasena": tk.StringVar(),
            "fecha_nacimiento": tk.StringVar(),
        }
        formulario = ttk.Frame(self.contenido, style="Tarjeta.TFrame")
        formulario.grid(row=2, column=0, columnspan=2, sticky="ew")
        formulario.columnconfigure(0, weight=1)
        formulario.columnconfigure(1, weight=1)
        campos = (
            ("Nombre", "nombre", 0, 0, False),
            ("Apellido", "apellido", 0, 1, False),
            ("Nombre de usuario", "nombre_usuario", 2, 0, False),
            ("Correo electrónico", "correo", 2, 1, False),
            ("Contraseña", "contrasena", 4, 0, True),
            ("Fecha de nacimiento (AAAA-MM-DD)", "fecha_nacimiento", 4, 1, False),
        )
        for etiqueta, clave, fila, columna, oculto in campos:
            self._crear_campo(
                formulario, etiqueta, self.registro_vars[clave], fila,
                columna, oculto=oculto, ancho=24,
            )

        ttk.Label(formulario, text="Puesto", style="Acceso.TLabel").grid(
            row=6, column=0, sticky="w", pady=(0, 5)
        )
        self.rango_var = tk.StringVar(value="Mesero/a")
        ttk.Combobox(
            formulario,
            textvariable=self.rango_var,
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
        ).grid(row=7, column=0, columnspan=2, sticky="ew", pady=(0, 12))

        ttk.Button(
            formulario, text="Registrar usuario",
            command=self._registrar_usuario, style="Acceso.TButton",
        ).grid(row=8, column=0, columnspan=2, sticky="ew", pady=(4, 8))
        ttk.Button(
            formulario, text="Volver al inicio de sesión",
            command=self._mostrar_acceso, style="Secundario.TButton",
        ).grid(row=9, column=0, columnspan=2, sticky="ew")

    def _registrar_usuario(self) -> None:
        valores = {clave: variable.get().strip() for clave, variable in self.registro_vars.items()}
        if any(not valor for valor in valores.values()):
            messagebox.showwarning(
                "Datos incompletos", "Completa todos los campos para crear la cuenta."
            )
            return
        try:
            self.servicio.registrar_usuario(
                nombre=valores["nombre"],
                apellido=valores["apellido"],
                nombre_usuario=valores["nombre_usuario"],
                contrasena=valores["contrasena"],
                correo_electronico=valores["correo"],
                fecha_nacimiento=valores["fecha_nacimiento"],
                rango=self.rango_var.get(),
            )
        except ValueError as error:
            messagebox.showerror("No se pudo registrar", str(error))
            return
        except OSError as error:
            messagebox.showerror("Error al guardar", str(error))
            return

        self.usuario_var.set(valores["nombre_usuario"])
        self.contrasena_var.set("")
        self._mostrar_acceso()
        messagebox.showinfo(
            "Cuenta creada", "El usuario quedó registrado. Ya puedes iniciar sesión."
        )

    def _intentar_ingreso(self) -> None:
        if not self.usuario_var.get().strip() or not self.contrasena_var.get().strip():
            messagebox.showwarning("Datos incompletos", "Ingrese usuario y contraseña.")
            return

        usuario = self.servicio.validar_acceso(
            self.usuario_var.get(), self.contrasena_var.get()
        )
        if usuario is None:
            messagebox.showerror("Acceso denegado", "Las credenciales no son válidas.")
            return
        self.al_ingresar(usuario)
