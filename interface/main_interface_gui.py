import customtkinter as ctk  # Importar la librería para crear interfaces gráficas
from PIL import Image  # Importar clases para trabajar con imágenes
from screeninfo import get_monitors  # Importar la función para obtener información de monitores
import threading  # Importar biblioteca para el manejo de multihilos en Python
from ear.ear_sophie_flac import EarSophie  # Importar la clase "EarSophie" para grabar audio
from interface.reset_window_gui import ResetWindow  # Importa clase ResetWindow para gui de ventana terciaria
from interface.update_api_window_gui import \
    UpdateApiWindow  # Importa clase UpdateApiWindow para gui de ventana terciaria
from models.to_greet import ToGreet  # Importar la clase "ToGreet" para saludar
from voice.sophie_voice_elevenlabs import SophieVoice  # Importar la clase "SophieVoice" para escuchar a Sophie
from models.timer import timer  # Importar la clase "timer" para obtener lista de tiempos de las frases
from models.timer import audio_error_timer_file_path_1, audio_error_timer_file_path_2, audio_error_timer_file_path_3
from models.speech_to_text_google import audio_error_speech_to_text_file_path_1, audio_error_speech_to_text_file_path_2
from voice.sophie_voice_reproductor import \
    SophieVoiceReproductor  # Importar la clase "SophieVoiceReproductor" para reproducir voz de Sophie
from models.speech_to_text_google import transcriber  # Importar la función "transcriber" para la transcripción de audio
from translator.google_translator import GoogleTranslator  # Importar la clase "GoogleTranslator" para traducir texto
from brain.brain import BrainSophie
from resolve_path.resolve_path import resolve_path
import logging

# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(threadName)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"


# Clase que define la interface principal de la app
class MainInterface(ctk.CTkToplevel):
    # Se crean la variables de entorno con valor inicial nulo
    user_name = None
    api_key_openai = None
    api_key_elevenLabs = None

    # Rutas de los assets de audio

    # Acceder al archivo de audio grabado por el microfono
    audio_speech_user_path = resolve_path(EarSophie.audio_speech_user_file_path)

    # Acceder al archivo de audio de Sophie retornado por ElevenLabs
    audio_speech_sophie_path = resolve_path(SophieVoice.audio_speech_file_path)

    # Dirección del archivo de audioerror cuando se produzca alguna excepción con Eleven Labs.
    audio_error_elevenLabs_path = resolve_path(SophieVoice.audio_error_file_path)

    # Dirección de los archivos de audioerror cuando se produzca alguna excepción con la función timer.
    audio_error_timer_file_path_1 = resolve_path(audio_error_timer_file_path_1)
    audio_error_timer_file_path_2 = resolve_path(audio_error_timer_file_path_2)
    audio_error_timer_file_path_3 = resolve_path(audio_error_timer_file_path_3)

    # Dirección del archivo de audioerror cuando se produzca alguna excepción con la clase EarSophie.
    audio_error_start_recording_file_path = resolve_path(EarSophie.audio_error_start_recording_file_path)
    audio_error_stop_recording_file_path = resolve_path(EarSophie.audio_error_stop_recording_file_path)
    audio_error_record_audio_file_path = resolve_path(EarSophie.audio_error_record_audio_file_path)
    audio_error_save_audio_file_path = resolve_path(EarSophie.audio_error_save_audio_file_path)

    # Dirección del archivo de audioerror cuando se produzca alguna excepción con la función transcriber.
    audio_error_speech_to_text_file_path_1 = resolve_path(audio_error_speech_to_text_file_path_1)
    audio_error_speech_to_text_file_path_2 = resolve_path(audio_error_speech_to_text_file_path_2)

    # Dirección del archivo de audioerror cuando se produzca alguna excepción con la clase GoogleTranslator.
    audio_error_google_translator_1 = resolve_path(GoogleTranslator.audio_error_google_translator_file_path_1)
    audio_error_google_translator_2 = resolve_path(GoogleTranslator.audio_error_google_translator_file_path_2)

    # Dirección del archivo de audioerror cuando se produzca alguna excepción con la clase BrainSophie.
    audio_error_brain_sophie = resolve_path(BrainSophie.audio_error_brain_sophie_file_path)

    # Rutas de los assets de imágen

    # Ruta relativa del icono
    icon_path = resolve_path('interface/image_files/api_2.ico')

    # Ruta relativa de las imagenes
    reset_image_path = resolve_path('interface/image_files/reset_1.png')
    black_microphone_image_path = resolve_path('interface/image_files/microphone_black.png')
    red_microphone_image_path = resolve_path('interface/image_files/microphone_green.png')
    dark_sophie_image_path = resolve_path('interface/image_files/sophie_2.jpg')
    light_sophie_image_path = resolve_path('interface/image_files/sophie_3.jpg')

    # Dimensionar la ventana "MainInterface"
    monitor = get_monitors()[0]
    screen_width = monitor.width
    screen_height = monitor.height
    relation_size = 0.75
    x_ventana = int(screen_width * relation_size)
    y_ventana = int(screen_height * relation_size)

    # Variables de control de la app
    # Variable para controlar la reproducción de audio
    audio = None

    def __init__(self, master=None):
        super().__init__(master)
        # Recive la ventana principal como parametro para poderla llamar mas adelante en método update API
        self.loguin_interface = master
        self.user_conversation = []
        self.sophie_conversation = []
        self.default_role = [{'role': 'system', 'content': 'Eres una asistente mal hablada y grosera......'}]

        self.current_word = 0

        # Configurar el título de la ventana "MainInterface"
        self.title("Sophie Elocuence")
        # Establecer el tamaño y posición de la ventana usando variables de clase
        self.geometry(
            f"{self.x_ventana}x{self.y_ventana}+{(self.screen_width // 2) - (self.x_ventana // 2)}+{(self.screen_height // 2) - (self.y_ventana // 2)}")
        # Establecer el icono de la ventana a partir de una imagen,
        # "usar método after por un error de customtkinter y toplevel, para caragar los iconos"
        self.after(250, lambda: self.iconbitmap(self.icon_path))

        # Configurar grid layout (4x4)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)  # hace que columna 2 se ajuste a la imagen "Sophie"
        self.grid_rowconfigure((0, 1, 2), weight=0)
        self.grid_rowconfigure(3, weight=1)

        # Crear y ubicar franja lateral contenedora de widgets "sidebar frame"
        self.sidebar_frame = ctk.CTkFrame(master=self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")

        # Crear etiqueta emcabezado "SETUP"
        self.logo_label = ctk.CTkLabel(master=self.sidebar_frame,
                                       text="SETUP",
                                       font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 20))

        # Crear y ubicar etiqueta "Sophie's subtitle options"
        self.sophie_sub_option_label = ctk.CTkLabel(master=self.sidebar_frame, text="Sophie's subtitle options:",
                                                    anchor="w")
        self.sophie_sub_option_label.grid(row=1, column=0, padx=20, pady=(0, 0))
        # Crear boton con menu opciones de "Sophie's subtitle options"
        self.sophie_sub_option_menu = ctk.CTkOptionMenu(master=self.sidebar_frame,
                                                        values=["English/Spanish", "English", "Spanish", "Disabled"])
        # Establecer la opcion por defecto y ubicar el boton menu de subtitulos de Sophie
        self.sophie_sub_option_menu.set("English/Spanish")
        self.sophie_sub_option_menu.grid(row=2, column=0, padx=20, pady=(3, 15))

        # Crear y ubicar etiqueta "User's subtitle options:"
        self.user_sub_option_label = ctk.CTkLabel(master=self.sidebar_frame, text="User's subtitle options:",
                                                  anchor="w")
        self.user_sub_option_label.grid(row=3, column=0, padx=20, pady=(0, 0))
        # Crear boton con menu opciones de "User's subtitle options:"
        self.user_sub_option_menu = ctk.CTkOptionMenu(master=self.sidebar_frame,
                                                      values=["English/Spanish", "English", "Spanish", "Disabled"])
        # Establecer la opcion por defecto y ubicar el boton menu de subtitulos del usuario
        self.user_sub_option_menu.set("English/Spanish")
        self.user_sub_option_menu.grid(row=4, column=0, padx=20, pady=(3, 15))

        # Crear y ubicar etiqueta "Subtitle font size:"
        self.sub_font_size_label = ctk.CTkLabel(master=self.sidebar_frame, text="Subtitle font size:", anchor="w")
        self.sub_font_size_label.grid(row=5, column=0, padx=20, pady=(0, 0))
        # Crear boton con menu opciones de "User's subtitle options:"
        self.sub_font_size_menu = ctk.CTkOptionMenu(master=self.sidebar_frame,
                                                    values=["18", "20", "22"],
                                                    command=self.change_sub_font_size,
                                                    anchor="n")

        # Establecer la opcion por defecto y ubicar el boton menu de subtitulos del usuario
        self.sub_font_size_menu.set("20")
        self.sub_font_size_menu.grid(row=6, column=0, padx=20, pady=(3, 15))

        # Crear y ubicar etiqueta "Volume:" para el volumen de la voz de Sophie
        self.volume_setup_label = ctk.CTkLabel(master=self.sidebar_frame, text="Volume:", anchor="w")
        self.volume_setup_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        # Establecer la configuracion del boton Slider del volumen de la voz de Sophie
        self.volume_setup_slider = ctk.CTkSlider(master=self.sidebar_frame, from_=0, to=1, number_of_steps=50,
                                                 orientation="horizontal", command=self.volume_setup)
        # Establecer la opcion por defecto y ubicar el boton menu de subtitulos del usuario
        self.volume_setup_slider.set(0.5)
        # ubicar el boton tipo "Slider" del vulumen volumen de la voz de Sophie
        self.volume_setup_slider.grid(row=8, column=0, padx=(10, 10), pady=(10, 10), sticky="ns")

        # Crear y ubicar etiqueta "Speed:" para la velocidad de la voz de Sophie
        self.speed_setup_label = ctk.CTkLabel(self.sidebar_frame, text="Speed:", anchor="w")
        self.speed_setup_label.grid(row=9, column=0, padx=20, pady=(5, 0))
        # Establecer la configuracion del boton tipo "Slider" para la velocidad de la voz de Sophie
        self.speed_setup_slider = ctk.CTkSlider(master=self.sidebar_frame, from_=3, to=1, number_of_steps=2,
                                                orientation="horizontal", command=self.speed_setup)
        # ubicar el boton tipo "Slider" de la velocidad de la voz de Sophie
        self.speed_setup_slider.grid(row=10, column=0, padx=(10, 10), pady=(10, 10), sticky="ns")
        self.speed_setup_slider.set(2)

        # Establecer fila 11 con un peso de 1 para que abarque el maximo espacio y de un espaciado entre los widgets
        self.sidebar_frame.grid_rowconfigure(11, weight=1)

        # Crear y ubicar etiqueta "Update API:" para actualizar credenciales de las API Keys
        self.update_apis_label = ctk.CTkLabel(master=self.sidebar_frame, text="Update API:", anchor="w")
        self.update_apis_label.grid(row=12, column=0, padx=20, pady=(10, 0))
        # Crear y ubicar boton "Update API:" para actualizar credenciales de las API Keys
        self.update_apis_button = ctk.CTkButton(master=self.sidebar_frame, text='Update',
                                                command=self.update_api_setup)
        self.update_apis_button.grid(row=13, column=0, padx=20, pady=10)

        # Crear y ubicar etiqueta "Appearance Mode:" para cambiar la apariencia de la ventana y sus widgets
        self.appearance_mode_label = ctk.CTkLabel(master=self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=14, column=0, padx=20, pady=(10, 0))
        # Crear y ubicar boton "Appearance Mode:" para cambiar la apariencia de la ventana y sus widgets
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(master=self.sidebar_frame,
                                                             values=["Light", "Dark", "System"],
                                                             command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=15, column=0, padx=20, pady=(5, 25))
        # Establecer la configuracion del boton tipo "Slider" para la velocidad de la voz de Sophie
        self.appearance_mode_optionemenu.set("System")

        # Obtiene las dimensiones reales de la imagen
        width, height = Image.open(self.light_sophie_image_path).size
        # Modificar las dimensiones de la imagen a traves de un modificador
        factor_image = 0.6
        # Redimensionar la imagen
        width_image = int(width * factor_image)
        height_image = int(height * factor_image)

        # Crear y ubicar franja contenedora de imagen "Image Sophie"
        self.sidebar_frame = ctk.CTkFrame(master=self, fg_color="transparent", corner_radius=0)  # transparent, "gray75"
        self.sidebar_frame.grid(row=0, column=1, rowspan=2, sticky="nsew")

        # Cargar imagenes de Sophie para tema light y dark
        self.add_sophie_image = ctk.CTkImage(light_image=Image.open(self.light_sophie_image_path),
                                             dark_image=Image.open(self.dark_sophie_image_path),
                                             size=(width_image, height_image))
        # Isertar y ubicar las imagenes de sophie en una etiqueta para visualizarlas
        self.image_sophie_label = ctk.CTkLabel(master=self.sidebar_frame, text="", image=self.add_sophie_image)
        self.image_sophie_label.pack(padx=(15, 0), pady=(15, 0))

        # Crear textbox del usuario
        self.textbox_user = ctk.CTkTextbox(master=self, width=200, height=160, wrap="word")
        self.textbox_user.grid(row=0, column=2, padx=(15, 15), pady=(15, 0), sticky="nsew")
        # Cambia el tamaño de la letra a 20
        self.textbox_user.configure(font=("Comic Mono", int(self.sub_font_size_menu.get())))
        self.textbox_user.tag_config("1", foreground="#50C878")
        self.textbox_user.tag_config("2", foreground="")
        self.textbox_user.tag_config("3", foreground="#e47200")
        self.textbox_user.insert("0.0", f"{self.user_name}'s Subtitles:\n\n", "3")
        # Deshabilita la edición de texto en la textbox del usuario
        self.textbox_user.configure(state='disabled')
        # Deshabilita la visualización del curso del textbox del usuario
        self.textbox_user.configure(insertwidth=0)

        # Crear textbox de Sophie
        self.textbox_sophie = ctk.CTkTextbox(master=self, width=200, height=160, wrap="word")
        self.textbox_sophie.grid(row=1, column=2, padx=(15, 15), pady=(15, 0), sticky="nsew")
        # Cambia el tamaño de la letra a 20
        self.textbox_sophie.configure(font=("Comic Mono", int(self.sub_font_size_menu.get())))
        self.textbox_sophie.tag_config("1", foreground="#50C878")
        self.textbox_sophie.tag_config("2", foreground="")
        self.textbox_sophie.tag_config("3", foreground="#e47200")
        self.textbox_sophie.insert("0.0", "Sophie's Subtitles:\n\n", "3")
        # Deshabilita la edición de texto en la textbox de Sophie
        self.textbox_sophie.configure(state='disabled')
        # Deshabilita la visualización del curso del textbox de Sophie
        self.textbox_sophie.configure(insertwidth=0)

        # Crear franja horizontal para el widget "microphone"
        self.horizontal_microphone_frame = ctk.CTkFrame(master=self, corner_radius=5, height=20)
        self.horizontal_microphone_frame.grid(row=3, column=1, columnspan=1, padx=(15, 0), pady=(10, 10), sticky="nsew")

        # Establecer tamaño de las imagenes
        self.size_image = 40
        # Cargar imágenes para los botones de micrófono
        self.microphone_black = ctk.CTkImage(Image.open(self.black_microphone_image_path),
                                             size=(self.size_image, self.size_image))
        self.microphone_red = ctk.CTkImage(Image.open(self.red_microphone_image_path),
                                           size=(self.size_image, self.size_image))
        # Crear un botón de micrófono con la imagen en estado inactivo
        self.microphone_button = ctk.CTkButton(master=self.horizontal_microphone_frame, text="",
                                               image=self.microphone_black, width=10, height=10)

        # Colocar el botón de micrófono en la ventana
        self.microphone_button.pack(padx=5, pady=(8, 8))

        # Asociar eventos de clic del mouse a los métodos de inicio y detención de grabación
        self.microphone_button.bind("<ButtonPress-1>", self.start_recording)
        self.microphone_button.bind("<ButtonRelease-1>", self.stop_recording)

        # Crear franja horizontal para el widget "reset"
        self.horizontal_reset_frame = ctk.CTkFrame(master=self, corner_radius=5, height=20)
        self.horizontal_reset_frame.grid(row=3, column=2, columnspan=2, padx=(15, 15), pady=(10, 10), sticky="nsew")

        # Cargar imágenes para el boton de reset
        self.image_reset = ctk.CTkImage(Image.open(self.reset_image_path), size=(self.size_image, self.size_image))
        # Crear un botón de reset con imagen
        self.reset_button = ctk.CTkButton(master=self.horizontal_reset_frame,
                                          text="",
                                          image=self.image_reset,
                                          width=10,
                                          height=10,
                                          command=self.reset_window)
        # Colocar el botón de micrófono en la franja reset
        self.reset_button.pack(padx=5, pady=(8, 8))

        self.microphone_button.configure(state='disabled')
        self.update_apis_button.configure(state='disabled')
        self.reset_button.configure(state='disabled')
        self.reset_button.update()

        # llama la funcion saludo inicial
        self.initiator_to_greet()
        print(self.api_key_openai)

        # Vincular el evento de cierre de la ventana a la función close_program
        self.protocol("WM_DELETE_WINDOW", self.close_program)

    # Métodos asociados a los eventos:

    # ***************************************************************************************************** #
    # ***************************************************************************************************** #
    # *********************** MÉTODOS ASOCIADOS AL FUNCIONAMIENTO DE LA INTERFACE ************************* #
    # ***************************************************************************************************** #
    # ***************************************************************************************************** #

    def change_sub_font_size(self, new_sub_font_size: str):
        # Método para cambiar el tamaño de la fuente de las texbox
        self.textbox_user.configure(font=("Comic Mono", int(self.sub_font_size_menu.get())))
        self.textbox_sophie.configure(font=("Comic Mono", int(self.sub_font_size_menu.get())))
        self.update()

    def volume_setup(self, volume_value: float):
        # Método para variar el volumen de la voz de Sophie
        self.audio.set_volume(volume_value)

    def speed_setup(self, speed_value: float):
        # Método para variar la velocidad de la voz de Sophie
        self.speed_value = int(speed_value)  # Beta

    def start_recording(self, event):
        # Método para inicializar y capturar la grabación de audio por micrófono del usuario
        if self.microphone_button.cget("state") == "normal":
            self.audio_recorder = EarSophie()
            self.start_audio_recorder = self.audio_recorder.start_recording()  # Iniciar la grabación de audio
            self.microphone_button.configure(image=self.microphone_red)  # Cambiar la imagen del botón
            self.update()  # Actuliza la interface gráfica para ver el cambio de la imagen del microfono a rojo
        else:
            self.update()

    def stop_recording(self, event):
        # Método para finalizar y guardar la grabación de audio por microfono del usuario
        if self.microphone_button.cget("state") == "normal":
            self.stop_audio_recorder = self.audio_recorder.stop_recording()  # Detener la grabación de audio
            self.microphone_button.configure(image=self.microphone_black)  # Cambia la imagen del microfono a negro
            self.microphone_button.update()  # Actualiza la imagen del boton del micrófono a negro
            # Se deshabilita el boton para poder capturar audio del usuario, el boton para reiniciar la conversación, y el boton para actualizar las API.
            self.microphone_button.configure(state=ctk.DISABLED)
            self.update_apis_button.configure(state=ctk.DISABLED)
            self.reset_button.configure(state=ctk.DISABLED)
            self.microphone_button.update()
            # Se comprueba si resulto algun error durante la captura de audio del usuario con el microfono
            # Si existe algun error se llama alguno de los métodos correspondientes, acontinuación:
            if self.start_audio_recorder[0] is True:
                text = self.start_audio_recorder[1]
                audio = self.audio_error_start_recording_file_path
                times = [312, 187, 187, 751, 312, 187, 125, 312, 500, 312, 563, 250, 438]
                self.preparing_karaoke(text, audio, times)
            elif self.stop_audio_recorder[0] is True:
                text = self.stop_audio_recorder[1]
                audio = self.audio_error_stop_recording_file_path
                times = [309, 185, 185, 742, 309, 185, 123, 309, 432, 185, 309, 556, 371, 247, 432]
                self.preparing_karaoke(text, audio, times)
            # Si no existe ningun error, entonces se llama al método para transcribir el audio
            else:
                self.initiator()  # Inicia el método speech_to_text en un hilo secundario

        else:
            self.update()

    def update_api_setup(self):
        # Método para actualizar las credenciales de las API de Openai y Eleven Labs
        update_api_window = UpdateApiWindow(master=self, callback=self.handle_response_update_api)

    def handle_response_update_api(self, response):
        # Método para verificar respuesta de la ventana de "update_api_setup"
        if response:
            # Oculta la interface principal (instancia de MainInterface)
            self.withdraw()
            # Mostrar la ventana principal nuevamente (instancia de Loguin)
            self.loguin_interface.deiconify()  # Asume que loguin_gui es el nombre de la ventana principal

    def reset_window(self):
        # Método para crear una instancia de ResetWindow, para resetear el historial de la conversación con Sophie
        reset_window = ResetWindow(master=self, callback=self.handle_response_reset)

    def handle_response_reset(self, response):
        # Método para verificar la respuesta del usuario de la ventana "reset_window"
        if response:  # Si el usuario respondio "YES", se reiniciara la conversación con Sophie
            self.current_word = 0
            # Declaro un hilo de ejecución, para ejecutar el Karaoke
            self.initiator_to_greet()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        # Método para cambiar la apariencia de la interface de la aplicación
        ctk.set_appearance_mode(new_appearance_mode)

        # *****************************************************************************************************
        # *****************************************************************************************************
        # ********************************** AQUI VA LA LÓGICA DEL PROGRAMA ***********************************
        # *****************************************************************************************************
        # *****************************************************************************************************

    def to_greet(self):
        # Método para realizar saludo inicial de Sophie hacia el usuario
        # Este método devuelve un diccionario con un saludo en inglés y su respectiva traducción al español
        self.to_greet_list = ToGreet(self.user_name).greet()
        # llama al método para convertir texto en Audio con el modelo de elevenLabs
        self.sophie_voice_generator_initiator = threading.Thread(target=self.sophie_voice_generator, args=((self.to_greet_list['EN']),))
        self.sophie_voice_generator_initiator.start()
        self.sophie_voice_verificator(self.to_greet_list)

    def initiator_to_greet(self):
        # Declaro un hilo de ejecución, para ejecutar el Karaoke
        threading_to_greet = threading.Thread(target=self.to_greet)
        threading_to_greet.start()

    def transcribe(self):
        # Se llama al método para transcribir el audio capturado por el microfono del usuario
        self.transcriber = transcriber(self.audio_speech_user_path)
        # Si existe algun error durante la transcripcion del audio, se llamara alguno de los métodos correspondientes, acontinuación:
        if self.transcriber[0] is True:

            if self.transcriber[1] == 1:
                text = self.transcriber[2]
                audio = self.audio_error_speech_to_text_file_path_1
                times = [143, 359, 71, 359, 718, 215, 431, 431, 287, 215, 287, 359]
                self.preparing_karaoke(text, audio, times)

            else:
                text = self.transcriber[2]
                audio = self.audio_error_speech_to_text_file_path_2
                times = [316, 63, 253, 443, 253, 443, 253, 443, 316, 697, 443]
                self.preparing_karaoke(text, audio, times)

        else:
            # Se envia la solicitud al API de OpenAi en un hilo separado para que el tiempo de respuesta sea menor
            self.sophie_thought_initiator = threading.Thread(target=self.sophie_thought, args=((self.transcriber[1]),))
            self.sophie_thought_initiator.start()
            # Si no se registro ningun error, entonces se continua con la traducción de la transcripción del audio
            self.to_translate(self.transcriber[1], 'user')

    def to_translate(self, input_text, _id):
        # Se llama al método para traducir la transcripción del audio usando el servicio de Google Translator
        self.translated_text = GoogleTranslator(input_text).translate()
        # Se comprueba si ocurrio algun error durante la traducción de la transcripción, se llama los siguientes métodos, A continuación:
        if self.translated_text[0] is True:
            if self.translated_text[1] == 1:
                text = self.translated_text[2]
                audio = self.audio_error_google_translator_1
                times = [274, 68, 274, 274, 137, 616, 205, 548, 342, 411, 137, 753, 137, 205, 274, 753, 137,
                         479, 137, 479, 342, 205]
                self.preparing_karaoke(text, audio, times)

            else:
                text = self.translated_text[2]
                audio = self.audio_error_google_translator_2
                times = [276, 138, 345, 276, 138, 345, 552, 276, 414, 138, 621, 207, 276, 483, 207, 414, 690,
                         483]
                self.preparing_karaoke(text, audio, times)

        else:
            # Si no existe ningun error durante la traducción de la transcripción, se verifica que método se llamara, a continuación:
            if _id == 'user':
                # Se llama el metódo para inserta el texto en el texbox del usuario:
                self.insert_user_textbox(self.translated_text[1])

            elif _id == 'sophie':
                # Se llama al metódo 'voice_verificator' para verificar si el audio se pudo generar
                self.sophie_voice_verificator(self.translated_text[1])

    def insert_user_textbox(self, text_input):
        # Habilita el textbox del Usuario para poder insertar nuevo texto
        self.textbox_user.configure(state='normal')
        # Borra el contenido actual del cuadro de texto del usuario
        self.textbox_user.delete("1.0", "end")

        # Se verifíca el estado del botón de los subtítulos y se ejecuta el método correspondiente:
        if self.user_sub_option_menu.get() == "English/Spanish":
            # Inserta título del "textbox_sophie"
            self.textbox_user.insert("0.0", f"{self.user_name}'s Subtitles:", "3")
            # Inserta título del "English Subtitles"
            self.textbox_user.insert("end", "\n\nEnglish Subtitles:\n\n", "3")
            # Insertar la transcripcion del audio del usuario en ingles
            self.textbox_user.insert("end", text_input['EN'], "2")
            # Inserta título "Spanish Subtitles"
            self.textbox_user.insert("end", "\n\nSpanish Subtitles:\n\n", "3")
            # Insertar la transcripcion del audio del usuario en español
            self.textbox_user.insert("end", text_input['ES'], "2")

        elif self.user_sub_option_menu.get() == "English":
            # Inserta título del "textbox" del usuario
            self.textbox_user.insert("0.0", f"{self.user_name}'s Subtitles:", "3")
            # Inserta título del "English Subtitles"
            self.textbox_user.insert("end", "\n\nEnglish Subtitles:\n\n", "3")
            # Insertar la transcripcion del audio del usuario en ingles
            self.textbox_user.insert("end", text_input['EN'], "2")
            self.textbox_user.insert("end", "\n\nSpanish Subtitles: Disabled\n\n", "3")

        elif self.user_sub_option_menu.get() == "Spanish":
            # Inserta título del "textbox" del usuario
            self.textbox_user.insert("0.0", f"{self.user_name}'s Subtitles:\n\n", "3")
            # Inserta título del "English Subtitles: Disabled"
            self.textbox_user.insert("end", "English Subtitles: Disabled", "3")
            # Inserta título "Spanish Subtitles"
            self.textbox_user.insert("end", "\n\nSpanish Subtitles:\n\n", "3")
            # Insertar la transcripcion del audio del usuario en español
            self.textbox_user.insert("end", text_input['ES'], "2")

        else:
            # Inserta título del "usuario"
            self.textbox_user.insert("0.0", f"{self.user_name}'s Subtitles: Disabled\n\n", "3")

        # Se deshabilita la edición del texto insertado en el textbox del Usuario
        self.textbox_user.configure(state='disabled')
        # Se llama al método 'sophie_thought_verificator' para verificar si la solicitud en el hilo secundario al API de OpenAI fue exitosa.
        self.sophie_thought_verificator()

    def sophie_thought(self, text_input):
        self.message = self.default_role
        self.message.append({'role': 'user', 'content': text_input})
        self.sophies_think = BrainSophie(self.message, self.api_key_openai).think()

    def sophie_thought_verificator(self):
        # Bloquea el hilo principal hasta que "sophie_though_initiator" termine su proceso:
        self.sophie_thought_initiator.join()

        # Una vez terminado el proceso de "sophie_though_initiator" se verifica su contenido, para saber si existe alguna excepción:
        if self.sophies_think[0] is True:
            text = self.sophies_think[1]
            audio = self.audio_error_brain_sophie
            times = [289, 506, 144, 361, 289, 72, 506, 578, 361, 723, 289, 506, 289, 216, 433, 506, 433, 361, 216, 867,
                     289, 216, 433, 506, 72, 433, 650]
            self.preparing_karaoke(text, audio, times)
        else: # ojo revisar el rol de la respuest///0
            self.message.append(self.sophies_think[1])
            self.think_input_text = self.sophies_think[1]
            self.sophie_voice_generator_initiator = threading.Thread(target=self.sophie_voice_generator,
                                                                     args=(self.think_input_text,))
            self.sophie_voice_generator_initiator.start()

            self.to_translate(self.think_input_text, 'sophie')

    def sophie_voice_generator(self, text_input):

        self.speech_generator_input_text = text_input

        if int(self.speed_setup_slider.get()) == 1:  # Este reemplazo no modifica la velocidad de la voz de Sophie
            self.speech_generator_input_text = self.speech_generator_input_text.replace(" ",
                                                                                        " ")  # El espaciado queda igual, no cambia
        elif int(self.speed_setup_slider.get()) == 2:  # Este reemplazo hace mas pausada la voz de Sophie
            self.speech_generator_input_text = self.speech_generator_input_text.replace(" ",
                                                                                        "-")  # Reemplaza un espacio por "-"
        elif int(self.speed_setup_slider.get()) == 3:  # Este reemplazo hace aun mas pausada la voz de Sophie
            self.speech_generator_input_text = self.speech_generator_input_text.replace(" ",
                                                                                        "--")  # Reemplaza un espacio por tres espacios

        # Se envía la solicitud a la API de Eleven Labs para generar la respuesta de audio.
        self.audio_speech_sophie_path = SophieVoice(self.api_key_elevenLabs,
                                                    self.speech_generator_input_text).generate_audio()

    def sophie_voice_verificator(self, text_input):

        self.sophie_voice_generator_initiator.join()
        # Se verifica si se generó algún error en la petición a la API de Eleven Labs.
        if self.audio_speech_sophie_path[0] is True:
            text_alert = self.audio_speech_sophie_path[1]
            audio = self.audio_error_elevenLabs_path
            times = [289, 144, 362, 651, 289, 362, 434, 362, 217, 724, 289, 217, 434, 289, 506, 362, 217, 217, 217, 217,
                     289]
            self.preparing_karaoke(text_alert, audio, times)

        else:
            audio_file_path = self.audio_speech_sophie_path[1]
            self.timer(text_input, audio_file_path)

    def timer(self, text_input, audio_imput):
        self.english_transcription = text_input['EN']
        self.audio_input = audio_imput
        # Se lama a la función Timer para obtener la lista de tiempos para el karaoke
        self.times_list = timer(self.audio_input, self.english_transcription)
        # Se verifica que no exista ningún error durante el método timer, si existe alguno se mostrara en karaoke:
        if self.times_list[0] is True:
            if self.times_list[1] == 1:
                text_alert = self.times_list[2]
                audio = self.audio_error_timer_file_path_1
                times = [140, 351, 562, 140, 210, 351, 562, 140, 491, 281, 210, 281, 562, 210, 210, 351]
                self.preparing_karaoke(text_alert, audio, times)

            elif self.times_list[1] == 2:
                text_alert = self.times_list[2]
                audio = self.audio_error_timer_file_path_2
                times = [145, 363, 582, 145, 218, 363, 582, 145, 509, 291, 218, 363, 582, 145, 218, 363, 291, 145, 291]
                self.preparing_karaoke(text_alert, audio, times)

            else:
                text_alert = self.times_list[2]
                audio = self.audio_error_timer_file_path_3
                times = [145, 363, 581, 145, 218, 363, 581, 145, 363, 290, 145, 363, 218, 218, 218, 363, 145, 218, 363]
                self.preparing_karaoke(text_alert, audio, times)

        else:
            # Si no existe ningún error, se llama al siguiente método para preparar el karaoke
            self.preparing_karaoke(text_input, self.audio_input, self.times_list[1])

    def preparing_karaoke(self, karaoke_input_text, karaoke_input_audio, karaoke_input_times):
        # Convierte los valores de las claves del diccionario de un tipo "str" a un tipo "list", para que pueda ser leido por el karaoke
        for clave in karaoke_input_text:
            karaoke_input_text[clave] = karaoke_input_text[clave].split()
        # Se asignan los valores de los subtitulos en ingles a la variable "self.text_input_english"
        self.text_input_english = karaoke_input_text['EN']
        # Se asignan los valores de los subtitulos en español a la variable "self.text_input_spanish"
        self.text_input_spanish = karaoke_input_text['ES']
        # Se asignan los valores de los tiempos del karaoke a la variable "self.times_list"
        self.times_list = karaoke_input_times
        # Se carga el respectivo audio
        self.audio = SophieVoiceReproductor(karaoke_input_audio)
        # Se asigna el valor de 0 a la variable "self.current_word"
        self.current_word = 0
        # Se inicializa el "karaoke"
        self.karaoke()
        # inicia la reproducción del audio "Voz de Sophie"
        self.audio.playing()

    def karaoke(self):
        # habilita la textbox de Sophie para poder insertar texto
        self.textbox_sophie.configure(state='normal')
        # Borra el contenido actual del cuadro de texto
        self.textbox_sophie.delete("1.0", "end")

        # Se obtiene estado del boton "Subtitles option" y se ejecuta el método correspondiente, A continuación:
        if self.sophie_sub_option_menu.get() == "English/Spanish":
            self.textbox_sophie.insert("0.0", "Sophie's Subtitles:", "3")
            self.textbox_sophie.insert("end", "\n\nEnglish Subtitles:\n\n", "3")

            # Inserta cada palabra con el formato correspondiente
            for i, word in enumerate(self.text_input_english):
                tag = "1" if i == self.current_word else "2"  # La palabra actual tiene el tag "1", las demás tienen el tag "2"
                self.textbox_sophie.insert("end", word + " ", tag)

            self.textbox_sophie.insert("end", "\n\nSpanish Subtitles:\n\n", "3")
            # Inserta todas las palabras de nuevo con el color estándar
            for spanish_word in self.text_input_spanish:
                self.textbox_sophie.insert("end", spanish_word + " ", "2")

        elif self.sophie_sub_option_menu.get() == "English":
            self.textbox_sophie.insert("0.0", "Sophie's Subtitles:", "3")
            self.textbox_sophie.insert("end", "\n\nEnglish Subtitles:\n\n", "3")

            # Inserta cada palabra con el formato correspondiente
            for i, word in enumerate(self.text_input_english):
                tag = "1" if i == self.current_word else "2"  # La palabra actual tiene el tag "1", las demás tienen el tag "2"
                self.textbox_sophie.insert("end", word + " ", tag)

            self.textbox_sophie.insert("end", "\n\nSpanish Subtitles: Disabled\n\n", "3")

        elif self.sophie_sub_option_menu.get() == "Spanish":
            self.textbox_sophie.insert("0.0", "Sophie's Subtitles:", "3")
            self.textbox_sophie.insert("end", "\n\nEnglish Subtitles: Disabled\n\n", "3")
            self.textbox_sophie.insert("end", "Spanish Subtitles:\n\n", "3")
            # Inserta todas las palabras de nuevo con el color estándar
            for spanish_word in self.text_input_spanish:
                self.textbox_sophie.insert("end", spanish_word + " ", "2")

        else:
            self.textbox_sophie.insert("0.0", "Sophie's Subtitles: Disabled\n\n", "3")

        # Si la palabra actual no es la última, programa la próxima actualización
        if self.current_word < len(self.text_input_english) - 1:
            # Programa la próxima actualización para dentro del tiempo especificado en la lista de tiempos
            self.after(self.times_list[self.current_word], self.karaoke)
            self.current_word += 1  # Actualiza el contador para la palabra actual

        else:
            # Si la palabra actual es la última, se llama al método "change_last_word_color_textbox_sophie", para insertar toda la frase unicolor
            self.after(self.times_list[-1], self.inserting_last_unicolor_sentence)

    def inserting_last_unicolor_sentence(self):
        # Método para insertar la ultima frase inicolor

        # Borra el texto de "textbox_sophie"
        self.textbox_sophie.delete("1.0", "end")

        # Se obtiene estado del boton "Subtitles option" y se ejecuta el método correspondiente, A continuación:
        if self.sophie_sub_option_menu.get() == "English/Spanish":
            # Inserta título del "textbox_sophie"
            self.textbox_sophie.insert("0.0", "Sophie's Subtitles:", "3")
            # Inserta título del "English Subtitles"
            self.textbox_sophie.insert("end", "\n\nEnglish Subtitles:\n\n", "3")
            # Inserta todas las palabras de nuevo con el color estándar en ingles
            for word in self.text_input_english:
                self.textbox_sophie.insert("end", word + " ", "2")
            # Inserta todas las palabras de nuevo con el color estándar en Español
            self.textbox_sophie.insert("end", "\n\nSpanish Subtitles:\n\n", "3")
            # Inserta todas las palabras de nuevo con el color estándar
            for word in self.text_input_spanish:
                self.textbox_sophie.insert("end", word + " ", "2")

        elif self.sophie_sub_option_menu.get() == "English":
            # Inserta título del "textbox_sophie"
            self.textbox_sophie.insert("0.0", "Sophie's Subtitles:", "3")
            # Inserta título del "English Subtitles"
            self.textbox_sophie.insert("end", "\n\nEnglish Subtitles:\n\n", "3")
            # Inserta todas las palabras de nuevo con el color estándar en ingles
            for word in self.text_input_english:
                self.textbox_sophie.insert("end", word + " ", "2")
            self.textbox_sophie.insert("end", "\n\nSpanish Subtitles: Disabled\n\n", "3")

        elif self.sophie_sub_option_menu.get() == "Spanish":
            # Inserta título del "textbox_sophie"
            self.textbox_sophie.insert("0.0", "Sophie's Subtitles:\n\n", "3")
            self.textbox_sophie.insert("end", "English Subtitles: Disabled", "3")
            self.textbox_sophie.insert("end", "\n\nSpanish Subtitles:\n\n", "3")
            # Inserta todas las palabras de nuevo con el color estándar
            for word in self.text_input_spanish:
                self.textbox_sophie.insert("end", word + " ", "2")

        else:
            self.textbox_sophie.insert("0.0", "Sophie's Subtitles: Disabled\n\n", "3")

        # Se deshabilita la edición del texto insertado en el textbox de Sophie
        self.textbox_sophie.configure(state='disabled')
        # Se habilita el boton para poder capturar audio del usuario, el boton para reiniciar la conversación, y el boton para actualizar las API.
        self.microphone_button.configure(state=ctk.NORMAL)
        self.update_apis_button.configure(state=ctk.NORMAL)
        self.reset_button.configure(state=ctk.NORMAL)
        # Se reinicia el contador de palabras
        self.current_word = 0

    def initiator(self):
        # Declaro un hilo de ejecución secundario
        threading_speech_to_text = threading.Thread(target=self.transcribe)
        # se ejecuta el hilo secunadrio
        threading_speech_to_text.start()

    def close_program(self):
        self.master.quit()  # Cierra el programa desde la ventana secundaria


if __name__ == "__main__":
    main_intreface = MainInterface()
    main_intreface.mainloop()
