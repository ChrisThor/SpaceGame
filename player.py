import math
import mining_device
import pygame
import vector


class Player:
    def __init__(self, position=vector.Vector(8, 0)):
        self.position = position
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
        self.mining_device = mining_device.MiningDevice(2, 3)

    def draw_player(self, background, center_x, center_y, zoom_factor):
        pygame.draw.rect(background,
                         (255, 255, 255),
                         (center_x - self.width / 2 * zoom_factor,
                          center_y - self.height / 2 * zoom_factor,
                          self.width * zoom_factor,
                          self.height * zoom_factor))

    def move_player(self, direction, tickrate, active_chunks):
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
                            # self.position.x_value = math.ceil(self.position.x_value)
                            self.position.x_value = blcos[0].position.x_value - self.width / 2
                    else:
                        # self.position.x_value = math.ceil(self.position.x_value)
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
                            # self.position.x_value = math.floor(self.position.x_value)
                            self.position.x_value = blcos[0].position.x_value + 1 + self.width / 2
                    else:
                        # self.position.x_value = math.floor(self.position.x_value)
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

        # if collide_block_corner is not None:
        #     if not collide_block_corner.solid:
        #         pass
        # else:
        #     chunk_x = math.floor(self.position.x_value / block.chunk.size)
        #     chunk_y = math.floor((self.position.y_value - 4) / block.chunk.size)
        #     for chunk in active_chunks:
        #         if chunk.position.x_value == chunk_x and chunk.position.y_value == chunk_y:
        #             collide_block_corner = chunk.get_block_relative_to_block(block.position, y_offset=-4)
        #             if collide_block_corner is not None:
        #                 if not collide_block_corner.solid:
        #                     self.position.y_value -= 1.0
        #                     self.position.x_value += direction * tickrate
        #                     return True
        #                 break
        # return False

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
        smallest_y_distance = None
        temp_block = None
        for block in self.bottom_blocks:
            relative_distance_to_player = (block.position - self.position)
            if smallest_y_distance is None:
                temp_block = block
                smallest_y_distance = relative_distance_to_player.y_value
            elif smallest_y_distance > relative_distance_to_player.y_value:
                temp_block = block
                smallest_y_distance = relative_distance_to_player.y_value

        try:
            if smallest_y_distance == 0:
                return True
            elif smallest_y_distance < 0:
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
