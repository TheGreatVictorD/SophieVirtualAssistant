# Importar las bibliotecas necesarias
import speech_recognition as sr  # Importar la biblioteca de reconocimiento de voz de "SpeechRecognition"
import logging  # Modulo para el control de registro de eventos
import threading

# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(threadName)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Ruta relativa a los archivos 'audio_error' para la reproducción de audio cuando se produzca un error.
audio_error_speech_to_text_file_path_1 = 'models/audio_files/audio_error_speech_to_text_1.wav'
audio_error_speech_to_text_file_path_2 = 'models/audio_files/audio_error_speech_to_text_2.wav'


# Define una función llamada 'transcriber' que toma como argumento el nombre de un archivo de audio
def transcriber(audio_filename):
    # Crea un objeto Recognizer de SpeechRecognition
    r = sr.Recognizer()

    # Abre el archivo de audio especificado
    with sr.AudioFile(audio_filename) as source:
        # Escucha el contenido del archivo de audio
        audio = r.listen(source)
        try:
            # Intenta utilizar el reconocimiento de voz de Google para convertir el audio en texto,
            # especificando que se debe utilizar el idioma español (es-ES)
            text = r.recognize_google(audio, language='es-ES')
            return False, text  # Devuelve el texto transcrito

        # Maneja la excepción cuando el reconocimiento de voz no puede entender el audio
        except sr.UnknownValueError:
            # Texto de respuesta en caso de que no se pueda reconocer el audio
            text = {'ES': 'Lo siento, no te entendí. Por favor, repite de nuevo lo que dijiste.',
                    'EN': "I'm sorry, I didn't understand you. Please repeat what you said again."}
            return True, 1, text

        # Maneja la excepción cuando hay un error al realizar la solicitud de reconocimiento de voz
        except sr.RequestError as e:
            text = f'Lo siento, no puedo procesar tu solicitud con el servicio de reconocimiento de voz de Google. Type error: {e}.'  # Texto de respuesta en caso de error
            print(text)
            text = {
                'ES': 'Lo siento, no puedo procesar tu solicitud con el servicio de reconocimiento de voz de Google.',
                'EN': "Sorry, I can't process your request with Google's voice recognition service."}
            return True, 2, text


# Verifica si este archivo es el archivo principal que se está ejecutando
if __name__ == "__main__":
    # Nombre del archivo de audio que se va a transcribir
    audio_filename = "flac.flac"

    # Llama a la función 'transcriber' con el nombre del archivo de audio y muestra el resultado
    print(transcriber(audio_filename))
