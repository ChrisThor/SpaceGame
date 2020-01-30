import math
import mining_device
import pygame
import vector


class Player:
    def __init__(self, position=vector.Vector(8, 0)):
        self.position = position
        self.speed = vector.Vector()
        self.height = 4
        self.width = 2
        self.jumps = 1
        self.max_jumps = 1
        self.bottom_blocks = []
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

    def move_player(self, direction, tickrate):
        step = direction * tickrate
        if direction > 0:
            smallest_x_distance, amount_of_nearest_blocks, blcos = self.find_smallest_x_distance(self.right_side_blocks, True)
            if len(blcos) > 0:
                if step < smallest_x_distance - self.width / 2:
                    self.position.x_value += direction * tickrate
                else:
                    pass
            else:
                self.position.x_value += direction * tickrate
        else:
            smallest_x_distance, amount_of_nearest_blocks, blcos = self.find_smallest_x_distance(self.left_side_blocks, False)
            if len(blcos) > 0:
                if step > smallest_x_distance + self.width:
                    self.position.x_value += direction * tickrate
                else:
                    pass
            else:
                self.position.x_value += direction * tickrate

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
                    amount += 1
                    blcos.append(block)
            else:
                if smallest_x_distance < relative_distance_to_player.x_value:
                    blcos = [block]
                    amount = 1
                    smallest_x_distance = relative_distance_to_player.x_value
                elif smallest_x_distance == relative_distance_to_player.x_value:
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
