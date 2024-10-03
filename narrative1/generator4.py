import sys
from typing import Optional, Union, List
from random import choice
from datetime import datetime
from Dual import DualOutput, DualInput

locations = ["dormitorio", "baño", "inicio del pasillo", "final del pasillo"]
goals = ["Cerrando la puerta del baño con llave para estar a salvo", "Moviendo el personaje al interior del baño"]
key_posibilities = {1:"pegada en la puerta", 2:"en el cajón", 3:"el bolsillo de la chaqueta", 4:"el bolsillo del pantalón", 5:"perdida"}

class Character:
    def __init__(self, name: str, location: str, is_safe: bool):
        self.name = name
        self.location = location
        self.is_safe = is_safe

    def go_start_of_aisle(self, final_step: Optional[bool] = None) -> None:
        if self.location == "dormitorio" or self.location == "final del pasillo":
            self.location = "inicio del pasillo"
            print(f"{self.name} se ha movido a {self.location}.")
            if final_step:
                self.is_safe = True
                print(f"{self.name} ha completado la meta de la historia.")
        else:
            if self.location == "inicio del pasillo":
                print(f"{self.name} ya está en el inicio del pasillo.")
            else:
                print(f"{self.name} no puede moverse a inicio del pasillo desde el {self.location}.")
        print(f"Estado actual del personaje:\n{self}")
        return

    def go_end_of_aisle(self, final_step: Optional[bool] = None) -> None:
        if self.location == "inicio del pasillo" or self.location == "baño":
            self.location = "final del pasillo"
            print(f"{self.name} se ha movido a {self.location}.")
            if final_step:
                self.is_safe = True
                print(f"{self.name} ha completado la meta de la historia.")
        else:
            if self.location == "final del pasillo":
                print(f"{self.name} ya está en el final del pasillo.")
            else:
                print(f"{self.name} no puede moverse al final del pasillo desde el {self.location}.")
        print(f"Estado actual del personaje:\n{self}")
        return

    def go_bedroom(self, final_step: Optional[bool] = None) -> None:
        if self.location == "final del pasillo":
            self.location = "dormitorio"
            print(f"{self.name} se ha movido a {self.location}.")
            if final_step:
                self.is_safe = True
                print(f"{self.name} ha completado la meta de la historia.")
        else:
            if self.location == "dormitorio":
                print(f"{self.name} ya está en el dormitorio.")
            else:
                print(f"{self.name} no puede moverse a al dormitorio desde el {self.location}.")
        print(f"Estado actual del personaje:\n{self}")
        return

    def go_bathroom(self, final_step: Optional[bool] = None) -> None:
        if self.location == "final del pasillo":
            self.location = "baño"
            print(f"{self.name} se ha movido a {self.location}.")
            if final_step:
                self.is_safe = True
                print(f"{self.name} ha completado la meta de la historia.")
        else:
            if self.location == "baño":
                print(f"{self.name} ya está en el baño.")
            else:
                print(f"{self.name} no puede moverse al baño desde el {self.location}.")
        print(f"Estado actual del personaje:\n{self}")

    def search_key(self, key_state: str, final_step: Optional[bool] = None) -> Union[bool, None]:
        if self.location == "baño":
            for ubi_key in key_posibilities:
                if key_state == key_posibilities[ubi_key]:
                    if key_state != "perdida":
                        print(f"La llave fue encontrada en {key_state}.\n")
                        return True
                    else:
                        print(f"La llave no fue encontrada.")
                        print(f"{self.name} no puede cerrar la puerta del baño, y no esta seguro.\n")
                        return False
                else:
                    print(f"La llave no fue encontrada en {key_posibilities[ubi_key]}. \nBuscando en otro lugar...\n")
            if final_step:
                self.is_safe = True
                print(f"{self.name} ha completado la meta de la historia.")
                return
        else:
            print(f"{self.name} no puede buscar la llave en {self.location}.")
        print(f"Estado actual del personaje:\n{self}")
        return

    def close_door(self, final_step: Optional[bool] = None) -> None:
        if self.location == "baño":
            print(f"{self.name} ha cerrado la puerta del baño con llave.")
            if final_step:
                self.is_safe = True
                print(f"{self.name} ha completado la meta de la historia.")
        else:
            print(f"{self.name} no puede cerrar la puerta del baño en {self.location}.")
        print(f"Estado actual del personaje:\n{self}")
        return

    def __str__(self) -> str:
        return f"Estructura del personaje {self.name}:\n- Ubicación: {self.location}\n- ¿Está seguro?: {'Sí' if self.is_safe else 'No'}\n"


def goal_bathroom(char: Character) -> None:
    char.go_start_of_aisle()
    char.go_end_of_aisle()
    char.go_bathroom(final_step=True)
    print(f"{char.name} ha entrado al baño y ahora está seguro.")
    return

def goal_close_door(char: Character, ubi_key: str) -> None:
    char.go_start_of_aisle()
    char.go_end_of_aisle()
    char.go_bathroom()
    if not char.search_key(ubi_key):
        return
    char.close_door(final_step=True)
    print(f"{char.name} ha cerrado la puerta del baño con llave y ahora está seguro.")
    return

def main():
    print("\n\t*** Generador de historias ***\n\n")
    num_chars = int(input("Ingrese el número de personajes (maximo 5) : "))
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

        if goal == 0:
            # Meta: Cerrando la puerta del baño con llave para estar a salvo
            if char.is_safe:
                print(f"Historia del personaje {char.name} complateda. El personaje ya está a salvo.")
            else:
                print("*** Estado de la llave de la puerta del baño ***")
                key_status = choice(list(key_posibilities.values()))
                print(f"\n\n * La llave está {key_status} *\n\n")
                goal_close_door(char, key_status)

        elif goal == 1:
            # Meta: Moviendo el personaje al baño
            if char.is_safe:
                print(f"Historia del personaje {char.name} completada. El personaje ya está a salvo.")
            else:
                goal_bathroom(char)

        print(f"\nEstado final del personaje:\n{char}")


if __name__ == "__main__":
    datenow = datetime.now()
    datetime = datenow.strftime("%m-%d_%H-%M")

    log_file = open(f"outputs/output_{datetime}.txt", 'w')
    dual_output = DualOutput(log_file, sys.stdout)
    dual_input = DualInput(log_file)

    sys.stdout = dual_output
    sys.stderr = dual_output
    input = dual_input

    main()

    log_file.close()
