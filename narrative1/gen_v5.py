import sys
from collections import deque
from typing import Optional, Union, List
from random import choice
from datetime import datetime
from Dual import DualOutput, DualInput

locations = ["dormitorio", "baño", "inicio del pasillo", "final del pasillo"]

# Definición del grafo donde las ubicaciones son los nodos y los movimientos posibles son las aristas
# En las listas estan las ubicaciones a las que se puede mover desde la ubicación actual
graph = {
    "dormitorio": ["inicio del pasillo"],
    "inicio del pasillo": ["dormitorio", "final del pasillo"],
    "final del pasillo": ["inicio del pasillo", "baño"],
    "baño": ["final del pasillo"]
}

class Character:
    '''
    Clase que representa a un personaje en la historia.
    Cada personaje tiene un nombre, una ubicación y un estado de seguridad.
    Attributes:
        name (str): El nombre del personaje.
        location (str): La ubicación actual del personaje.
        is_safe (bool): Indica si el personaje está seguro o no
    '''

    def __init__(self, name: str, location: str, is_safe: bool):
        self.name = name
        self.location = location
        self.is_safe = is_safe

    def move_to(self, target_location: str) -> bool:
        '''
        Método para mover al personaje a una ubicación objetivo.
        Args:
            target_location (str): La ubicación a la que se quiere mover al personaje.
        Returns:
            bool: True si el movimiento fue exitoso, False en caso contrario.
        '''

        if target_location in graph[self.location]:
            print(f"{self.name} se ha movido de {self.location} a {target_location}.")
            self.location = target_location
            return True
        else:
            print(f"{self.name} no puede moverse a {target_location} desde {self.location}.")
            return False

    def find_path_to_dormitorio(self) -> List[str]:
        '''
        Método para encontrar el camino más corto desde la ubicación actual del personaje hasta el dormitorio.
        *Utiliza BFS para encontrar el camino más corto.*
        Returns:
            List[str]: Lista de ubicaciones que forman el camino más corto hacia el dormitorio.
        '''

        # BFS para encontrar el camino más corto hacia el dormitorio
        queue = deque([[self.location]])  # Cola de caminos posibles, comenzando con la ubicación actual
        visited = set()  # Conjunto para rastrear las ubicaciones visitadas

        print(f"\t@ Buscando el camino desde {self.location} al dormitorio...\n")
        while queue:
            path = queue.popleft()  # Tomamos el primer camino en la cola
            current_location = path[-1]  # Última ubicación en el camino actual

            print(f"\t@ Explorando camino: {path} (actualmente en {current_location})")

            if current_location == "dormitorio":  # Si hemos llegado al dormitorio
                print(f"\t@ ¡Camino encontrado! El camino es: {path}")
                return path

            if current_location not in visited:  # Si no hemos visitado esta ubicación
                visited.add(current_location)  # La marcamos como visitada
                print(f"\t@ Marcando {current_location} como visitado.")

                for neighbor in graph[current_location]:  # Exploramos los vecinos (ubicaciones conectadas)
                    new_path = list(path)  # Copiamos el camino actual
                    new_path.append(neighbor)  # Agregamos el vecino al nuevo camino
                    queue.append(new_path)  # Añadimos el nuevo camino a la cola
                    print(f"\t@ Agregando nuevo camino a la cola: {new_path}")

        print("\t@ No se encontró un camino hacia el dormitorio.")
        return []


    def execute_plan(self, path: List[str]) -> None:
        '''
        Método para ejecutar un plan de movimiento para el personaje.
        Args:
            path (List[str]): Lista de ubicaciones que forman el plan de movimiento
        '''

        for step in path:
            print(f"^ Intentando mover a {self.name} a {step}...")
            self.move_to(step)

    def __str__(self) -> str:
        '''
        Método para representar un objeto Character como una cadena de texto.
        Returns:
            str: Cadena de texto que representa la estructura del personaje.
       '''

        return f"\n\tEstructura del personaje {self.name}:\n\t- Ubicación: {self.location}\n\t- ¿Está seguro?: {'Sí' if self.is_safe else 'No'}\n"


def generate_story(datetime_str: str) -> None:
    '''
    Función principal para generar una historia con personajes y una meta.
    Args:
        datetime_str (str): Cadena de texto que representa la fecha y hora de ejecución.
    '''

    print(" Fecha y hora de ejecución: ", datetime_str)
    print(" Autor: Jorge Angel Juarez Vazquez\n\n")
    print("\n\t*** Generador de historias ***\n\n")
    num_chars = int(input("* Ingrese el número de personajes (maximo 5): "))
    characters = []
    goals = ["Cerrar la puerta del baño con llave para estar a salvo", "Mover el personaje al baño"]

    # Crear personajes con la información proporcionada por el usuario
    for i in range(num_chars):
        print(f"\nInformación de personaje {i + 1}:")
        name = input(f"* Ingrese el nombre del personaje {i + 1}: ")
        print(f"Ubicación del personaje {i + 1}: ")
        for index, loc in enumerate(locations):
            print(f"{index + 1}. {loc}")
        ubi = int(input("* Ingrese la ubicación inicial del protagonista (número): ")) - 1
        safe = input("* ¿El personaje está seguro? (s/n): ")
        characters.append(Character(name, locations[ubi], False if safe == "n" else True))

    print("*¿Cuál es la meta de la historia?")
    for index, goal in enumerate(goals):
        print(f"{index + 1}. {goal}")
    goal = int(input("* Ingrese la meta de la historia (número): ")) - 1

    print("\n\n\t*** Empezando generación de historia ***\n")
    for i, char in enumerate(characters):
        print(f"PERSONAJE {i + 1} - {char.name}")
        print(f"Estado inicial del personaje:\n{char}")

        if char.location != "dormitorio":
            print(f"\tEl personaje {char.name} no está en el dormitorio, no se puede iniciar ninguno de los planes.")
            print(f"\tBuscando un camino hacia el dormitorio para {char.name}...")
            path_to_dormitorio = char.find_path_to_dormitorio()
            if path_to_dormitorio:
                print(f"El personaje {char.name} está en {char.location}. Moviéndolo al dormitorio.\n\n\n")
                char.execute_plan(path_to_dormitorio)
            else:
                print(f"No se encontró un camino hacia el dormitorio para {char.name}.")
                continue

        # Aquí se puede continuar con el plan como antes, ya que el personaje está en el dormitorio
        # -----------------------------------------------------------------------------------------

        # Plan 0 - Cerrar la puerta del baño con llave para estar a salvo
        if goal == 0:
            print("\t** Estado de la llave de la puerta del baño **")
            key_status = choice(["pegada en la puerta", "en el cajón", "el bolsillo de la chaqueta", "el bolsillo del pantalón", "perdida"])
            print(f"\t** La llave está {key_status} **")
            char.execute_plan(["inicio del pasillo", "final del pasillo", "baño"])
            if char.location == "baño" and key_status != "perdida":
                char.is_safe = True
                print(f"{char.name} ha cerrado la puerta del baño y está seguro.")
            else:
                print(f"{char.name} no está seguro.")

        # Plan 1 - Mover el personaje al baño
        elif goal == 1:
            char.execute_plan(["inicio del pasillo", "final del pasillo", "baño"])
            char.is_safe = True
            print(f"{char.name} ha completado la meta de la historia y está seguro.")

        print(f"\nEstado final del personaje:\n{char}")

if __name__ == "__main__":
    datenow = datetime.now()
    datetime = datenow.strftime("%m-%d_%H-%M")

    log_file = open(f"narrative1/logs/output_{datetime}.txt", 'w', encoding='utf-8')
    dual_output = DualOutput(log_file, sys.stdout)
    dual_input = DualInput(log_file)

    sys.stdout = dual_output
    sys.stderr = dual_output
    input = dual_input

    datetime_str = datenow.strftime("%m/%d - %H:%M")
    generate_story(datetime_str)

    log_file.close()
