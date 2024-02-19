# Importa las bibliotecas necesarias
import threading  # Biblioteca para el manejo de hilos secundarios
import numpy as np  # Biblioteca para trabajar con matrices y arrays
import pyaudio  # Biblioteca para el manejo del audio
import soundfile as sf  # Biblioteca para trabajar con archivos de audio
import logging  # Modulo para el control de registro de eventos

# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(threadName)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


# Definir una clase llamada EarSophie que representa el grabador de audio
class EarSophie:
    # Ruta relativa a los archivos de audio error
    audio_error_start_recording_file_path = 'ear/audio_files/audio_error_start_recording.wav'
    audio_error_stop_recording_file_path = 'ear/audio_files/audio_error_stop_recording.wav'
    audio_error_record_audio_file_path = 'ear/audio_files/audio_error_record_audio.wav'
    audio_error_save_audio_file_path = 'ear/audio_files/audio_error_save_audio.wav'

    # Ruta relativa al archivo de audio obtenido del usuario
    audio_speech_user_file_path = 'ear/audio_files/audio_speech_user.flac'

    def __init__(self):
        # Inicializar variables de instancia
        self.is_recording = False
        self.frames = []  # Almacenar los fragmentos de audio capturados
        try:
            self.p = pyaudio.PyAudio()  # Inicializar el objeto PyAudio para el manejo del audio
        except Exception as e:
            text = f"Disculpa la interrupción, se produjo un fallo al inicializar el servicio de Pyaudio. Tipo de error: {e}"
            print(text)

    # Método para iniciar la grabación de audio
    def start_recording(self):
        self.is_recording = True
        self.frames = []  # Reiniciar los fragmentos de audio
        try:
            # Configurar y abrir un flujo de audio de entrada
            self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True,
                                      frames_per_buffer=1024)
            # Iniciar un hilo para grabar audio en segundo plano
            self.audio_thread = threading.Thread(target=self._record_audio)
            self.audio_thread.start()
            text = "Se inició la grabación de audio con éxito."
            return False, text

        except Exception as e:
            text = f"Disculpa la interrupción, se produjo un fallo al iniciar la grabación de audio con Pyaudio. Tipo de error: {e}"
            print(text)
            text = {'ES': 'Disculpa la interrupción, se produjo un fallo al iniciar la grabación de audio con Pyaudio.',
                    'EN': 'Sorry for the interruption, there was an error starting audio recording with Pyaudio.'}
            return True, text

    # Método para detener la grabación de audio
    def stop_recording(self):
        self.is_recording = False
        try:
            self.stream.stop_stream()  # Detener el flujo de audio
            self.stream.close()  # Cerrar el flujo de audio
            # self.audio_thread.join()  # Esperar a que el hilo de grabación termine
            self.save_audio()  # Guardar el audio grabado en un archivo
            text = f'Cierre de flujo de grabación de audio con éxito'
            return False, text

        except Exception as e:
            text = f"Disculpa la interrupción, se produjo un fallo en el cierre de flujo de la grabación de audio con Pyaudio. Tipo de error: {e}"
            print(text)
            text = {
                'ES': 'Disculpa la interrupción, se produjo un fallo en el cierre de flujo de la grabación de audio con Pyaudio.',
                'EN': 'Sorry for the interruption, there was an error closing the audio recording stream with Pyaudio.'}
            return True, text

    # Método privado para capturar audio mientras se está grabando
    def _record_audio(self):
        while self.is_recording:
            try:
                data = self.stream.read(1024)  # Leer un fragmento de audio
                self.frames.append(data)  # Agregar el fragmento al registro de fragmentos
                text = f"Registrando el flujo de fragmentos de audio con éxito"

            except Exception as e:
                text = f"Disculpa la interrupción, se produjo un error al tratar de leer o agregar el registro del flujo de fragmentos de audio. Tipo de error: {e}"
                print(text)
                text = {
                    'ES': 'Disculpa la interrupción, se produjo un error al tratar de leer o agregar el registro del flujo de fragmentos de audio.',
                    'EN': 'Sorry for the interruption, an error occurred while trying to read or add the audio fragment stream record.'}
                return True, text

    # Método para guardar el audio grabado en un archivo
    def save_audio(self):
        try:
            audio_data = np.frombuffer(b"".join(self.frames),
                                       dtype=np.int16)  # Convertir los fragmentos en datos de audio
            sf.write(self.audio_speech_user_file_path, audio_data,
                     44100)  # Guardar los datos de audio en un archivo FLAC
            text = f"Se guardaron fragmentos de audio con éxito"
            return False, text

        except Exception as e:
            text = f"Disculpa la interrupción, parece que se produjo un error al tratar de convertir o guardar el registro del flujo de fragmentos de audio. Tipo de error: {e}"
            print(text)
            text = {
                'ES': 'Disculpa la interrupción, parece que se produjo un error al tratar de convertir o guardar el registro del flujo de fragmentos de audio.',
                'EN': 'Sorry for the interruption, it seems there was an error trying to convert or save the audio snippet stream record.'}
            return True, text
