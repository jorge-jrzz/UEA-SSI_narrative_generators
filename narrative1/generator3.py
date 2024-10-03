import sys
from typing import Optional
from datetime import datetime


class DualOutput:
    def __init__(self, file, terminal):
        self.file = file
        self.terminal = terminal

    def write(self, message):
        self.file.write(message)
        self.terminal.write(message)

    def flush(self):
        self.file.flush()
        self.terminal.flush()


class DualInput:
    def __init__(self, file, input_func=input):
        self.file = file
        self.input_func = input_func

    def __call__(self, prompt=""):
        response = self.input_func(prompt)
        self.file.write(prompt + response + "\n")
        self.file.flush()
        return response


class Character:
    def __init__(self, name: str, location: str, is_safe: bool):
        self.name = name
        self.location = location
        self.is_safe = is_safe


    def go_start_of_aisle(self, final_step: Optional[bool] = None) -> None:
        if self.location == "dormitorio":
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
        if self.location == "inicio del pasillo":
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


locations = ["dormitorio", "baño", "inicio del pasillo", "final del pasillo"]
goals = ["Cerrando la puerta del baño con llave para estar a salvo", "Moviendo el personaje al interior del baño"]

def goal_bathroom(char: Character) -> None:
    char.go_start_of_aisle()
    char.go_end_of_aisle()
    char.go_bathroom(final_step=True)
    return

def goal_close_door(char: Character) -> None:
    char.go_start_of_aisle()
    char.go_end_of_aisle()
    char.go_bathroom()
    char.close_door(final_step=True)
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
                goal_close_door(char)
                print(f"{char.name} ha cerrado la puerta del baño con llave y ahora está seguro.")

        elif goal == 1:
            # Meta: Moviendo el personaje al baño
            if char.is_safe:
                print(f"Historia del personaje {char.name} completada. El personaje ya está a salvo.")
            else:
                goal_bathroom(char)
                print(f"{char.name} ha entrado al baño y ahora está seguro.")

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
