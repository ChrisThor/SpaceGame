import pygame
import random


class Block:
    def __init__(self,
                 position,
                 size,
                 chunk,
                 colour=(123, 123, 123),
                 name="Test Block",
                 description="This is a test description",
                 solid=True,
                 hardness=1,
                 max_brightness=1):
        self.position = position
        self.chunk = chunk
        self.colour = colour
        self.alternate_colour = None
        self.name = name
        self.description = description
        # if random.randint(0, 1) == 0:
        #     solid = False
        self.solid = solid
        self.hardness = hardness
        self.size = size
        self.brightness = 0
        self.max_brightness = max_brightness

    def dismantle(self, mining_device, tickrate):
        if self.hardness > 0:
            self.hardness -= mining_device.mining_speed * tickrate
            return False
        elif self.solid:
            self.solid = False
            return True
        else:
            return False

    def place(self, colour, name, description, hardness):
        if not self.solid:
            self.solid = True
            self.colour = colour
            self.name = name
            self.description = description
            self.hardness = hardness
            return True
        return False

    def draw_block(self, background, center_x, center_y, player, zoom_factor, block_offset):
        if block_offset is None:
            relative_distance_to_player = (self.position - player.position) * zoom_factor * self.size
            pos_x_on_screen = int(center_x + relative_distance_to_player.x_value)
            pos_y_on_screen = int(
                center_y + relative_distance_to_player.y_value + player.height * zoom_factor / 2 * self.size)
        else:
            position = self.position.copy()
            position.x_value += block_offset
            relative_distance_to_player = (position - player.position) * zoom_factor * self.size
            pos_x_on_screen = int(center_x + relative_distance_to_player.x_value)
            pos_y_on_screen = int(
                center_y + relative_distance_to_player.y_value + player.height * zoom_factor / 2 * self.size)
        if self.alternate_colour is None:
            pygame.draw.rect(background,
                             (self.colour[0] * self.brightness * self.max_brightness,
                              self.colour[1] * self.brightness * self.max_brightness,
                              self.colour[2] * self.brightness * self.max_brightness),
                             (pos_x_on_screen, pos_y_on_screen,
                              self.size * zoom_factor, self.size * zoom_factor))
        else:
            pygame.draw.rect(background,
                             self.alternate_colour,
                             (pos_x_on_screen, pos_y_on_screen,
                              self.size * zoom_factor, self.size * zoom_factor))
            self.alternate_colour = None


class AirBlock(Block):
    def __init__(self, position):
        super().__init__(position, solid=False)
