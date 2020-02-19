import pygame
import random


class Block:
    def __init__(self,
                 position,
                 size,
                 chunk,
                 texture,
                 block_information=None,
                 colour=(123, 123, 123),
                 name="Test Block",
                 description="This is a test description",
                 solid=True,
                 hardness=1,
                 max_brightness=1,
                 containing=None):
        self.position = position
        self.chunk = chunk
        self.texture = texture
        self.used_texture = texture
        self.colour = colour
        self.alternate_colour = None
        self.name = name
        self.description = description
        self.solid_top = False
        if block_information is not None:
            if block_information * 20 > self.position.y_value:
                self.solid = False
            else:
                self.solid = True
        else:
            self.solid = solid
        # if random.randint(0, 1) == 0:
        #     solid = False
        # self.solid = solid
        self.hardness = hardness
        self.size = size
        self.brightness = 0
        self.max_brightness = max_brightness
        self.shade = pygame.Surface((int(self.size), int(self.size)))
        self.old_zoom_factor = 0
        self.containing = containing

    def dismantle(self, mining_device, tickrate):
        if self.hardness > 0:
            self.hardness -= mining_device.mining_speed * tickrate
            return False
        elif self.solid:
            self.solid = False
            self.texture = None
            self.solid_top = False
            self.containing = None
            return True
        else:
            return False

    def place(self, colour, name, description, hardness, texture):
        if not self.solid:
            self.solid = True
            self.colour = colour
            self.name = name
            self.description = description
            self.hardness = hardness
            self.texture = texture
            return True
        return False

    def draw_block(self, background, foreground, center_x, center_y, player, zoom_factor, block_offset):
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
            if self.brightness > 0:
                if self.old_zoom_factor != zoom_factor:
                    self.old_zoom_factor = zoom_factor
                    self.shade = pygame.Surface((int(self.size * zoom_factor), int(self.size * zoom_factor)))
                    self.used_texture = pygame.transform.scale(self.texture, (int(self.size * zoom_factor), int(self.size * zoom_factor)))
                background.blit(self.used_texture, (pos_x_on_screen, pos_y_on_screen))
                if self.containing is not None:
                    self.containing.draw_as_block_content(background, pos_x_on_screen, pos_y_on_screen, int(self.size * zoom_factor), zoom_factor)
                shade = -255 * self.brightness * self.max_brightness + 255
                if self.brightness != 1 or self.max_brightness != 1:
                    if self.shade.get_alpha() != shade:
                        self.shade.set_alpha(-255 * self.brightness * self.max_brightness + 255)
                    foreground.blit(self.shade, (pos_x_on_screen, pos_y_on_screen))
            else:
                pygame.draw.rect(foreground,
                                 (0, 0, 0),
                                 (pos_x_on_screen, pos_y_on_screen,
                                  self.size * zoom_factor, self.size * zoom_factor))
        else:
            pygame.draw.rect(background,
                             self.alternate_colour,
                             (pos_x_on_screen, pos_y_on_screen,
                              self.size * zoom_factor, self.size * zoom_factor))
            self.alternate_colour = None

    def draw_as_block_content(self, background, pos_x_on_screen, pos_y_on_screen, zoom, zoom_factor):
        if zoom_factor != self.old_zoom_factor:
            self.used_texture = pygame.transform.scale(self.texture, (zoom, zoom))
        background.blit(self.used_texture, (pos_x_on_screen, pos_y_on_screen))
