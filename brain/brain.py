# Importa las bibliotecas necesarias
import openai  # Importa el módulo 'openai' para interactuar con la API de OpenAI.
import os  # Importa el módulo 'os' para interactuar con el sistema operativo.
import logging  # Modulo para el control de registro de eventos
import threading


# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(threadName)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
# print(f'Cantidad de hilos activos__aqui brain: {len(threading.enumerate())}')
# logging.info(f'Brain')

# Definimos la clase BrainSophie
class BrainSophie:
    # Ruta al archivo 'audio_error_brain_sophie' para la reproducción de audio en caso de error.
    audio_error_brain_sophie_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "audio_files",
                                                      "audio_error_brain_sophie.wav")

    # El método constructor de la clase
    def __init__(self, message, api_key):
        self.message = message  # Texto proporcionado por el usuario
        self.api_key = api_key  # Clave API de OpenAI

    # Método para realizar la solicitud al modelo GPT
    def think(self):
        try:
            openai.api_key = self.api_key  # Establece la clave API

            # Realiza la solicitud al modelo GPT
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.message,
                temperature=0.5,
                max_tokens=35,
                top_p=0.3,
                frequency_penalty=0.5,
                presence_penalty=0.0
            )
            # Devuelve la respuesta del modelo
            return False, response.choices[0].message['content']

        except Exception as e:
            # En caso de error, devuelve el mensaje de error
            text = f"'¡Rayos! Parece que ocurrió un problema al procesar tu solicitud con el servicio de OpenAI. Por favor, verifica la conectividad con el servicio de OpenAI. Quedo atenta.' Type error: {e}"
            print(text)
            text = {
                'ES': '¡Rayos! Parece que ocurrió un problema al procesar tu solicitud con el servicio de OpenAI. Por favor, verifica la conectividad con el servicio de OpenAI. Quedo atenta.',
                'EN': 'Good heavens! It seems that a problem occurred while processing your request with the OpenAI service. Please check the connectivity with the OpenAI service. I remain attentive.'}
            return True, text


if __name__ == "__main__":
    # Prueba de la clase
    user_text = "Hello, I need to practice my English."  # Texto del usuario
    api_key = "your_api_key"  # Clave API de OpenAI
    sophie = BrainSophie(user_text, api_key)  # Crea una instancia de la clase
    response = sophie.think()  # Realiza la solicitud al modelo GPT
    print(response)  # Imprime la respuesta
