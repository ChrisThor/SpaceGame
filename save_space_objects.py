import pickle
import os


def save_space_objects(space_objects):
    files = os.listdir("saves")
    for file in files:
        os.unlink(f"saves\\{file}")
    for i in range(len(space_objects)):
        with open(f"saves\\space_object_{i}.so", "wb") as space_object_file:
            pickle.dump(space_objects[i], space_object_file)


def load_space_objects(space, hope_ship):
    list_of_space_objects = os.listdir("saves\\")
    space.space_objects = []

    for i in range(len(list_of_space_objects)):
        with open(f"saves\\{list_of_space_objects[i]}", "rb") as space_object_file:
            space_object = pickle.load(space_object_file)
            space.space_objects.append(space_object)
            if space_object.name == "Hope":
                hope_ship = space_object

    return hope_ship
