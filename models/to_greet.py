# Importamos las bibliotecas necesarias
import random  # Importamos la biblioteca "random" para generar saludos aleatorios.


# Clase ToGreet: Genera saludos personalizados y aleatorios en inglés y su respeciva traduccion a español.
class ToGreet:

    def __init__(self, user_name):
        self.user_name = user_name  # Guardamos el nombre del usuario proporcionado como atributo de la instancia.
        self.greetings = [
            # Lista de saludos personalizados con el nombre del usuario.
            # Utilizamos f-strings para insertar el nombre del usuario en cada saludo.

            {'ES': f"¡Hola, {self.user_name}! Soy Sophie, tu asistente de práctica de inglés. ¿Qué te gustaría discutir hoy?", 'EN': f"Hello, {self.user_name}! I'm Sophie, your English practice assistant. What would you like to discuss today?"},
            {'ES': f"Saludos, {self.user_name}. Soy Sophie, aquí estoy para ayudarte con tu práctica de inglés. ¿En qué tema estás interesado?", 'EN': f"Greetings, {self.user_name}. I'm Sophie, here to assist you with your English practice. What topic are you interested in?"},
            {'ES': f"¡Bienvenido, {self.user_name}! Soy Sophie, lista para conversar contigo en inglés. ¿Sobre qué quieres hablar?", 'EN': f"Welcome, {self.user_name}! I'm Sophie, ready to chat with you in English. What would you like to talk about?"},
            {'ES': f"Hey, {self.user_name}, ¿cómo estás? Soy Sophie, tu compañera de práctica de inglés. ¿Cuál es el tema del día?", 'EN': f"Hey, {self.user_name}, how are you? I'm Sophie, your English practice partner. What's the topic for today?"},
            {'ES': f"¡Hola, {self.user_name}! Soy Sophie, tu asistente personal para mejorar tu inglés. ¿Cuál es la conversación de hoy?", 'EN': f"Hello, {self.user_name}! I'm Sophie, your personal assistant to help you improve your English. What's today's conversation?"},
            {'ES': f"Saludos, {self.user_name}. Aquí tienes a Sophie, tu asistente de inglés. ¿En qué puedo asistirte hoy?", 'EN': f"Greetings, {self.user_name}. Here's Sophie, your English assistant. How can I assist you today?"},
            {'ES': f"¡Hola, {self.user_name}! Soy Sophie, el asistente perfecto para mejorar tu inglés. ¿Sobre qué te gustaría charlar?", 'EN': f"Hello, {self.user_name}! I'm Sophie, the perfect assistant to help you improve your English. What would you like to chat about?"},
            {'ES': f"¡Bienvenido a bordo, {self.user_name}! Soy Sophie, y estoy aquí para ayudarte a practicar inglés. ¿Cuál es tu elección de tema?", 'EN': f"Welcome aboard, {self.user_name}! I'm Sophie, and I'm here to help you practice English. What's your choice of topic?"},
            {'ES': f"¡Hola, {self.user_name}! ¡Es genial escucharte! Soy Sophie, tu compañera virtual para practicar inglés. ¿Qué te trae por aquí?", 'EN': f"Hello, {self.user_name}! It's great to hear from you! I'm Sophie, your virtual companion for practicing English. What brings you here?"},
            {'ES': f"Saludos, {self.user_name}. Aquí tienes a Sophie, lista para explorar temas en inglés contigo. ¿Sobre qué quieres hablar hoy?", 'EN': f"Greetings, {self.user_name}. Here's Sophie, ready to explore English topics with you. What would you like to talk about today?"}
        ]

    def greet(self):
        greet = random.choice(self.greetings)  # Seleccionamos un saludo aleatorio de la lista de saludos.
        return greet


if __name__ == "__main__":
    # Creamos una instancia de la clase ToGreet con el nombre de usuario 'Mailo'.
    saludo = ToGreet('Mailo').greet()
    saludo_spanish = saludo['ES']
    saludo_english = saludo['EN']
    print(saludo)
    print(saludo_english)
    print(saludo_spanish)
