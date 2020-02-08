import math
import mining_device
import pygame
import vector


class Player:
    def __init__(self, position_x=8):
        self.position = vector.Vector(position_x, 0)
        self.speed = vector.Vector()
        self.chunk_x = 11111111
        self.chunk_y = 11111111
        self.side_block_colour = None
        self.bottom_block_colour = None
        self.height = 3.5
        self.width = 1.75
        self.jumps = 1
        self.max_jumps = 1
        self.bottom_blocks = []
        self.top_blocks = []
        self.left_side_blocks = []
        self.right_side_blocks = []
        self.animation_state = 0
        self.animation_type = 0
        self.textures = {}
        self.flip_texture = False
        self.smallest_y_distance = None
        self.load_character_textures()
        self.current_texture = self.textures["standing"]
        self.mining_device = mining_device.MiningDevice(2, 3)

    def load_character_textures(self):
        self.textures["standing"] = pygame.image.load("textures/character/genvieve_standing.png")
        self.textures["walking0"] = pygame.image.load("textures/character/genvieve_walking_0.png")
        self.textures["walking1"] = pygame.image.load("textures/character/genvieve_walking_1.png")
        self.textures["walking2"] = pygame.image.load("textures/character/genvieve_walking_2.png")
        self.textures["walking3"] = pygame.image.load("textures/character/genvieve_walking_3.png")
        self.textures["walking4"] = pygame.image.load("textures/character/genvieve_walking_4.png")
        self.textures["walking5"] = pygame.image.load("textures/character/genvieve_walking_5.png")
        self.textures["walking6"] = pygame.image.load("textures/character/genvieve_walking_6.png")
        self.textures["walking7"] = pygame.image.load("textures/character/genvieve_walking_7.png")
        self.textures["jumping0"] = pygame.image.load("textures/character/genvieve_jumping_0.png")
        self.textures["jumping1"] = pygame.image.load("textures/character/genvieve_jumping_1.png")
        self.textures["jumping2"] = pygame.image.load("textures/character/genvieve_jumping_2.png")
        self.textures["jumping3"] = pygame.image.load("textures/character/genvieve_jumping_3.png")
        self.textures["falling0"] = pygame.image.load("textures/character/genvieve_falling_0.png")
        self.textures["falling1"] = pygame.image.load("textures/character/genvieve_falling_1.png")
        self.textures["falling2"] = pygame.image.load("textures/character/genvieve_falling_2.png")
        self.textures["falling3"] = pygame.image.load("textures/character/genvieve_falling_3.png")

    def draw_player(self, background, center_x, center_y, zoom, block_size):
        zoom_factor = zoom * block_size
        # pygame.draw.rect(background,
        #                  (255, 255, 255),
        #                  (center_x - self.width / 2 * zoom_factor,
        #                   center_y - self.height / 2 * zoom_factor,
        #                   self.width * zoom_factor,
        #                   self.height * zoom_factor))
        size = self.current_texture.get_size()
        x_offset = 1 + 3 / 8
        if self.flip_texture:
            texture = pygame.transform.flip(self.current_texture, True, False)
            x_offset = 1.625
        else:
            texture = self.current_texture
        background.blit(pygame.transform.scale(texture, (int(size[0] * zoom), int(size[1] * zoom))), (center_x - x_offset * zoom_factor,
                          center_y - 2.5 * zoom_factor))
    
    def manage_animations(self, tickrate):
        if self.speed.y_value > 0:
            if self.smallest_y_distance is not None:
                if self.smallest_y_distance > 1:
                    if self.animation_type != 2:
                        self.animation_type = 2
                        self.animation_state = 0
                    self.set_falling_animation_texture(tickrate)
                else:
                    self.set_walking_animation_texture(tickrate)
            else:
                if self.animation_type != 2:
                    self.animation_type = 2
                    self.animation_state = 0
                self.set_falling_animation_texture(tickrate)
        elif self.speed.y_value < 0:
            if self.animation_type != 3:
                self.animation_type = 3
                self.animation_state = 0
            self.set_jumping_animation_texture(tickrate)
    
    def set_walking_animation_texture(self, tickrate):
        self.animation_state += tickrate
        if self.animation_state < 1 / 8:
            self.current_texture = self.textures["walking0"]
        elif self.animation_state < 2 / 8:
            self.current_texture = self.textures["walking1"]
        elif self.animation_state < 3 / 8:
            self.current_texture = self.textures["walking2"]
        elif self.animation_state < 4 / 8:
            self.current_texture = self.textures["walking3"]
        elif self.animation_state < 5 / 8:
            self.current_texture = self.textures["walking4"]
        elif self.animation_state < 6 / 8:
            self.current_texture = self.textures["walking5"]
        elif self.animation_state < 7 / 8:
            self.current_texture = self.textures["walking6"]
        elif self.animation_state < 1:
            self.current_texture = self.textures["walking7"]
        else:
            self.animation_state = 0
            self.current_texture = self.textures["walking0"]

    def set_falling_animation_texture(self, tickrate):
        if self.animation_state < 1 / 10:
            self.current_texture = self.textures["falling0"]
        elif self.animation_state < 2 / 10:
            self.current_texture = self.textures["falling1"]
        elif self.animation_state < 3 / 10:
            self.current_texture = self.textures["falling2"]
        elif self.animation_state < 4 / 10:
            self.current_texture = self.textures["falling3"]
        self.animation_state += tickrate

    def set_jumping_animation_texture(self, tickrate):
        if self.animation_state < 1 / 10:
            self.current_texture = self.textures["jumping0"]
        elif self.animation_state < 2 / 10:
            self.current_texture = self.textures["jumping1"]
        elif self.animation_state < 3 / 10:
            self.current_texture = self.textures["jumping2"]
        elif self.animation_state < 4 / 10:
            self.current_texture = self.textures["jumping3"]
        self.animation_state += tickrate

    def move_player(self, direction, tickrate, active_chunks):
        if self.speed.y_value == 0:
            if self.animation_type != 1:
                self.animation_type = 1
                self.animation_state = 0
            self.set_walking_animation_texture(tickrate)

        step = direction * tickrate
        if direction > 0:
            smallest_x_distance, amount_of_nearest_blocks, blcos = self.find_smallest_x_distance(self.right_side_blocks, True)
            if len(blcos) > 0:
                if step < smallest_x_distance - self.width / 2:
                    self.position.x_value += direction * tickrate
                else:
                    if len(blcos) == 1 and blcos[0].position.y_value + 1 == self.position.y_value:
                        if self.do_stair_movement(blcos[0], direction, tickrate, active_chunks):
                            return True
                        else:
                            self.position.x_value = blcos[0].position.x_value - self.width / 2
                    else:
                        self.position.x_value = blcos[0].position.x_value - self.width / 2
            else:
                self.position.x_value += direction * tickrate
        else:
            smallest_x_distance, amount_of_nearest_blocks, blcos = self.find_smallest_x_distance(self.left_side_blocks, False)
            if len(blcos) > 0:
                if step > smallest_x_distance + self.width:
                    self.position.x_value += direction * tickrate
                else:
                    if len(blcos) == 1 and blcos[0].position.y_value + 1 == self.position.y_value:
                        if self.do_stair_movement(blcos[0], direction, tickrate, active_chunks):
                            return True
                        else:
                            self.position.x_value = blcos[0].position.x_value + 1 + self.width / 2
                    else:
                        self.position.x_value = blcos[0].position.x_value + 1 + self.width / 2
            else:
                self.position.x_value += direction * tickrate
        return False

    def do_stair_movement(self, block, direction, tickrate, active_chunks):
        if direction < 0:
            direc = -1
        else:
            direc = 1
        if not self.check_top_blocks(tickrate, 0):
            required_block = block.chunk.get_block_relative_to_block(block, active_chunks, x_offset=-direc, y_offset=1)
            if required_block is not None and required_block[0].solid:
                collide_block_corner = block.chunk.get_block_relative_to_block(block, active_chunks, y_offset=-4)
                if collide_block_corner is not None and not collide_block_corner[0].solid:
                    self.position.y_value -= 1.0
                    self.position.x_value += direction * tickrate
                    return True
        return False

    def find_smallest_x_distance(self, blocks, positive):
        smallest_x_distance = None
        amount = 0
        blcos = []
        for block in blocks:
            relative_distance_to_player = block.position - self.position
            if smallest_x_distance is None:
                amount = 1
                smallest_x_distance = relative_distance_to_player.x_value
                blcos.append(block)
            if positive:
                if smallest_x_distance > relative_distance_to_player.x_value:
                    blcos = [block]
                    amount = 1
                    smallest_x_distance = relative_distance_to_player.x_value
                elif smallest_x_distance == relative_distance_to_player.x_value:
                    if block not in blcos:
                        amount += 1
                        blcos.append(block)
            else:
                if smallest_x_distance < relative_distance_to_player.x_value:
                    blcos = [block]
                    amount = 1
                    smallest_x_distance = relative_distance_to_player.x_value
                elif smallest_x_distance == relative_distance_to_player.x_value:
                    if block not in blcos:
                        amount += 1
                        blcos.append(block)
        return smallest_x_distance, amount, blcos

    def check_blocks_underneath(self, tickrate, gravity):
        self.smallest_y_distance = None
        temp_block = None
        for block in self.bottom_blocks:
            relative_distance_to_player = (block.position - self.position)
            if self.smallest_y_distance is None:
                temp_block = block
                self.smallest_y_distance = relative_distance_to_player.y_value
            elif self.smallest_y_distance > relative_distance_to_player.y_value:
                temp_block = block
                self.smallest_y_distance = relative_distance_to_player.y_value

        try:
            if self.smallest_y_distance == 0:
                return True
            elif self.smallest_y_distance < 0:
                self.position.y_value = math.floor(self.position.y_value)
                return True
            else:
                temp_speed = vector.Vector(self.speed.x_value, self.speed.y_value)
                temp_speed.y_value += gravity * tickrate
                temp_position_y = self.position.y_value + temp_speed.y_value * tickrate
                temp_y = temp_block.position.y_value - temp_position_y
                if temp_y < 0:
                    self.position.y_value = temp_position_y + temp_y
                    return True
                return False
        except TypeError:
            return False

    def check_top_blocks(self, tickrate, gravity):
        smallest_y_distance = None
        temp_block = None
        for block in self.top_blocks:
            relative_distance_to_player = (block.position - self.position)
            if smallest_y_distance is None:
                temp_block = block
                smallest_y_distance = relative_distance_to_player.y_value
            elif smallest_y_distance < relative_distance_to_player.y_value:
                temp_block = block
                smallest_y_distance = relative_distance_to_player.y_value

        if smallest_y_distance is not None and temp_block is not None:
            if smallest_y_distance == -self.height - 1:
                self.speed.y_value = 0
                return True
            else:
                temp_speed = vector.Vector(self.speed.x_value, self.speed.y_value)
                temp_speed.y_value += gravity * tickrate
                temp_position_y = self.position.y_value + temp_speed.y_value * tickrate
                if temp_position_y - self.height - 1 < temp_block.position.y_value:
                    self.position.y_value = temp_block.position.y_value + self.height + 1
                    self.speed.y_value = 0
                    return True
                return False
        else:
            return False
