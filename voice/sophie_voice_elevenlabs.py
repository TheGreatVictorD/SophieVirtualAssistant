# Importamos las bibliotecas necesarias
from elevenlabs import generate, set_api_key, save, Voice, VoiceSettings  # Importamos la biblioteca "elevenlabs" para interactuar con la API de ElevenLabs.


class SophieVoice:

    # Ruta relativa al archivo 'audio_error_elevenLabs.wav' para la reproducción de audio cuando se produzca un error.
    audio_error_file_path = 'voice/audio_files/audio_error_elevenLabs.wav'

    # Ruta relativa al archivo 'audio_speech_sophie.wav' para la reproducción de audio.
    audio_speech_file_path = 'voice/audio_files/audio_speech_sophie.wav'

    def __init__(self, api_key_eleven_labs, text_input):
        set_api_key(api_key_eleven_labs)  # Establecemos la clave de la API de Eleven Labs.
        self.text_input = text_input  # Guardamos el texto de entrada proporcionado como atributo de la instancia.

    def generate_audio(self):
        try:
            # Intentamos generar audio a partir del texto utilizando la API de Eleven Labs.
            audio = generate(
                text=self.text_input,
                voice=Voice(
                    voice_id='EXAVITQu4vr4xnSDxMaL',
                    settings=VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True)),
                model="eleven_multilingual_v2"
            )
            save(audio, self.audio_speech_file_path)

            return False, self.audio_error_file_path  # Devolvemos el resultado de la generación de audio y la ruta al archivo de error.

        except Exception as e:
            # Si ocurre una excepción al generar el audio, la capturamos y mostramos un mensaje de error.
            text = f"¡Ups! Parece que algo salió mal. Por favor, revisa la conexión con el servicio de Eleven Labs. Gracias. Te espero pronto. Tipo de error: {e}"
            print(f"Ocurrió un error al generar el audio con el servicio de Eleven Labs. Tipo de error: {e}")
            text = {"EN": "Oops! It seems something went wrong. Please check the connection with the Eleven Labs service. Thank you. I'll see you soon.",
                    "ES": "¡Ups! Parece que algo salió mal. Por favor, revisa la conexión con el servicio de Eleven Labs. Gracias. Te espero pronto."}
            return True, text


if __name__ == "__main__":
    API_KEY = 'lkguyfuyfukvugkykuyfcytj'  # Clave de la API de Eleven Labs.
    text = 'Hola, soy ¡Sophie! Soy una inteligencia artificial, un programa de computadora diseñado para ser informativo y completo. ' \
           'Todavía estoy en desarrollo, pero ¡he aprendido a realizar muchos tipos de tareas!, incluyendo...'
    voice = SophieVoice(API_KEY, text)  # Creamos una instancia de la clase SophieVoice con la clave de la API y el texto.
    voice.generate_audio()
