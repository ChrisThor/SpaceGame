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
        if len(self.history) == 0 or self.history[len(self.history) - 1] != self.text:
            self.history.append(self.text)
        command = self.text.split(" ")
        if command[0] == "give":
            if command[1] == "object" or command[1] == "o":
                objects = os.listdir("world_objects/objects")
                if f"{command[2]}.yaml" in objects:
                    with open(f"world_objects/objects/{command[2]}.yaml", "r") as file:
                        item = yaml.safe_load(file)
                        player.blueprint = blueprint_object.BlueprintObject(
                            pygame.image.load(item["textures"][0]), command[2], "world_objects/objects")
        elif command[0] == "tp":
            if len(command) == 3:
                if command[1] != "~":
                    try:
                        if "~" in command[1]:
                            player.position.x_value += float(command[1][1:])
                        else:
                            player.position.x_value = float(command[1])
                    except ValueError:
                        pass
                if command[2] != "~":
                    try:
                        if "~" in command[2]:
                            player.position.y_value += float(command[2][1:])
                        else:
                            player.position.y_value = float(command[2])
                    except ValueError:
                        pass
        self.text = ""
