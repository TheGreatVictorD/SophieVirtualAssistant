# Importamos las bibliotecas necesarias
from googletrans import \
    Translator  # Importamos la biblioteca "googletrans" para la detección de idioma y traducción de texto.
import threading  # Biblioteca para el manejo de hilos secundarios
import logging  # Modulo para el control de registro de eventos

# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(threadName)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


# Definimos la clase GoogleTranslator
class GoogleTranslator:
    # El método constructor de la clase que inicializa el texto a traducir y el objeto traductor
    def __init__(self, text):
        self.text = text
        self.translator = Translator()

    # Ruta a los archivos 'audio_error' para la reproducción de audio cuando se produzca un error.
    audio_error_google_translator_file_path_1 = 'translator/audio_files/audio_error_google_translator_1.wav'
    audio_error_google_translator_file_path_2 = 'translator/audio_files/audio_error_google_translator_2.wav'

    # Método para traducir el texto
    def translate(self):
        try:
            # Detectamos el idioma del texto
            languages = self.translator.detect(self.text).lang
            # Si el idioma es español, traducimos el texto al inglés
            if languages == 'es':
                text_en = self.translator.translate(self.text, src='es', dest='en').text
                return False, {'ES': self.text, 'EN': text_en}

            # Si el idioma es inglés, traducimos el texto al español
            elif languages == 'en':
                text_es = self.translator.translate(self.text, src='en', dest='es').text
                return False, {'ES': text_es, 'EN': self.text}

            # Si el idioma no es ni inglés ni español, imprimimos un mensaje de error
            else:
                text = {
                    'ES': 'Rayos, parece que no puedo reconocer el idioma en el que intentas comunicarte. Debes comunicarte en inglés o español. Gracias.',
                    'EN': "Damn, I can't seem to recognize the language you're trying to communicate in. You must communicate in English or Spanish. Thank you."}
                print(text['ES'])
                return True, 1, text

        # En caso de cualquier excepción durante la traducción, imprimimos un mensaje de error
        except Exception as e:
            text = f"Ocurrió un error al intentar traducir el texto a través del servicio de Google Translator. Tipo de error: {e}"
            print(text)
            text = {
                'ES': 'Vaya, parece que ocurrió un error al intentar traducir el texto a través del servicio de Google Translator.',
                'EN': 'Oops, it seems that an error occurred when trying to translate the text through the Google Translator service.'}
            return True, 2, text


# Si este script se ejecuta como el principal, creamos un objeto de la clase GoogleTranslator y lo usamos para traducir un texto
if __name__ == "__main__":
    translator = GoogleTranslator("Hello, I'm Sophie, a very advanced artificial intelligence model")
    result = translator.translate()

    # Imprimimos la traducción en español y su tipo para respectivas pruebas
    x = result[1]["ES"]
    print(x)
    print(type(x))

    # Imprimimos la traducción en inglés y su tipo para respectivas pruebas
    y = result[1]["EN"]
    print(y)
    print(type(y))
