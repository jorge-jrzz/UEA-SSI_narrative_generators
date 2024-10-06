from typing import List
from random import choice
from utils import get_logger

logger = get_logger("History Generator")

class Character:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        if location != "bathroom":
            self._is_safe = False
        else:
            self._is_safe = True

    @property
    def is_safe(self):
        return self._is_safe

    @is_safe.setter
    def is_safe(self, location: str):
        if location == "bathroom":
            self._is_safe = True
        else:
            self._is_safe = False

    def get_next_location(self) -> List[str]:
        if self.location == "bedroom":
            return ["start of the aisle"]
        elif self.location == "start of the aisle":
            return ["end of the aisle", "bedroom"]
        elif self.location == "end of the aisle":
            return ["bathroom", "start of the aisle"]
        elif self.location == "bathroom":
            return ["end of the aisle"]
        return []

def generate_history(character: Character, history: List[str]):
    character.is_safe = character.location
    if character.location == "bathroom":
        # history.append(f"{character.name} is in the bathroom, and is safe.")
        history.append(f"{character.name} está en el baño, y está seguro.")
        logger.info("Acción realizada: Personaje seguro en el baño.")
    elif character.location == "bedroom":
        # history.append(f"{character.name} is in the bedroom, and is not safe.")
        history.append(f"{character.name} está en el dormitorio, y no está seguro.")
        logger.info("Acción realizada: Personaje inseguro en el dormitorio.")
    elif character.location == "start of the aisle":
        # history.append(f"{character.name} is at the start of the aisle, and is not safe.")
        history.append(f"{character.name} está al inicio del pasillo, y no está seguro.")
        logger.info("Acción realizada: Personaje inseguro al inicio del pasillo.")
    elif character.location == "end of the aisle":
        # history.append(f"{character.name} is at the end of the aisle, and is not safe; but he can go into the bathroom.")
        history.append(f"{character.name} está al final del pasillo, y no está seguro; pero puede ir al baño.")
        logger.info("Acción realizada: Personaje inseguro al final del pasillo.")

    return

rooms = ["bedroom", "bathroom", "start of the aisle", "end of the aisle"]

# Partes de la historia
story_parts = [
    "estaba en su casa cuando de repente escuchó un ruido extraño en la noche.",
    "No estaba seguro de qué hacer, pero sabía que debía encontrar un lugar seguro.",
    "Sabía que el baño era una opción, pero el camino estaba oscuro y lleno de peligros.",
    "El miedo era palpable, pero debía seguir adelante.",
    "Decidió moverse con cuidado, creía que estaría seguro.",
    "Respiró hondo y se relajó un poco, sabiendo que había encontrado un lugar seguro, al menos por ahora."
]

def final_story(history: List[str]):
    story = ""
    for i, sentence in enumerate(history):
        # Añadir la parte de la historia correspondiente (si existe)
        if i < len(story_parts):
            story += story_parts[i] + " "
        # Añadir la oración actual de la lista
        story += sentence + "\n"
    return story

if __name__ == "__main__":
    name = input("Ingrese el nombre del protagonista: ")
    room = choice(rooms)
    character = Character(name, room)
    history = []
    if not character.is_safe:
        while not character.is_safe:
            generate_history(character, history)
            room = choice(character.get_next_location())
            character.location = room
            logger.warning(f"Personaje movido a {room}.")
    else:
        generate_history(character, history)

    # Crear la historia usando las oraciones disponibles
    logger.info("Creando historia...")
    story = final_story(history)

    print(f"{character.name} {story}")
