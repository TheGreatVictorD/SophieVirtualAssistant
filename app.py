# Importa la clase Login del módulo loguin_gui en el paquete interface.
from interface.loguin_gui import Login

# Verifica si este script es el principal (es decir, se está ejecutando como un programa independiente).cls
if __name__ == "__main__":
    # Crea una instancia de la clase Login, que representa la interfaz de inicio de sesión.
    app = Login()
    # Inicia el bucle principal del programa, que se encarga de gestionar eventos y la interfaz gráfica.
    app.mainloop()
