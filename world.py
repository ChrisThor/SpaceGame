import pygame
import chunk
import player
import vector
import random
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
        self.all_blocks = self.get_all_blocks()
        self.calculate_light(self.chunks)
        self.player = player.Player()
        self.active_chunks = []
        self.move_left = False
        self.move_right = False
        self.tool_active = False
        self.tool_mode = 0
        self.mouse_position = None
        self.player_direction = 0
        self.gravity = 1

    def get_all_blocks(self):
        all_blocks = {}
        for chunx in self.chunks:
            for block_line in chunx.blocks:
                for block in block_line:
                    all_blocks[f"{block[0].position.x_value}_{block[0].position.y_value}"] = block
        return all_blocks

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
                    if self.player.speed.y_value == 0 and self.player.jumps > 0 and \
                            not self.player.check_top_blocks(tickrate, 50):
                        self.player.jumps -= 1
                        self.player.speed.y_value = -31.25
                elif event.key == pygame.K_x:
                    if self.tool_mode == 0:
                        self.tool_mode = 1
                    else:
                        self.tool_mode = 0
                elif event.key == pygame.K_LCTRL:
                    self.player.mining_device.size = 1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.move_left = False
                elif event.key == pygame.K_d:
                    self.move_right = False
                elif event.key == pygame.K_LCTRL:
                    self.player.mining_device.size = self.player.mining_device.original_size
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.player.mining_device.mode = 0
                    self.tool_active = True
                elif event.button == 3:
                    self.player.mining_device.mode = 1
                    self.tool_active = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 or event.button == 3:
                    self.tool_active = False

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

        for chunq in self.active_chunks:
            chunq.draw_chunk_background(background, center_x, center_y, zoom_factor, self.player)

        self.player.draw_player(background, center_x, center_y, zoom_factor * self.general_block_size)
        for chunq in self.active_chunks:
            chunq.draw_chunk_foreground(background, center_x, center_y, zoom_factor, self.player)

        return running, zoom_factor

    def apply_gravity(self, tickrate):
        gravity = 50
        if not self.player.check_top_blocks(tickrate, gravity):
            pass
        if not self.player.check_blocks_underneath(tickrate, gravity):
            if self.player.speed.y_value < gravity:
                self.player.speed.y_value += gravity * tickrate
        elif self.player.speed.y_value >= 0:
            self.player.speed.y_value = 0
            self.player.jumps = self.player.max_jumps
            self.player.position.y_value = round(self.player.position.y_value)

    def get_active_chunks(self):
        if self.player.position.x_value < -self.width / 2 * self.general_chunk_size:
            self.player.position.x_value += self.width * self.general_chunk_size
        elif self.player.position.x_value >= self.width / 2 * self.general_chunk_size:
            self.player.position.x_value -= self.width * self.general_chunk_size

        chunk_pos_x = math.floor((self.player.position.x_value + 7) / self.general_chunk_size)
        chunk_pos_y = math.floor((self.player.position.y_value + 7) / self.general_chunk_size)

        if chunk_pos_x != self.player.chunk_x or chunk_pos_y != self.player.chunk_y:
            self.active_chunks = []
            self.player.chunk_x = chunk_pos_x
            self.player.chunk_y = chunk_pos_y

            neg_val_x = -4
            pos_val_x = 3
            neg_val_y = -3
            pos_val_y = 2
            for chunq in self.chunks:
                if chunk_pos_y + neg_val_y < chunq.position.y_value < chunk_pos_y + pos_val_y:
                    if chunk_pos_x + neg_val_x < chunq.position.x_value < chunk_pos_x + pos_val_x:
                        chunq.block_offset = None
                        self.active_chunks.append(chunq)
                    elif chunk_pos_x + neg_val_x < -self.width / 2:
                        if chunk_pos_x + self.width + neg_val_x < chunq.position.x_value < self.width / 2:
                            chunq.block_offset = -self.width * self.general_chunk_size
                            self.active_chunks.append(chunq)
                    elif chunk_pos_x + pos_val_x > self.width / 2:
                        if -self.width / 2 <= chunq.position.x_value < chunk_pos_x - self.width + pos_val_x:
                            chunq.block_offset = self.width * self.general_chunk_size
                            self.active_chunks.append(chunq)

    def apply_speed(self, tickrate):
        self.player.position += self.player.speed * tickrate

    def get_chunks_above_position(self, chunk_pos_x, chunk_pos_y):
        top_chunks = []
        for chunk_ in self.active_chunks:
            if chunk_.position.x_value == chunk_pos_x:
                top_chunks.append(chunk_)
                if chunk_.position.y_value == chunk_pos_y:
                    return top_chunks

    def get_collision_blocks(self):
        chunk_pos_x = math.floor(self.player.position.x_value / self.general_chunk_size)
        chunk_pos_y = math.floor(self.player.position.y_value / self.general_chunk_size)
        self.player.bottom_blocks = []
        self.player.top_blocks = []
        self.player.left_side_blocks = []
        self.player.right_side_blocks = []
        # print(f"{chunk_pos_x},{chunk_pos_y}")
        if self.player.speed.y_value <= 0:
            top_chunks = self.get_chunks_above_position(chunk_pos_x, chunk_pos_y)
            for i in range(len(top_chunks) - 1, -1, -1):
                chunk_ = top_chunks[i]
                for block_line in chunk_.blocks:
                    for j in range(len(block_line) - 1, -1, -1):
                        block = block_line[j][0]
                        relative_distance_to_player = block.position - self.player.position
                        if block.solid and -2 < relative_distance_to_player.x_value < 1 and \
                                -self.player.height > relative_distance_to_player.y_value:
                            block.alternate_colour = (123, 123, 123)
                            self.player.top_blocks.append(block)
                            break
                    if len(self.player.top_blocks) == 3:
                        break
                if len(self.player.top_blocks) == 3:
                    break
        if self.player.speed.y_value >= 0:
            for chunq in self.active_chunks:
                if chunq.position.x_value == chunk_pos_x and chunq.position.y_value == chunk_pos_y:
                    for block_line in chunq.blocks:
                        for block in block_line:
                            block = block[0]
                            # block.alternate_colour = (245, 245, 245)
                            relative_distance_to_player = block.position - self.player.position
                            if -2 < relative_distance_to_player.x_value < 1 and \
                                    relative_distance_to_player.y_value >= 0:
                                if block.solid:
                                    block.alternate_colour = (255, 0, 255)
                                    self.player.bottom_blocks.append(block)
                                    break
                        if len(self.player.bottom_blocks) == 3:
                            break
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
                block = block[0]
                # block.alternate_colour = (255, 125, 12)
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
            math.floor(((mouse_position[0] - center_x) / (
                    self.general_block_size * zoom_factor)) + self.player.position.x_value)
        block_pos_y = \
            math.floor(((mouse_position[1] - center_y) / (
                    self.general_block_size * zoom_factor)) + self.player.position.y_value) - 2

        area_x_1 = block_pos_x - (self.player.mining_device.size - math.floor(self.player.mining_device.size / 2 + 1))
        area_x_2 = block_pos_x + (self.player.mining_device.size - math.ceil(self.player.mining_device.size / 2))
        area_y_1 = block_pos_y - (self.player.mining_device.size - math.floor(self.player.mining_device.size / 2 + 1))
        area_y_2 = block_pos_y + (self.player.mining_device.size - math.ceil(self.player.mining_device.size / 2))

        for chunq in self.active_chunks:
            for block_x in range(area_x_1, area_x_2 + 1):
                for block_y in range(area_y_1, area_y_2 + 1):
                    chunk_pos_x = math.floor(block_x / self.general_chunk_size)
                    chunk_pos_y = math.floor(block_y / self.general_chunk_size)

                    if chunk_pos_x < -self.width / 2:
                        chunk_pos_x += self.width
                    elif chunk_pos_x >= self.width / 2:
                        chunk_pos_x -= self.width

                    if chunk_pos_x == chunq.position.x_value and chunk_pos_y == chunq.position.y_value:
                        for bloq in chunq.blocks[block_x % self.general_chunk_size][block_y % self.general_chunk_size]:
                            bloq.alternate_colour = (255, 50, 50)
                        if self.tool_active:
                            if self.tool_mode == 0:
                                if chunq.blocks[block_x % self.general_chunk_size][
                                        block_y % self.general_chunk_size][self.player.mining_device.mode].dismantle(
                                        self.player.mining_device,
                                        tickrate):
                                    self.calculate_light(self.active_chunks)
                            elif self.tool_mode == 1:
                                chunq.blocks[block_x % self.general_chunk_size][
                                    block_y % self.general_chunk_size][self.player.mining_device.mode].place(
                                    (random.randint(0, 123),
                                     random.randint(0, 255),
                                     random.randint(0, 255)),
                                    "Test Block",
                                    "This is a test description",
                                    1)
                                self.calculate_light(self.active_chunks)

    def calculate_light(self, chunks):
        max_light_distance = 8
        for chunq in chunks:
            for block_line in chunq.blocks:
                for block in block_line:
                    if not block[0].solid and not block[1].solid:
                        for x in range(-max_light_distance, max_light_distance + 1):
                            for y in range(-max_light_distance, max_light_distance + 1):
                                if math.sqrt(x**2 + y**2) <= max_light_distance:
                                    try:
                                        blocks = self.all_blocks[f"{block[0].position.x_value + x}_{block[0].position.y_value + y}"]
                                    except KeyError:
                                        continue
                                    if blocks is not None:
                                        for b in blocks:
                                            try:
                                                brightness = 1 - (b.position - block[0].position).get_length() / max_light_distance
                                            except ZeroDivisionError:
                                                brightness = 1
                                            if b.brightness < brightness:
                                                b.brightness = brightness
        # a:y=sin(x)(1)/(tan(y)) (1-x^(2))0.02
