# Importamos las bibliotecas necesarias
import pygame  # Importamos la biblioteca "pygame", para la reproducción de audio.
import threading  # Importamos la biblioteca "threading", para el manejo de hilos secundarios


class SophieVoiceReproductor:
    def __init__(self, audio_file):
        pygame.mixer.init()  # Inicializa el mezclador de música de Pygame
        try:
            pygame.mixer.music.load(audio_file)  # Intenta cargar el archivo de audio
        except pygame.error as e:
            print(
                f"Se produjo un error al cargar el archivo de audio en el reproductor multimedia. El error es del tipo audio: {e}")  # Imprime el error si no se puede cargar el archivo
        self.audio_thread = None  # Hilo para la reproducción de audio

    def playing(self):
        # Si no hay un hilo de audio o si el hilo de audio no está vivo
        if not self.audio_thread or not self.audio_thread.is_alive():
            # Crea un nuevo hilo de audio y lo inicia
            self.audio_thread = threading.Thread(target=self._play_audio)
            self.audio_thread.start()

    def _play_audio(self):
        try:
            pygame.mixer.music.play()  # Intenta reproducir el audio
        except pygame.error as e:
            print(
                f"Error al reproducir el audio en el reproductor multimedia: {e}")  # Imprime el error si no se puede reproducir el audio

    def pause(self):
        try:
            pygame.mixer.music.pause()  # Intenta pausar el audio
        except pygame.error as e:
            print(
                f"Error al pausar el audio en el reproductor multimedia: {e}")  # Imprime el error si no se puede pausar el audio

    def unpause(self):
        try:
            pygame.mixer.music.unpause()  # Intenta reanudar el audio
        except pygame.error as e:
            print(
                f"Error al reanudar el audio en el reproductor multimedia: {e}")  # Imprime el error si no se puede reanudar el audio

    def stop(self):
        try:
            pygame.mixer.music.stop()  # Intenta detener el audio
        except pygame.error as e:
            print(
                f"Error al detener el audio en el reproductor multimedia: {e}")  # Imprime el error si no se puede detener el audio

    def set_volume(self, volume):
        try:
            pygame.mixer.music.set_volume(volume)  # Intenta ajustar el volumen del audio
        except pygame.error as e:
            print(
                f"Error al ajustar el volumen en el reproductor multimedia: {e}")  # Imprime el error si no se puede ajustar el volumen
