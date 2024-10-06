import sys
from datetime import datetime
from utils import DualOutput, DualInput


class Character:
    def __init__(self, name: str, location: str, is_safe: bool):
        self.name = name
        self.location = location
        self.is_safe = is_safe

    def get_next_location(self) -> str:
        if self.location == "dormitorio":
            return "inicio del pasillo"
        elif self.location == "inicio del pasillo":
            return "final del pasillo"
        elif self.location == "final del pasillo":
            return "baño"
        return ""

    def __str__(self):
        return f"Estructura del personaje {self.name}:\n- Ubicación: {self.location}\n- ¿Está seguro?: {'Sí' if self.is_safe else 'No'}\n"


locations = ["dormitorio", "baño", "inicio del pasillo", "final del pasillo"]
goals = ["Cerrando la puerta con llave para estar a salvo", "Moviendo el personaje al baño"]

def main():
    print("\n\t*** Generador de historias ***\n\n")
    num_chars = int(input("Ingrese el número de personajes: "))
    characters = []
    for i in range(num_chars):
        print(f"\nInformación de personaje {i + 1}:")
        name = input(f"Ingrese el nombre del personaje {i + 1}: ")
        print(f"Ingrese la ubicación del personaje {i + 1}: ")
        for index, loc in enumerate(locations):
            print(f"{index + 1}. {loc}")
        ubi = int(input("Ingrese la ubicación inicial del protagonista (número): ")) - 1
        safe = input("¿El personaje está seguro? (s/n): ")
        characters.append(Character(name, locations[ubi], False if safe == "n" else True))

    print("\n¿Cuál es la meta de la historia?")
    for index, goal in enumerate(goals):
        print(f"{index + 1}. {goal}")
    goal = int(input("Ingrese la meta de la historia (número): ")) - 1

    print("\n\t*** Empezando generación de historia ***\n")
    for i, char in enumerate(characters):
        print(f"PERSONAJE {i + 1} - {char.name}")
        print(f"Estado inicial del personaje:\n{char}")

        if char.location != "dormitorio":
            print("Historia del personaje no válida. El personaje debe estar en el dormitorio.")
            exit()

        if goal == 0:
            # Meta: Cerrando la puerta con llave para estar a salvo
            if char.is_safe:

                print(f"Historia del personaje {char.name} no válida. El personaje ya está seguro.")
            else:
                char.is_safe = True
                print(f"{char.name} ha cerrado la puerta con llave y ahora está seguro.")

        elif goal == 1:
            # Meta: Moviendo el personaje al baño
            while char.location != "baño":
                char.location = char.get_next_location()
                print(f"{char.name} se ha movido a {char.location}.")
                print(f"Estado actual del personaje:\n{char}")
            print(f"{char.name} ha llegado al baño.")
            char.is_safe = True

        print(f"\nEstado final del personaje:\n{char}")

if __name__ == "__main__":
    datenow = datetime.now()
    datetime = datenow.strftime("%m-%d_%H:%M")

    log_file = open(f"narrative1/logs/output_{datetime}.txt", 'w')
    dual_output = DualOutput(log_file, sys.stdout)
    dual_input = DualInput(log_file)

    sys.stdout = dual_output
    sys.stderr = dual_output
    input = dual_input

    main()

    log_file.close()
