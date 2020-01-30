import pygame
import chunk
import player
import vector
import math


class World:
    def __init__(self, width):
        self.chunks = []
        self.general_block_size = 8
        self.general_chunk_size = 16
        self.width = width
        for i in range(int(-width / 2), int(width / 2)):
            for j in range(-8, 8):
                self.chunks.append(chunk.Chunk(vector.Vector(i, j), self.general_chunk_size, self.general_block_size))
        self.player = player.Player()
        self.active_chunks = []
        self.move_left = False
        self.move_right = False
        self.mining = False
        self.mouse_position = None
        self.player_direction = 0
        self.gravity = 1

    def access_surface(self, background, center_x, center_y, zoom_factor, tickrate):
        running = True
        self.get_active_chunks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_a:
                    self.move_left = True
                elif event.key == pygame.K_d:
                    self.move_right = True
                elif event.key == pygame.K_F2:
                    zoom_factor *= 2
                elif event.key == pygame.K_F1:
                    zoom_factor /= 2
                elif event.key == pygame.K_SPACE:
                    if self.player.jumps > 0:
                        self.player.jumps -= 1
                        self.player.speed.y_value = -31.25
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.move_left = False
                elif event.key == pygame.K_d:
                    self.move_right = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mining = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mining = False

        self.dismantle_blocks(center_x, center_y, zoom_factor, tickrate)

        self.get_collision_blocks()

        if self.move_right:
            if self.player.move_player(5, tickrate, self.active_chunks):
                self.get_collision_blocks()
        elif self.move_left:
            if self.player.move_player(-5, tickrate, self.active_chunks):
                self.get_collision_blocks()

        self.apply_gravity(tickrate)
        self.apply_speed(tickrate)
        self.player.draw_player(background, center_x, center_y, zoom_factor * self.general_block_size)
        for chunq in self.active_chunks:
            chunq.draw_chunk(background, center_x, center_y, zoom_factor, self.player)

        return running, zoom_factor

    def apply_gravity(self, tickrate):
        gravity = 50
        if not self.player.check_blocks_underneath(tickrate, gravity):
            if self.player.speed.y_value < gravity:
                self.player.speed.y_value += gravity * tickrate
        elif self.player.speed.y_value >= 0:
            self.player.speed.y_value = 0
            self.player.jumps = self.player.max_jumps
            self.player.position.y_value = round(self.player.position.y_value)

    def get_active_chunks(self):
        self.active_chunks = []
        if self.player.position.x_value < -self.width / 2 * self.general_chunk_size:
            self.player.position.x_value += self.width * self.general_chunk_size
        elif self.player.position.x_value > self.width / 2 * self.general_chunk_size:
            self.player.position.x_value -= self.width * self.general_chunk_size
        neg_val = 3
        pos_val = 2
        for chunq in self.chunks:
            if -chunq.size * neg_val < \
                    chunq.position.x_value * chunq.size - self.player.position.x_value < \
                    chunq.size * pos_val:

                if -chunq.size * neg_val < \
                        chunq.position.y_value * chunq.size - self.player.position.y_value < \
                        chunq.size * pos_val:
                    self.active_chunks.append(chunq)

    def apply_speed(self, tickrate):
        self.player.position += self.player.speed * tickrate

    def get_collision_blocks(self):
        chunk_pos_x = math.floor(self.player.position.x_value / self.general_chunk_size)
        chunk_pos_y = math.floor(self.player.position.y_value / self.general_chunk_size)
        self.player.bottom_blocks = []
        self.player.left_side_blocks = []
        self.player.right_side_blocks = []
        # print(f"{chunk_pos_x},{chunk_pos_y}")
        for chunq in self.active_chunks:
            if chunq.position.x_value == chunk_pos_x and chunq.position.y_value == chunk_pos_y:
                for block_line in chunq.blocks:
                    for block in block_line:
                        block.alternate_colour = (245, 245, 245)
                        relative_distance_to_player = block.position - self.player.position
                        if -2 < relative_distance_to_player.x_value < 1 and \
                                relative_distance_to_player.y_value >= 0:
                            block.alternate_colour = (255, 0, 255)
                            if block.solid:
                                self.player.bottom_blocks.append(block)
                                break
                    if len(self.player.bottom_blocks) == 3:
                        # break
                        pass
                if len(self.player.bottom_blocks) == 0:
                    chunk_pos_y += 1
                else:
                    break

        chunk_pos_y = math.floor(self.player.position.y_value / self.general_chunk_size)
        a_a = math.floor((self.player.position.x_value - self.player.width) / self.general_chunk_size)
        b_a = math.floor((self.player.position.y_value - self.player.height) / self.general_chunk_size)
        a_c = math.floor((self.player.position.x_value + self.player.width * 2) / self.general_chunk_size)
        chunk1 = None
        chunk2 = None
        chunk3 = None
        chunk4 = None
        chunk5 = None
        chunk6 = None
        for chunq_number in range(len(self.active_chunks)):
            chunq = self.active_chunks[chunq_number]
            if chunq.position.x_value == chunk_pos_x and chunq.position.y_value == chunk_pos_y:
                chunk1 = chunq
            elif chunq.position.x_value == chunk_pos_x - 1 and chunq.position.y_value == chunk_pos_y:
                chunk2 = chunq
            elif chunq.position.x_value == chunk_pos_x and chunq.position.y_value == chunk_pos_y - 1:
                chunk3 = chunq
            elif chunq.position.x_value == chunk_pos_x - 1 and chunq.position.y_value == chunk_pos_y - 1:
                chunk4 = chunq
            elif chunq.position.x_value == chunk_pos_x + 1 and chunq.position.y_value == chunk_pos_y:
                chunk5 = chunq
            elif chunq.position.x_value == chunk_pos_x + 1 and chunq.position.y_value == chunk_pos_y - 1:
                chunk6 = chunq
            if chunk1 is not None and chunk2 is not None and chunk3 is not None and chunk4 is not None and chunk5 is \
                    not None and chunk6 is not None:
                break
        use_top = False
        use_left = False
        use_right = False
        use_bottom = True
        if a_a != chunk_pos_x:
            use_left = True
        elif a_c != chunk_pos_x:
            use_right = True
        if b_a != chunk_pos_y:
            use_top = True
        if self.player.position.y_value % self.general_chunk_size == 0:
            use_bottom = False
        try:
            if use_bottom:
                self.sideways_check(chunk1)
        except AttributeError:
            pass
        try:
            if use_left and use_bottom:
                self.sideways_check(chunk2)
        except AttributeError:
            use_left = False
        try:
            if use_top:
                self.sideways_check(chunk3)
        except AttributeError:
            use_top = False
        try:
            if use_top and use_left:
                self.sideways_check(chunk4)
        except AttributeError:
            pass
        try:
            if use_right and use_bottom:
                self.sideways_check(chunk5)
        except AttributeError:
            use_right = False
        try:
            if use_right and use_top:
                self.sideways_check(chunk6)
        except AttributeError:
            pass

    def sideways_check(self, chanq):
        for block_line in chanq.blocks:
            for block in block_line:
                block.alternate_colour = (255, 125, 12)
                relative_distance_to_player = block.position - self.player.position
                if block.solid and -3 < relative_distance_to_player.x_value < -self.player.width / 2 and \
                        -5 < relative_distance_to_player.y_value < 0:
                    block.alternate_colour = (255, 255, 0)
                    self.player.left_side_blocks.append(block)
                elif block.solid and self.player.width / 2 <= relative_distance_to_player.x_value < 2 and \
                        -5 < relative_distance_to_player.y_value < 0:
                    block.alternate_colour = (200, 200, 0)
                    self.player.right_side_blocks.append(block)

    def dismantle_blocks(self, center_x, center_y, zoom_factor, tickrate):
        mouse_position = pygame.mouse.get_pos()
        block_pos_x = \
            math.floor(((mouse_position[0] - center_x) / (self.general_block_size * zoom_factor)) + self.player.position.x_value)
        block_pos_y = \
            math.floor(((mouse_position[1] - center_y) / (self.general_block_size * zoom_factor)) + self.player.position.y_value) - 2

        area_x_1 = block_pos_x - (self.player.mining_device.size - math.floor(self.player.mining_device.size / 2 + 1))
        area_x_2 = block_pos_x + (self.player.mining_device.size - math.ceil(self.player.mining_device.size / 2))
        area_y_1 = block_pos_y - (self.player.mining_device.size - math.floor(self.player.mining_device.size / 2 + 1))
        area_y_2 = block_pos_y + (self.player.mining_device.size - math.ceil(self.player.mining_device.size / 2))

        for chunq in self.active_chunks:
            for block_x in range(area_x_1, area_x_2 + 1):
                for block_y in range(area_y_1, area_y_2 + 1):
                    chunk_pos_x = math.floor(block_x / self.general_chunk_size)
                    chunk_pos_y = math.floor(block_y / self.general_chunk_size)

                    if chunk_pos_x == chunq.position.x_value and chunk_pos_y == chunq.position.y_value:
                        chunq.blocks[block_x % self.general_chunk_size][block_y % self.general_chunk_size].alternate_colour = (255, 50, 50)
                        if self.mining:
                            chunq.blocks[block_x % self.general_chunk_size][block_y % self.general_chunk_size].dismantle(self.player.mining_device, tickrate)
