import customtkinter as ctk  # Importar la librería para crear interfaces gráficas
from screeninfo import get_monitors  # Importar la función para obtener información de monitores

ctk.set_appearance_mode("System")  # Modos: "System" (estándar), "Dark", "Light"
ctk.set_default_color_theme("green")  # Temas: "blue" (estándar), "green", "dark-blue"


class UpdateApiWindow(ctk.CTkToplevel):

    # Dimensionar la ventana "UpdateApiWindow"
    monitor = get_monitors()[0]
    screen_width = monitor.width
    screen_height = monitor.height

    x_ventana = 350
    y_ventana = 100

    def __init__(self, master=None, callback=None):
        super().__init__(master)

        # Bloqueo de redimensión de ventana en alto y ancho
        self.resizable(False, False)

        # Establecer el tamaño y posición de la ventana usando variables de clase
        self.geometry(
            f"{self.x_ventana}x{self.y_ventana}+{(self.screen_width // 2) - (self.x_ventana // 2)}+{(self.screen_height // 2) - (self.y_ventana // 2)}")

        # Hace que UpdateApiWindow sea siempre una ventana secundaria de master
        self.transient(master)

        # Hace que UpdateApiWindow sea modal (bloquea otras ventanas hasta que esta se cierre)
        self.grab_set()

        # Hace que UpdateApiWindow no se pueda mover
        self.overrideredirect(True)

        # Crear franja horizontal para el widget "reset"
        self.horizontal_reset_frame = ctk.CTkFrame(master=self, corner_radius=20)
        self.horizontal_reset_frame.grid(row=0, column=0, rowspan=1, padx=(15, 15), pady=(15, 15), sticky="nsew")

        # Crear etiqueta
        self.reset_label = ctk.CTkLabel(master=self.horizontal_reset_frame,
                                        text="¿Do you want to update the API keys?",
                                        font=("Arial", 15))
        self.reset_label.pack(pady=(1, 0))

        # Crear botones
        self.yes_button = ctk.CTkButton(master=self.horizontal_reset_frame, text="YES",
                                        command=lambda: [callback(True), self.grab_release(), self.withdraw()])
        self.yes_button.pack(side="left", pady=(5, 10), padx=(10, 10))

        self.no_button = ctk.CTkButton(master=self.horizontal_reset_frame, text="NO",
                                       command=lambda: [callback(False), self.grab_release(), self.withdraw()])
        self.no_button.pack(side="right", pady=(5, 10), padx=(10, 10))


if __name__ == "__main__":
    update_api_interface = UpdateApiWindow()
    update_api_interface.mainloop()
