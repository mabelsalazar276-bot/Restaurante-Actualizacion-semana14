# Mesa Abierta

**Autora:** Mabela del Cisne Salazar Ren

**Trabajo:** Semana 14

## Descripción

Mesa Abierta es una aplicación de escritorio desarrollada en Python con Tkinter. Su objetivo es facilitar la consulta del menú y controlar el acceso de las personas registradas en el restaurante.

El proyecto organiza la información, la lógica y las vistas en módulos separados. Actualmente trabaja con las entidades `Producto` y `Usuario`; el catálogo incluye tacos, bowls, sopas, postres y bebidas.

## Estructura

```text
restaurante_app/
├── .gitignore
├── main.py
├── README.md
├── datos/
│   ├── productos.json
│   └── usuarios.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   └── usuario.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
└── ui/
	├── __init__.py
	├── login_view.py
	└── main_view.py
```

## Funcionamiento por componentes

- **Modelos:** representan la información de los productos y las cuentas de usuario.
- **Servicios:** gestionan la carga, persistencia y operaciones del catálogo, además de comprobar las credenciales.
- **Interfaz:** contiene el login y un panel principal organizado con `Frame`, `LabelFrame`, `Entry`, `Treeview`, `Scrollbar` y botones `ttk`.
- **Inicio:** `main.py` prepara la ventana, carga la información y enlaza los componentes.

## Archivos de datos

La información utilizada por el programa se encuentra en la carpeta `datos/`:

- `productos.json`: catálogo disponible.
- `usuarios.json`: usuarios habilitados para ingresar.

## Operaciones de productos

En la sección **Productos** se utiliza un formulario para capturar el ID, nombre, precio, categoría y stock. Las acciones disponibles son:

- **Registrar:** crea un producto nuevo.
- **Cargar / Consultar:** busca un producto mediante su ID y muestra sus datos en el formulario.
- **Actualizar:** reemplaza la información del producto seleccionado por su ID.
- **Eliminar:** retira el producto del catálogo.

Todas las acciones son solicitadas a `RestauranteServicio`. La interfaz no lee ni modifica directamente los archivos JSON; después de cada operación actualiza la tabla visible.

Las ventas no están implementadas; solo se muestran como una opción pendiente en la interfaz y no cuentan con modelo ni archivo de almacenamiento.

## Cómo iniciar la aplicación

Abre una terminal en la carpeta principal del proyecto y ejecuta:

```bash
python main.py
```

## Credenciales de demostración

```text
Usuario: sofia
Contraseña: menu2026
```

## Verificación de sintaxis

Para revisar que los archivos Python sean válidos, utiliza:

```bash
python -m compileall -q main.py modelos servicios ui
```

## Comprobación de la Semana 14

1. Ejecutar `python main.py` e ingresar con `sofia` y `menu2026`.
2. Abrir **Usuarios** para consultar la información registrada.
3. Abrir **Productos** y probar el registro, consulta, actualización y eliminación usando el formulario.
4. Cerrar y volver a ejecutar la aplicación para comprobar que los cambios permanecen en `datos/productos.json`.