class UserState:
    def __init__(self):
        # Diccionario para almacenar el estado de los usuarios
        self.estado_usuarios = {}



    def actualizar_estado(self,usuario, estado):
        """Actualiza el estado del usuario en el diccionario."""
        self.estado_usuarios[usuario] = estado

    def obtener_estado(self,usuario):
        """Obtiene el estado actual del usuario o 'menu' por defecto."""
        return self.estado_usuarios.get(usuario, "menu")