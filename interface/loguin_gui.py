import customtkinter as ctk  # Importar la librería para crear interfaces gráficas
from dotenv import load_dotenv  # Importar La libreria para caragar variables de entorno
import os  # Importar el módulo para interactuar con el sistema operativo
import webbrowser  # Importar la librería para abrir enlaces web
import time  # Importar la librería para usar temporizador
from PIL import Image  # Importar clases para trabajar con imágenes
from screeninfo import get_monitors  # Importar la función para obtener información de monitores
from interface.main_interface_gui import MainInterface  # Importar la clase para abrir ventana secundaria
from resolve_path.resolve_path import resolve_path

# Modo de color y tema
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"


class Login(ctk.CTk):

    # Ruta relativa de la imágen del icono
    icon_path = resolve_path('interface/image_files/api_2.ico')

    # Ruta relativa de las imagenes del logo
    image_light_path = resolve_path('interface/image_files/api_1.png')
    image_dark_path = resolve_path('interface/image_files/api_2.png')

    # Craga la ruta de la imagen del logo
    light_logo_path = Image.open(image_light_path)
    dark_logo_path = Image.open(image_dark_path)

    # Ruta relativa del arcivo "enn_save_data_credentials.txt"
    env_save_data_credentials_path = resolve_path('interface/credentials_files/.env.save_data_credentials')

    # Dimensionar la ventana "Login"
    x_ventana = 320  # Ancho de la ventana customtkinter
    y_ventana = 500  # Alto de la ventana customtkinter

    # Obtener las dimensiones del monitor primario
    monitor = get_monitors()[0]
    screen_width = monitor.width
    screen_height = monitor.height

    # Constructor de la clase "Login"
    def __init__(self):

        super().__init__()

        # Crear una ventana de la interfaz gráfica
        self.title("API login")  # Establecer el título de la ventana
        # Establecer el icono de la ventana a partir de una imagen
        self.iconbitmap(self.icon_path)
        # Establecer el tamaño y posición de la ventana usando variables de clase
        self.geometry(
            f'{self.x_ventana}x{self.y_ventana}+{(self.screen_width // 2) - (self.x_ventana // 2)}+{(self.screen_height // 2) - (self.y_ventana // 2)}')
        # Bloqueo de redimensión de ventana en alto y ancho
        self.resizable(False, False)
        # Hace que ResetWindow no se pueda mover
        # self.overrideredirect(True)

        # Cargar y redimensionar el logo de la aplicación
        self.logo_image = ctk.CTkImage(
            light_image=self.light_logo_path,
            dark_image=self.dark_logo_path,
            size=(150, 150)  # Tamaño de las imágenes
        )
        # Crea el widget de etiqueta que se usa para mostrar imagen del logo.
        logo_label = ctk.CTkLabel(master=self,
                                  image=self.logo_image,
                                  text='')

        # Asociar evento de clic al logo, abre pagina de repositorio
        logo_label.bind("<Button-1>", lambda e: self.open_github_repository())
        logo_label.pack(pady=20)

        # Valores por default de los entry para RememberMe
        self.switch_value = 'off'
        self.username_value = "Ej:Laura"
        self.api_openai_value = "*******"
        self.api_elevenLabs_value = "*******"

        # Carga las variables de entorno del archivo .env
        load_dotenv(self.env_save_data_credentials_path)

        switch_value = os.getenv("SWITCH_VALUE")
        username_value = os.getenv("USER_NAME")
        api_openai_value = os.getenv("API_KEY_OPENAI")
        api_elevenlabs_value = os.getenv("API_KEY_ELEVENLABS")

        # Verificar si valor de switch rememberMe es "on", toma los valores guardados en el archivo .env
        if switch_value == "on":
            self.switch_value = switch_value
            self.username_value = username_value
            self.api_openai_value = api_openai_value
            self.api_elevenLabs_value = api_elevenlabs_value

        # Crear etiqueta y campo de entrada para el usuario
        ctk.CTkLabel(master=self, text="Username").pack(pady=0)
        self.username = ctk.CTkEntry(self)
        self.username.insert(0, self.username_value)  # Insertar texto predeterminado
        # Borrar contenido al hacer clic en el campo
        self.username.bind("<Button-1>", lambda e: self.username.delete(0, 'end'))
        self.username.pack(pady=0)

        # Crear etiqueta y campo de entrada para el API Key from OpenAI
        self.api_key_openai_label = ctk.CTkLabel(master=self, text="API Key from OpenAI")
        self.api_key_openai_label.pack(pady=0)
        self.api_key_openai = ctk.CTkEntry(self)
        self.api_key_openai.insert(0, self.api_openai_value)  # Insertar texto oculto predeterminado
        # Borrar contenido al hacer clic en el campo
        self.api_key_openai.bind("<Button-1>", lambda e: self.api_key_openai.delete(0, 'end'))
        self.api_key_openai.pack(pady=0)

        # Crear etiqueta y campo de entrada para el API Key from ElevenLabs
        self.api_key_elevenlabs_label = ctk.CTkLabel(master=self, text="API Key from ElevenLabs")
        self.api_key_elevenlabs_label.pack(pady=0)
        self.api_key_elevenlabs = ctk.CTkEntry(self)
        self.api_key_elevenlabs.insert(0, self.api_elevenLabs_value)  # Insertar texto oculto predeterminado
        # Borrar contenido al hacer clic en el campo
        self.api_key_elevenlabs.bind("<Button-1>", lambda e: self.api_key_elevenlabs.delete(0, 'end'))
        self.api_key_elevenlabs.pack(pady=0)

        # Agregar el switch RememberMe
        switch_variable = ctk.StringVar(value=self.switch_value)
        self.remenber_switch = ctk.CTkSwitch(master=self,
                                             text='Remember me',
                                             variable=switch_variable,
                                             onvalue="on",
                                             offvalue="off"
                                             )
        self.remenber_switch.pack(pady=10, padx=10)

        # Crear botón "Entrar" que llama a la función get_user_input
        ctk.CTkButton(self, text="Enter", command=self.get_values).pack(pady=15)

        # se crea una variable con valor nulo, servira para albergar la instancia de la interface principal
        self.main_interface = None

    # Función para abrir el enlace en el navegador web del repositorio github
    def open_github_repository(self):
        github_repository_url = "https://github.com/TheGreatVictorD/Asistente_Virtual.git"
        webbrowser.open(github_repository_url)

    # Función para validar valores capturados por los entry
    def get_values(self):

        if self.api_key_openai.get() == "*******" or self.api_key_elevenlabs.get() == "*******" \
                or self.api_key_openai.get() == '' or self.api_key_elevenlabs.get() == '':
            # salta etiqueta de "ingrese valor valido"

            with open(self.env_save_data_credentials_path, 'w') as env_file:
                env_file.write(f"SWITCH_VALUE=off\n")
                env_file.write(f"USER_NAME='Ej:Laura'\n")
                env_file.write(f"API_KEY_OPENAI='*******'\n")
                env_file.write(f"API_KEY_ELEVENLABS='*******'\n")

            # En caso de tener ya un elemento "info_login" (etiqueta) creado, lo borra
            if hasattr(self, "info_login"):
                self.info_login.destroy()
            # Crea esta etiqueta siempre que las credenciales sean incorrectas
            self.info_login = ctk.CTkLabel(self, text="Invalid credentials...")
            self.info_login.pack()
            self.update()

        else:
            # Asigna las credenciales de las variables de entorno a sus respectivas variables de clase
            MainInterface.user_name = self.username.get()
            MainInterface.api_key_openai = self.api_key_openai.get()
            MainInterface.api_key_elevenLabs = self.api_key_elevenlabs.get()

            # Guarda las credenciales del usuario y el valor "on" del switch en el archivo "save_data_rememberMe.txt" para el siguiente inicio de sesión
            if self.remenber_switch.get() == 'on':
                # Guarda las credenciales capturadas del entry dentro del archivo .env
                with open(self.env_save_data_credentials_path, 'w') as env_file:
                    env_file.write(f"SWITCH_VALUE={self.remenber_switch.get()}\n")
                    env_file.write(f"USER_NAME={self.username.get()}\n")
                    env_file.write(f"API_KEY_OPENAI={self.api_key_openai.get()}\n")
                    env_file.write(f"API_KEY_ELEVENLABS={self.api_key_elevenlabs.get()}\n")

            else:
                # si el valor del switch es off, guarda los valores por default dentro del archivo .env
                with open(self.env_save_data_credentials_path, 'w') as env_file:
                    env_file.write(f"SWITCH_VALUE=off\n")
                    env_file.write(f"USER_NAME='Ej:Laura'\n")
                    env_file.write(f"API_KEY_OPENAI='*******'\n")
                    env_file.write(f"API_KEY_ELEVENLABS='*******'\n")

            # En caso de tener ya un elemento "info_login" (etiqueta) creado, lo borra
            if hasattr(self, "info_login"):
                self.info_login.destroy()

            # Crea esta etiqueta siempre que las credenciales sean correctas
            self.info_login = ctk.CTkLabel(self, text=f"Hello, {self.username.get()}. Wait a moment...")
            self.info_login.pack()
            # Actualiza la ventana para ver la etiquta de bienvenida
            self.update()
            # Temporiza para ver la etiqueta antes de cambiar de ventana
            time.sleep(1)
            # Se llamara el metódo para abrir ventana secundaria
            self.open_secondary_window()

    def open_secondary_window(self):
        # Esconde la ventana "Login"
        self.withdraw()
        # Verifica si existe un objeto creado de la clase Minterface
        if self.main_interface is None:  # si no existe, es nulo, se crea una instancia
            self.main_interface = MainInterface(master=self)

        else:  # si existe, la instancia se muestra
            self.main_interface.deiconify()
            self.update()


if __name__ == "__main__":
    login = Login()
    login.mainloop()
