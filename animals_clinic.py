class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.commands = []

    def add_command(self, command):
        self.commands.append(command)

    def get_commands(self):
        return self.commands

    def __str__(self):
        return f"{self.__class__.__name__}: {self.name}, Возраст: {self.age}"

class Pet(Animal):
    pass

class PackAnimal(Animal):
    pass

class Dog(Pet):
    pass

class Cat(Pet):
    pass

class Hamster(Pet):
    pass

class Horse(PackAnimal):
    pass

class Camel(PackAnimal):
    pass

class Donkey(PackAnimal):
    pass

class Counter:
    def __init__(self):
        self.count = 0
        self.closed = False
        self.in_context = False

    def add(self):
        if not self.in_context:
            raise RuntimeError("Counter must be used within a 'with' block")
        self.count += 1

    def __enter__(self):
        self.in_context = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.closed = True
        self.in_context = False
        if exc_type:
            print(f"Exception: {exc_type}, {exc_val}")
        return True

    def ensure_closed(self):
        if not self.closed:
            raise RuntimeError("Resource not properly closed")

def create_animal(animal_type, name, age, category):
    if category == "Pet":
        class CustomPet(Pet):
            pass
        CustomPet.__name__ = animal_type
        return CustomPet(name, age)
    elif category == "PackAnimal":
        class CustomPackAnimal(PackAnimal):
            pass
        CustomPackAnimal.__name__ = animal_type
        return CustomPackAnimal(name, age)
    else:
        raise ValueError("Unknown category")

def display_animals(animals, filter_class=None):
    filtered_animals = [animal for animal in animals if isinstance(animal, filter_class)] if filter_class else animals
    if filtered_animals:
        for animal in filtered_animals:
            print(animal)
    else:
        print("Список пуст.")

def main_menu():
    counter = Counter()
    animals = []
    while True:
        print("\n1. Завести новое животное")
        print("2. Посмотреть команды животного")
        print("3. Обучить животное новой команде")
        print("4. Посмотреть всех животных")
        print("5. Посмотреть PackAnimals")
        print("6. Посмотреть Pets")
        print("7. Выйти")
        choice = input("Выберите пункт меню: ")

        if choice == '1':
            try:
                with counter:
                    animal_type = input("Введите тип животного: ").capitalize()
                    name = input("Введите имя животного: ")
                    age = input("Введите возраст животного: ")
                    if not age.isdigit():
                        print("Возраст должен быть числом. Попробуйте снова.")
                        continue
                    age = int(age)
                    category = input("Введите категорию животного (Pet или PackAnimal): ").capitalize()
                    if category not in ["Pet", "Packanimal"]:
                        print("Неизвестная категория! Попробуйте снова.")
                        continue
                    animal = create_animal(animal_type, name, age, category)
                    animals.append(animal)
                    counter.add()
            except RuntimeError as e:
                print(e)

        elif choice == '2':
            name = input("Введите имя животного: ")
            animal = next((a for a in animals if a.name == name), None)
            if animal:
                commands = animal.get_commands()
                if commands:
                    print(f"Команды животного {animal.name}: {', '.join(commands)}")
                else:
                    print(f"Животное {animal.name} не знает ни одной команды.")
            else:
                print("Животное не найдено!")

        elif choice == '3':
            name = input("Введите имя животного: ")
            animal = next((a for a in animals if a.name == name), None)
            if animal:
                command = input("Введите новую команду: ")
                animal.add_command(command)
                print(f"Животное {animal.name} обучено команде '{command}'")
            else:
                print("Животное не найдено!")

        elif choice == '4':
            print("Все животные:")
            display_animals(animals)

        elif choice == '5':
            print("Все PackAnimals:")
            display_animals(animals, PackAnimal)

        elif choice == '6':
            print("Все Pets:")
            display_animals(animals, Pet)

        elif choice == '7':
            break

        else:
            print("Неверный выбор! Пожалуйста, выберите снова.")

    try:
        counter.ensure_closed()
    except RuntimeError as e:
        print(e)

if __name__ == "__main__":
    main_menu()
