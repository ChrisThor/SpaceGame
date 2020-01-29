import pygame
import chunk
import player
import vector
import math


class World:
    def __init__(self, width):
        self.chunks = []
        self.width = width
        for i in range(int(-width / 2), int(width / 2)):
            for j in range(-8, 8):
                self.chunks.append(chunk.Chunk(vector.Vector(i, j)))
        self.player = player.Player()
        self.active_chunks = []
        self.move_left = False
        self.move_right = False
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
                        self.player.speed.y_value = -250
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.move_left = False
                elif event.key == pygame.K_d:
                    self.move_right = False

        self.get_collision_blocks()

        if self.move_right:
            self.player.move_player(40, tickrate)
        elif self.move_left:
            self.player.move_player(-40, tickrate)

        self.apply_gravity(tickrate)
        self.apply_speed(tickrate)
        self.player.draw_player(background, center_x, center_y, zoom_factor)
        for chunq in self.active_chunks:
            chunq.draw_chunk(background, center_x, center_y, zoom_factor, self.player)

        return running, zoom_factor

    def apply_gravity(self, tickrate):
        gravity = 400
        if not self.player.check_blocks_underneath(tickrate, gravity):
            if self.player.speed.y_value < gravity:
                self.player.speed.y_value += gravity * tickrate
        elif self.player.speed.y_value >= 0:
            self.player.speed.y_value = 0
            self.player.jumps = self.player.max_jumps
            self.player.position.y_value = round(self.player.position.y_value / 8) * 8

    def get_active_chunks(self):
        self.active_chunks = []
        if self.player.position.x_value < -self.width / 2 * self.chunks[0].size * self.chunks[0].blocks[0][0].size:
            self.player.position.x_value += self.width * self.chunks[0].size * self.chunks[0].blocks[0][0].size
        elif self.player.position.x_value > self.width / 2 * self.chunks[0].size * self.chunks[0].blocks[0][0].size:
            self.player.position.x_value -= self.width * self.chunks[0].size * self.chunks[0].blocks[0][0].size
        neg_val = 3
        pos_val = 2
        for chunq in self.chunks:
            if -chunq.size * chunq.blocks[0][0].size * neg_val < \
                    chunq.position.x_value * chunq.size * chunq.blocks[0][0].size - self.player.position.x_value < \
                    chunq.size * chunq.blocks[0][0].size * pos_val:

                if -chunq.size * chunq.blocks[0][0].size * neg_val < \
                        chunq.position.y_value * chunq.size * chunq.blocks[0][0].size - self.player.position.y_value < \
                        chunq.size * chunq.blocks[0][0].size * pos_val:
                    self.active_chunks.append(chunq)

    def apply_speed(self, tickrate):
        self.player.position += self.player.speed * tickrate

    def get_collision_blocks(self):
        a = math.floor(self.player.position.x_value / self.chunks[0].size / self.chunks[0].blocks[0][0].size)
        b = math.floor(self.player.position.y_value / self.chunks[0].size / self.chunks[0].blocks[0][0].size)
        self.player.bottom_blocks = []
        self.player.left_side_blocks = []
        self.player.right_side_blocks = []
        # print(f"{a},{b}")
        for chunq in self.active_chunks:
            if chunq.position.x_value == a and chunq.position.y_value == b:
                for block_line in chunq.blocks:
                    for block in block_line:
                        block.alternate_colour = (245, 245, 245)
                        relative_distance_to_player = \
                            ((chunq.position * chunq.size * block.size + block.position * block.size) -
                             self.player.position)  # * zoom_factor
                        if -2 * block.size * 0.9 < relative_distance_to_player.x_value < block.size * 0.9 and \
                                relative_distance_to_player.y_value >= 0:
                            block.alternate_colour = (255, 0, 255)
                            if block.solid:
                                self.player.bottom_blocks.append(block)
                                break
                    if len(self.player.bottom_blocks) == 3:
                        # break
                        pass
                if len(self.player.bottom_blocks) == 0:
                    b += 1
                else:
                    break
        a = math.floor(self.player.position.x_value / self.chunks[0].size / self.chunks[0].blocks[0][0].size)
        b = math.floor(self.player.position.y_value / self.chunks[0].size / self.chunks[0].blocks[0][0].size)
        a_a = math.floor((self.player.position.x_value - self.player.width) / self.chunks[0].size / self.chunks[0].blocks[0][0].size)
        b_a = math.floor((self.player.position.y_value - self.player.height) / self.chunks[0].size / self.chunks[0].blocks[0][0].size)
        a_c = math.floor((self.player.position.x_value + self.player.width * 2) / self.chunks[0].size / self.chunks[0].blocks[0][0].size)
        chunk1 = None
        chunk2 = None
        chunk3 = None
        chunk4 = None
        chunk5 = None
        chunk6 = None
        for chunq_number in range(len(self.active_chunks)):
            chunq = self.active_chunks[chunq_number]
            if chunq.position.x_value == a and chunq.position.y_value == b:
                chunk1 = chunq
            elif chunq.position.x_value == a - 1 and chunq.position.y_value == b:
                chunk2 = chunq
            elif chunq.position.x_value == a and chunq.position.y_value == b - 1:
                chunk3 = chunq
            elif chunq.position.x_value == a - 1 and chunq.position.y_value == b - 1:
                chunk4 = chunq
            elif chunq.position.x_value == a + 1 and chunq.position.y_value == b:
                chunk5 = chunq
            elif chunq.position.x_value == a + 1 and chunq.position.y_value == b - 1:
                chunk6 = chunq
            if chunk1 is not None and chunk2 is not None and chunk3 is not None and chunk4 is not None and chunk5 is \
                    not None and chunk6 is not None:
                break
        use_top = False
        use_left = False
        use_right = False
        use_bottom = True
        if a_a != a:
            use_left = True
        elif a_c != a:
            use_right = True
        if b_a != b:
            use_top = True
        if self.player.position.y_value % (self.active_chunks[0].size * self.active_chunks[0].blocks[0][0].size) == 0:
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
                relative_distance_to_player = \
                    ((chanq.position * chanq.size * block.size + block.position * block.size) -
                     self.player.position)
                if block.solid and -3 * block.size < relative_distance_to_player.x_value < -self.player.width / 2 and \
                        -5 * block.size < relative_distance_to_player.y_value < 0:
                    block.alternate_colour = (255, 255, 0)
                    self.player.left_side_blocks.append(block)
                elif block.solid and 1 < relative_distance_to_player.x_value <= 2 * block.size and \
                        -5 * block.size < relative_distance_to_player.y_value < 0:
                    block.alternate_colour = (200, 200, 0)
                    self.player.right_side_blocks.append(block)
