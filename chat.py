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

    def enter_text(self, event, player):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.interpret_command(player)
                return False
            elif event.key == pygame.K_BACKSPACE:
                if len(self.text) > 0:
                    self.text = self.text[:-1]
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
        command = self.text.split(" ")
        item = None
        if len(command) == 3:
            if command[0] == "give":
                if command[1] == "object":
                    objects = os.listdir("world_objects/objects")
                    if f"{command[2]}.yaml" in objects:
                        with open(f"world_objects/objects/{command[2]}.yaml", "r") as file:
                            item = yaml.safe_load(file)
                            player.blueprint = blueprint_object.BlueprintObject(
                                pygame.image.load(item["textures"][0]), command[2], "world_objects/objects")
        self.text = ""
