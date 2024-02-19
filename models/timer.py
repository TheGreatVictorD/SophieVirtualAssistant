# Importar las bibliotecas necesarias
import wave  # Importamos la biblioteca "wave" para el manejo de archivos de audio

# Ruta relativa a los archivos 'audio_error' para la reproducción de audio cuando se produzca un error.
audio_error_timer_file_path_1 = 'models/audio_files/audio_error_timer_1.wav'
audio_error_timer_file_path_2 = 'models/audio_files/audio_error_timer_2.wav'
audio_error_timer_file_path_3 = 'models/audio_files/audio_error_timer_3.wav'


# Definición de la función 'timer' que calcula la duración de palabras en un archivo de audio
def timer(audio_input, transcription):

    try:
        # Elimina caracteres de la cadena, solo deja letras y números
        transcription = ''.join(c for c in transcription if c.isalnum() or c.isspace())

        # Dividir la transcripción en palabras
        words = transcription.split()

        # Calcular las longitudes de cada palabra
        word_durations = [len(word) for word in words]

        # Calcular la longitud total de las palabras
        total_words_durations = sum(word_durations)

        # Abrir el archivo de audio
        with wave.open(audio_input, 'rb') as wf:
            # Obtener la frecuencia de muestreo del archivo de audio
            fs = wf.getframerate()
            # Obtener el número total de muestras en el archivo de audio
            n_samples = wf.getnframes()
            # Calcular la duración total del archivo de audio en segundos
            total_audio_duration = (n_samples / fs) * 0.94

        # Calcular la relación entre la duración del audio y la duración de las palabras
        r = total_audio_duration / total_words_durations

        # Calcular la duración de cada palabra en milisegundos en función de la relación 'r'
        time_words_duration = [int(1000 * r * word // 1) for word in word_durations]
        # Retorna una lista con tiempo de duración de cada palabra
        return False, time_words_duration

    except FileNotFoundError:
        text = "Se produjo un error en la función Timer, parece que no se encontró la ubicación del archivo."
        print(text)
        text = {'ES': 'Se produjo un error en la función Timer, parece que no se encontró la ubicación del archivo.',
                'EN': 'An error occurred in the Timer function, it appears that the file location was not found.'}
        return True, 1, text
    except ZeroDivisionError:
        text = "Se produjo un error en la función Timer, parece que la duración total del archivo de audio es cero."
        print(text)
        text = {
            'ES': 'Se produjo un error en la función Timer, parece que la duración total del archivo de audio es cero.',
            'EN': 'An error occurred in the Timer function, it appears that the total duration of the audio file is zero.'}
        return True, 2, text
    except Exception as e:
        text = f"Se produjo un error en la función Timer, parece que no se pudo obtener los tiempos de las palabras. Type error: {e}"
        print(text)
        text = {
            'ES': 'Se produjo un error en la función Timer, parece que no se pudo obtener los tiempos de las palabras.',
            'EN': 'An error occurred in the Timer function, it seems that it could not get the times of the words.'}
        return True, 3, text


# Función principal, prueba
if __name__ == "__main__":
    # Nombre del archivo de audio
    audio_file = 'audio_error_brain_sophie.wav'
    # Transcripción del audio
    transcription = 'Good heavens! It seems that a problem occurred while processing your request with the OpenAI service. Please check the connectivity with the OpenAI service. I remain attentive.'
    # Llamar a la función 'timer' con el archivo de audio y la transcripción como argumentos
    times = timer(audio_file, transcription)[1]
    print(times)
    print(len(times))
    print(sum(times) / 1000)
