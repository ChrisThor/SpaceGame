import pygame
import random


class PlacedObject:
    def __init__(self, object_id, name, description, position, textures, flipped, droppable, animation_tick):
        self.object_id = object_id
        self.name = name
        self.description = description
        self.position = position
        self.textures = []
        for texture in textures:
            self.textures.append(pygame.image.load(texture))
        self.animation_state = 0
        self.flip_texture = flipped
        self.droppable = droppable
        if flipped:
            self.flip_textures()
        self.current_texture = self.textures[0]
        self.size = self.textures[0].get_size()
        self.block_offset = None
        self.frame_length = animation_tick
        self.hardness = 3
        self.recieving_blocks = []
        self.changed_blocks = []
        self.touched = False
        self.disabled = False

    def flip_textures(self):
        for i in range(len(self.textures)):
            self.textures[i] = pygame.transform.flip(self.textures[i], True, False)

    def draw_object(self, background, player, zoom_factor, center_x, center_y, block_size, tickrate):
        if self.touched:
            self.touched = False
        elif self.hardness < 3:
            self.hardness += tickrate
            if self.hardness > 3:
                self.hardness = 3
        self.animate(tickrate)
        zoom = zoom_factor * block_size
        if self.block_offset is None:
            position = self.position
        else:
            position = self.position.copy()
            position.x_value += self.block_offset
        jump_x = random.randint(0, int(1000 * ((3 - self.hardness) / 3))) / 70
        jump_y = random.randint(0, int(1000 * ((3 - self.hardness) / 3))) / 70
        relative_distance_to_player = (position - player.position) * zoom
        screen_position = (center_x + relative_distance_to_player.x_value + jump_x,
                           center_y + relative_distance_to_player.y_value - self.size[1] * zoom_factor + 1.75 * zoom + jump_y)
        background.blit(pygame.transform.scale(self.current_texture,
                                               (int(self.size[0] * zoom_factor), int(self.size[1] * zoom_factor))),
                        screen_position)

    def animate(self, tickrate):
        amount_of_textures = len(self.textures)
        if amount_of_textures > 1:
            if self.animation_state > amount_of_textures * self.frame_length:
                self.animation_state -= amount_of_textures * self.frame_length
            else:
                self.animation_state += tickrate

            for i in range(amount_of_textures):
                if self.animation_state < self.frame_length * i + self.frame_length:
                    self.current_texture = self.textures[i]
                    break

    def delete_blocks(self):
        for block in self.changed_blocks:
            block.solid_top = False
        # blocks = self.recieving_blocks.copy()
        # for block in blocks:
        #     if block.related_object.hardness < 0 and self != block.related_object:
        #         block.related_object = None
