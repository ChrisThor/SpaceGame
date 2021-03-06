import pygame
import yaml
import os
import blueprint_object


class Chat:
    def __init__(self):
        self.text = ""
        self.font = pygame.font.Font("fonts/Roboto_Mono/RobotoMono-Light.ttf", 50)
        self.pointer_tick = 0
        self.pointer = "|"
        self.history = []
        self.history_nr = None

    def enter_text(self, event, player):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.history_nr = None
                self.interpret_command(player)
                return False
            elif event.key == pygame.K_BACKSPACE:
                if len(self.text) > 0:
                    self.text = self.text[:-1]
            elif event.key == pygame.K_UP:
                if self.history_nr is None:
                    if len(self.history) != 0:
                        self.history_nr = len(self.history) - 1
                elif self.history_nr > 0:
                    self.history_nr -= 1
                self.text = self.history[self.history_nr]
            elif event.key == pygame.K_DOWN:
                if self.history_nr is not None:
                    if self.history_nr < len(self.history) - 1:
                        self.history_nr += 1
                        self.text = self.history[self.history_nr]
                    else:
                        self.history_nr = None
                        self.text = ""
            elif event.key == pygame.K_ESCAPE:
                self.history_nr = None
                self.text = ""
                return False
            else:
                self.text += event.unicode
        return True

    def process(self, tickrate):
        self.pointer_tick += tickrate
        if self.pointer_tick > .5 and self.pointer == "|":
            self.pointer = ""
        elif self.pointer_tick > 1:
            self.pointer_tick = 0
            self.pointer = "|"
        text_surface = self.font.render(f"> {self.text}{self.pointer}", True, (255, 255, 255))
        return text_surface

    def interpret_command(self, player):
        print(self.text)
        if self.text == "":
            return
        if len(self.history) == 0 or self.history[len(self.history) - 1] != self.text:
            self.history.append(self.text)
        command = self.text.split(" ")
        if command[0] == "give":
            if len(command) == 3:
                if command[1] == "object" or command[1] == "o":
                    objects = os.listdir("world_objects/objects")
                    if f"{command[2]}.yaml" in objects:
                        with open(f"world_objects/objects/{command[2]}.yaml", "r") as file:
                            item = yaml.safe_load(file)
                            player.mining_device.tool = 2
                            player.blueprint = blueprint_object.BlueprintObject(
                                pygame.image.load(item["textures"][0]), command[2], "world_objects/objects")
                elif command[1] == "block" or command[1] == "b":
                    blocks = os.listdir("world_objects/blocks")
                    if f"{command[2]}.yaml" in blocks:
                        with open(f"world_objects/blocks/{command[2]}.yaml", "r") as file:
                            player.mining_device.tool = 1
                            player.block = yaml.safe_load(file)

        elif command[0] == "tp":
            if len(command) == 3:
                self.edit_position(command, player.position)
            elif len(command) == 2:
                if command[1] == "spawn":
                    player.position = player.start_position.copy()
                    player.position.y_value -= 0.1
                    player.speed *= 0
        elif command[0] == "setspawn":
            if len(command) == 1:
                player.start_position = player.position.copy()
            elif len(command) == 3:
                self.edit_position(command, player.start_position)
        elif command[0] == "kill":
            if len(command) == 1:
                player.take_damage(player.health_bar.hp + 1, "")
        elif command[0] == "settoolsize":
            if len(command) == 3:
                if command[1] == "mining":
                    try:
                        if int(command[2]) > 0:
                            player.mining_device.mining_size = int(command[2])
                            player.mining_device.original_mining_size = player.mining_device.mining_size
                    except ValueError:
                        pass
                if command[1] == "building":
                    try:
                        if int(command[2]) > 0:
                            player.mining_device.building_size = int(command[2])
                            player.mining_device.original_building_size = player.mining_device.building_size
                    except ValueError:
                        pass
        self.text = ""

    def edit_position(self, command, position):
        if command[1] != "~":
            try:
                if "~" in command[1]:
                    position.x_value += float(command[1][1:])
                else:
                    position.x_value = float(command[1])
            except ValueError:
                pass
        if command[2] != "~":
            try:
                if "~" in command[2]:
                    position.y_value += float(command[2][1:])
                else:
                    position.y_value = float(command[2])
            except ValueError:
                pass
