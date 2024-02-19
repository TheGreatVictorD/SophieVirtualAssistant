import customtkinter as ctk  # Importar la librería para crear interfaces gráficas
from screeninfo import get_monitors  # Importar la función para obtener información de monitores

ctk.set_appearance_mode("System")  # Modos: "System" (estándar), "Dark", "Light"
ctk.set_default_color_theme("green")  # Temas: "blue" (estándar), "green", "dark-blue"


class ResetWindow(ctk.CTkToplevel):

    # Dimensionar la ventana "ResetWindow"
    monitor = get_monitors()[0]
    screen_width = monitor.width
    screen_height = monitor.height

    x_ventana = 358
    y_ventana = 120

    def __init__(self, master=None, callback=None):
        super().__init__(master)

        # Bloqueo de redimensión de ventana en alto y ancho
        self.resizable(False, False)

        # Establecer el tamaño y posición de la ventana usando variables de clase
        self.geometry(
            f"{self.x_ventana}x{self.y_ventana}+{(self.screen_width // 2) - (self.x_ventana // 2)}+{(self.screen_height // 2) - (self.y_ventana // 2)}")

        # Hace que ResetWindow sea siempre una ventana secundaria de master
        self.transient(master)

        # Hace que ResetWindow sea modal (es decir, bloquea otras ventanas hasta que esta se cierre)
        self.grab_set()

        # Hace que ResetWindow no se pueda mover
        self.overrideredirect(True)

        # Crear franja horizontal para el widget "botones"
        self.horizontal_reset_frame = ctk.CTkFrame(master=self, corner_radius=20)
        self.horizontal_reset_frame.grid(row=0, column=0, rowspan=1, padx=(15, 15), pady=(15, 15), sticky="nsew")

        # Crear etiqueta
        self.reset_label = ctk.CTkLabel(master=self.horizontal_reset_frame,
                                        text="¿Are you sure you want to restart the conversation?",
                                        font=("Arial", 14))
        self.reset_label.pack(pady=(13, 0))

        # Crear botones
        self.yes_button = ctk.CTkButton(master=self.horizontal_reset_frame, text="YES",
                                        command=lambda: [callback(True), self.grab_release(), self.withdraw()])
        self.yes_button.pack(side="left", pady=(10, 10), padx=(10, 10))

        self.no_button = ctk.CTkButton(master=self.horizontal_reset_frame, text="NO",
                                       command=lambda: [callback(False), self.grab_release(), self.withdraw()])
        self.no_button.pack(side="right", pady=(10, 10), padx=(10, 10))


if __name__ == "__main__":
    reset_interface = ResetWindow()
    reset_interface.mainloop()
