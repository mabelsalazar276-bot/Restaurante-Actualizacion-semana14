import tkinter as tk

from modelos.usuario import Usuario
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView


def main() -> None:
    raiz = tk.Tk()
    raiz.title("Mesa Abierta | Gestión del menú")
    raiz.geometry("960x600")
    raiz.minsize(800, 500)
    raiz.configure(background="#f6efe6")

    servicio = RestauranteServicio()
    servicio.cargar_datos()

    def mostrar_login() -> None:
        for widget in raiz.winfo_children():
            widget.destroy()
        LoginView(raiz, servicio, mostrar_panel).pack(fill="both", expand=True)

    def mostrar_panel(usuario: Usuario) -> None:
        for widget in raiz.winfo_children():
            widget.destroy()
        MainView(raiz, servicio, usuario, mostrar_login).pack(fill="both", expand=True)

    mostrar_login()
    raiz.mainloop()


if __name__ == "__main__":
    main()