import pygame
import chunk
import player
import vector
import noise_generator
import random
import math
import placed_object
from screenshot import take_screenshot
import chat
import yaml
from block import Block


class World:
    def __init__(self, width, height, background, screen):
        self.loading_percentage = -1
        self.chunks = []
        self.textures = {}
        self.load_textures(screen, background)
        self.black_chunk_colour = (0, 0, 0)
        self.general_block_size = 8
        self.general_chunk_size = 16
        self.width = width
        self.generate_chunks(height, width, background, screen)
        self.all_blocks = self.get_all_blocks()
        self.apply_block_variation(background, screen)
        self.max_light_distance = 8
        self.player = player.Player()
        self.set_player_position(height)
        self.calculate_world_light(background, screen, height * width)
        self.active_chunks = []
        self.move_left = False
        self.move_right = False
        self.chat_active = False
        self.take_screenshot = False
        self.down_fall = 0
        self.chat = chat.Chat()
        self.tool_active = False
        self.player.mining_device.tool = 0
        self.mouse_position = None
        self.player_direction = 0
        self.transparent_surface = pygame.Surface((1800, 1000), pygame.SRCALPHA, 32)
        self.gravity = 1

    def apply_block_variation(self, background, screen):
        value = 0
        max_value = len(self.chunks) - 1
        with open("world_objects/blocks/grass.yaml", "r") as file:
            grass = yaml.safe_load(file)
        for chunq in self.chunks:
            for block_line in chunq.blocks:
                for block in block_line:
                    blocq = chunq.get_block_relative_to_block(block[0], self.chunks, 0, -1)
                    if blocq is not None:
                        if not blocq[0].solid and not blocq[1].solid and (block[0].solid or block[1].solid):
                            block[0].containing = Block(block[0].position,
                                                        block[0].size,
                                                        chunq,
                                                        self.textures[grass["texture"]],
                                                        None,
                                                        (0, 0, 0),
                                                        grass.get("name", ""),
                                                        grass.get("description", ""),
                                                        hardness=grass.get("hardness", 0))
                            block[1].containing = Block(block[0].position,
                                                        block[0].size,
                                                        chunq,
                                                        self.textures[grass["texture"]],
                                                        None,
                                                        (0, 0, 0),
                                                        grass.get("name", ""),
                                                        grass.get("description", ""),
                                                        hardness=grass.get("hardness", 0))
                            block[0].hardness += block[0].containing.hardness
                            block[1].hardness += block[1].containing.hardness
            value += 1
            self.display_loading_text(screen, background, "Apply Block Variation...", round(value / max_value * 100))

    def set_player_position(self, height):
        y = None
        for i in range(int(-height * self.general_chunk_size / 2), int(height * self.general_chunk_size / 2)):
            for j in range(self.player.position.x_value - 1, self.player.position.x_value + 1):
                block = self.all_blocks[f"{j}_{i}"][0]
                if block.solid:
                    if y is None:
                        y = block.position.y_value
                    elif y > block.position.y_value:
                        y = block.position.y_value
        self.player.position.y_value = y

    def start_debug_mode(self):
        self.player.bottom_block_colour = (255, 0, 255)
        self.player.side_block_colour = (255, 255, 0)
        self.black_chunk_colour = (0, 255, 255)

    def stop_debug_mode(self):
        self.player.bottom_block_colour = None
        self.player.side_block_colour = None
        self.black_chunk_colour = (0, 0, 0)

    def load_textures(self, screen, background):
        self.display_loading_text(screen, background, "Loading Textures...", 0)
        self.textures["test00"] = pygame.image.load("textures/blocks/test00.png")
        self.display_loading_text(screen, background, "Loading Textures...", 0.33)
        self.textures["test01"] = pygame.image.load("textures/blocks/test02.png")
        self.display_loading_text(screen, background, "Loading Textures...", 0.67)
        self.textures["grass"] = pygame.image.load("textures/blocks/grass.png")
        self.display_loading_text(screen, background, "Loading Textures...", 1)

    def generate_chunks(self, height, width, background, screen):
        value = 0
        world_information = noise_generator.get_terrain_information(random.randint(0, 2 ** 32 - 1), width * self.general_chunk_size)
        max_value = height * width
        chunk_index = width
        for i in range(int(-width / 2), int(width / 2)):
            chunk_index -= 1
            for j in range(int(-height / 2), int(height / 2)):
                self.chunks.append(chunk.Chunk(self.textures, world_information, chunk_index, vector.Vector(i, j), self.general_chunk_size, self.general_block_size))
                value += 1
                self.display_loading_text(screen, background, "Generating World...", round(value / max_value * 100))

    def display_loading_text(self, screen, background, msg, percentage):
        if percentage != self.loading_percentage:
            self.loading_percentage = percentage
            headline = pygame.font.Font("fonts/Roboto_Mono/RobotoMono-BoldItalic.ttf", 100)
            font = pygame.font.Font("fonts/Roboto_Mono/RobotoMono-LightItalic.ttf", 50)
            headline_text = headline.render("> STARBOUNCE <", True, (255, 255, 0))
            text = font.render(f"{msg} {percentage}%", True, (255, 255, 0))
            headline_text = headline_text.convert_alpha()
            text = text.convert_alpha()
            screen.blit(background, (0, 0))
            screen.blit(text, (200, 200))
            screen.blit(headline_text, (200, 100))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit("Closed while loading")
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit("Closed while loading")

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
            if not self.chat_active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_RETURN:
                        self.chat_active = True
                    elif event.key == pygame.K_a:
                        self.move_left = True
                    elif event.key == pygame.K_d:
                        self.move_right = True
                    elif event.key == pygame.K_F2:
                        zoom_factor *= 2
                    elif event.key == pygame.K_F1:
                        zoom_factor /= 2
                    elif event.key == pygame.K_F3:
                        if self.black_chunk_colour == (0, 0, 0):
                            self.start_debug_mode()
                        else:
                            self.stop_debug_mode()
                    elif event.key == pygame.K_F12:
                        self.take_screenshot = True
                    elif event.key == pygame.K_SPACE:
                        if self.down_fall == 1:
                            self.down_fall = 2
                        elif self.player.speed.y_value == 0 and self.player.jumps > 0 and \
                                not self.player.check_top_blocks(tickrate, 50):
                            self.player.jumps -= 1
                            self.player.speed.y_value = -31.25
                    elif event.key == pygame.K_x:
                        if self.player.mining_device.tool < 2:
                            self.player.mining_device.tool += 1
                        else:
                            self.player.mining_device.tool = 0
                    elif event.key == pygame.K_LCTRL:
                        self.player.mining_device.size = 1
                        self.player.mining_device.set_surface(int(zoom_factor * self.general_block_size), self.player, self.textures)
                    elif event.key == pygame.K_s:
                        self.down_fall = 1
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.move_left = False
                    elif event.key == pygame.K_d:
                        self.move_right = False
                    elif event.key == pygame.K_LCTRL:
                        self.player.mining_device.size = self.player.mining_device.original_size
                        self.player.mining_device.set_surface(int(zoom_factor * self.general_block_size), self.player, self.textures)
                    elif event.key == pygame.K_s:
                        self.down_fall = 0
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
            else:
                self.chat_active = self.chat.enter_text(event, self.player)
                if not self.chat_active:
                    self.player.mining_device.set_surface(int(zoom_factor * self.general_block_size), self.player, self.textures)

        foreground = self.transparent_surface.copy()
        self.dismantle_blocks(center_x, center_y, zoom_factor, tickrate, foreground)

        self.get_collision_blocks()

        self.player.manage_animations(tickrate)

        if self.move_right:
            self.player.flip_texture = False
            if self.player.move_player(5, tickrate, self.active_chunks):
                self.get_collision_blocks()
        elif self.move_left:
            self.player.flip_texture = True
            if self.player.move_player(-5, tickrate, self.active_chunks):
                self.get_collision_blocks()
        elif self.player.speed.y_value == 0:
            self.player.current_texture = self.player.textures["standing"]
            self.player.animation_state = 0

        self.apply_gravity(tickrate)
        self.apply_speed(tickrate)

        objects_on_chunks = []
        for chunq in self.active_chunks:
            objects_on_chunks += chunq.draw_chunk([background, foreground], center_x, center_y, zoom_factor, self.player, self.black_chunk_colour)
        for object_on_chunk in objects_on_chunks:
            if not object_on_chunk.disabled:
                object_on_chunk.draw_object(background, self.player, zoom_factor, center_x, center_y, self.general_block_size, tickrate)
            else:
                # objects_on_chunks.remove(object_on_chunk)
                pass

        self.player.draw_player(background, center_x, center_y, zoom_factor, self.general_block_size)

        background.blit(foreground, (0, 0))

        if self.player.mining_device.tool != 2:
            self.player.mining_device.draw_affected_area(background,
                                                         int(zoom_factor * self.general_block_size),
                                                         self.player,
                                                         center_x,
                                                         center_y,
                                                         self.textures)

        if self.chat_active:
            background.blit(self.chat.process(tickrate), (0, 0))

        if self.take_screenshot:
            take_screenshot(background)
            self.take_screenshot = False

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
        rows = 0
        for chunk_ in self.active_chunks:
            if chunk_pos_x - 1 <= chunk_.position.x_value <= chunk_pos_x + 1 and chunk_pos_y - 1 <= chunk_.position.y_value <= chunk_pos_y:
                top_chunks.append(chunk_)
                if chunk_.position.y_value == chunk_pos_y:
                    rows += 1
                    if rows == 3:
                        return top_chunks
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
            if top_chunks is not None:
                for i in range(len(top_chunks) - 1, -1, -1):
                    chunk_ = top_chunks[i]
                    for block_line in chunk_.blocks:
                        for j in range(len(block_line) - 1, -1, -1):
                            block = block_line[j][0]
                            relative_distance_to_player = block.position - self.player.position
                            if block.solid and -self.player.width < relative_distance_to_player.x_value < self.player.width / 2 and \
                                    -math.ceil(self.player.height) > relative_distance_to_player.y_value:
                                if self.player.bottom_block_colour is not None:
                                    block.alternate_colour = self.player.bottom_block_colour
                                self.player.top_blocks.append(block)
                                break
                        if len(self.player.top_blocks) == 3:
                            break
                    if len(self.player.top_blocks) == 3:
                        break
        if self.player.speed.y_value >= 0:
            self.get_lower_collision_blocks(chunk_pos_x, chunk_pos_y)

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

    def get_lower_collision_blocks(self, chunk_pos_x, chunk_pos_y):
        self.get_lower_blocks_from_chunk(chunk_pos_x, chunk_pos_y)
        if len(self.player.bottom_blocks) != 3:
            new_chunk_pos_x = math.floor((self.player.position.x_value - self.player.width) / self.general_chunk_size)
            if new_chunk_pos_x != chunk_pos_x:
                self.get_lower_blocks_from_chunk(new_chunk_pos_x, chunk_pos_y)
            else:
                new_chunk_pos_x = math.floor((self.player.position.x_value + self.player.width) / self.general_chunk_size)
                if new_chunk_pos_x != chunk_pos_x:
                    self.get_lower_blocks_from_chunk(new_chunk_pos_x, chunk_pos_y)

    def get_lower_blocks_from_chunk(self, chunk_pos_x, chunk_pos_y):
        new_blocks = []
        for chunq in self.active_chunks:
            if chunq.position.x_value == chunk_pos_x and chunq.position.y_value == chunk_pos_y:
                for block_line in chunq.blocks:
                    for block in block_line:
                        block = block[0]
                        # block.alternate_colour = (245, 245, 245)
                        relative_distance_to_player = block.position - self.player.position
                        if -self.player.width < relative_distance_to_player.x_value < self.player.width / 2 and \
                                relative_distance_to_player.y_value >= 0:
                            if block.solid or self.down_fall != 2 and block.solid_top:
                                if self.player.bottom_block_colour is not None:
                                    block.alternate_colour = self.player.bottom_block_colour
                                new_blocks.append(block)
                                break
                    if len(new_blocks) + len(self.player.bottom_blocks) == 3:
                        break
                        pass
                if len(new_blocks) == 0:
                    chunk_pos_y += 1
                else:
                    break
        for bqwehejwhrk in new_blocks:
            self.player.bottom_blocks.append(bqwehejwhrk)

    def sideways_check(self, chanq):
        for block_line in chanq.blocks:
            for block in block_line:
                block = block[0]
                # block.alternate_colour = (255, 125, 12)
                relative_distance_to_player = block.position - self.player.position
                if block.solid and -3 < relative_distance_to_player.x_value <= -self.player.width / 2 and \
                        -5 < relative_distance_to_player.y_value < 0:
                    block.alternate_colour = self.player.side_block_colour
                    self.player.left_side_blocks.append(block)
                elif block.solid and self.player.width / 2 <= relative_distance_to_player.x_value < 2 and \
                        -5 < relative_distance_to_player.y_value < 0:
                    block.alternate_colour = self.player.side_block_colour
                    self.player.right_side_blocks.append(block)

    def dismantle_blocks(self, center_x, center_y, zoom_factor, tickrate, foreground):
        mouse_position = pygame.mouse.get_pos()
        block_pos_x = \
            math.floor(((mouse_position[0] - center_x) / (
                    self.general_block_size * zoom_factor)) + self.player.position.x_value)
        block_pos_y = \
            math.floor(((mouse_position[1] - center_y) / (
                    self.general_block_size * zoom_factor)) + self.player.position.y_value) - 2

        if self.player.mining_device.tool == 2:
            if self.player.blueprint is not None:
                area_x_1 = block_pos_x
                area_y_1 = block_pos_y
                blueprint_position = vector.Vector(block_pos_x,
                                                   block_pos_y + 1)
                self.player.blueprint.draw_blueprint(foreground,
                                                     self.player,
                                                     zoom_factor,
                                                     center_x,
                                                     center_y,
                                                     blueprint_position,
                                                     self.general_block_size,
                                                     self.player.flip_texture)
                if self.tool_active:
                    chunk_x = math.floor(area_x_1 / self.general_chunk_size)
                    chunk_y = math.floor(area_y_1 / self.general_chunk_size)
                    with open(f"{self.player.blueprint.path}/{self.player.blueprint.object_id}.yaml", "r") as file:
                        object_template = yaml.safe_load(file)
                        object_to_place = placed_object.PlacedObject(self.player.blueprint.object_id,
                                                                     object_template.get("name", "Default Name"),
                                                                     object_template.get("description", "This is a default description"),
                                                                     blueprint_position,
                                                                     object_template["textures"],
                                                                     self.player.flip_texture,
                                                                     object_template.get("drop", True),
                                                                     float(object_template.get("animation_tick", 0.16666666)))
                        for chunq in self.active_chunks:
                            if chunq.position.x_value == chunk_x and chunq.position.y_value == chunk_y:
                                size = [math.ceil(object_to_place.size[0] / 8), math.ceil(object_to_place.size[1] / 8)]
                                for x in range(size[0]):
                                    for y in range(size[1]):
                                        block = self.get_relative_block(
                                            self.all_blocks[f"{object_to_place.position.x_value}_{object_to_place.position.y_value}"][0],
                                            x,
                                            -y - 1)
                                        if block[0].related_object is not None:
                                            if not block[0].related_object.disabled:
                                                self.tool_active = False
                                        elif block[0].solid:
                                            self.tool_active = False
                        for chunq in self.active_chunks:
                            if chunq.position.x_value == chunk_x and chunq.position.y_value == chunk_y and self.tool_active:
                                chunq.placed_objects.append(object_to_place)
                                size = [math.ceil(object_to_place.size[0] / 8), math.ceil(object_to_place.size[1] / 8)]
                                for x in range(size[0]):
                                    if object_template.get("solid_top", False):
                                        block = self.get_relative_block(
                                            self.all_blocks[
                                                f"{object_to_place.position.x_value}_{object_to_place.position.y_value}"][
                                                0],
                                            x,
                                            -size[1])
                                        block[0].solid_top = True
                                        object_to_place.changed_blocks.append(block[0])
                                    for y in range(size[1]):
                                        block = self.get_relative_block(
                                            self.all_blocks[f"{object_to_place.position.x_value}_{object_to_place.position.y_value}"][0],
                                            x,
                                            -y - 1)
                                        object_to_place.recieving_blocks.append(block[0])
                                        block[0].related_object = object_to_place

                    self.tool_active = False

            # area_x_2 = block_pos_x + trans_flag.size[0] / self.general_block_size
            # area_y_2 = block_pos_y - trans_flag.size[1] / self.general_block_size

        area_x_1 = block_pos_x - (
                self.player.mining_device.size - math.floor(self.player.mining_device.size / 2 + 1))
        area_x_2 = block_pos_x + (self.player.mining_device.size - math.ceil(self.player.mining_device.size / 2))
        area_y_2 = block_pos_y + (self.player.mining_device.size - math.ceil(self.player.mining_device.size / 2))
        area_y_1 = block_pos_y - (
                self.player.mining_device.size - math.floor(self.player.mining_device.size / 2 + 1))

        self.player.mining_device.update_position(vector.Vector(area_x_1, area_y_1))

        if self.tool_active:
            update_light_for_blocks = []
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
                            if self.player.mining_device.tool == 0:
                                if chunq.blocks[block_x % self.general_chunk_size][
                                        block_y % self.general_chunk_size][self.player.mining_device.mode].dismantle(
                                        self.player.mining_device,
                                        tickrate):
                                    if self.player.mining_device.mode == 1 and not chunq.blocks[block_x % self.general_chunk_size][
                                            block_y % self.general_chunk_size][0].solid or self.player.mining_device.mode == 0 and \
                                            not chunq.blocks[block_x % self.general_chunk_size][
                                                block_y % self.general_chunk_size][1].solid:
                                        if not chunq.blocks[block_x % self.general_chunk_size][
                                                block_y % self.general_chunk_size][self.player.mining_device.mode - 1].solid:
                                            chunq.solid_blocks -= 1
                                            if chunq.solid_blocks == 0:
                                                chunq.state = 2
                                        update_light_for_blocks.append(chunq.blocks[block_x % self.general_chunk_size]
                                                                       [block_y % self.general_chunk_size])
                            elif self.player.mining_device.tool == 1 and self.player.block is not None:
                                if chunq.blocks[block_x % self.general_chunk_size][
                                        block_y % self.general_chunk_size][self.player.mining_device.mode].place(
                                        (random.randint(0, 123),
                                         random.randint(0, 255),
                                         random.randint(0, 255)),
                                        self.player.block.get("name", "Default block name"),
                                        self.player.block.get("description", "Default block description"),
                                        self.player.block.get("hardness", 0),
                                        self.textures[self.player.block["texture"]],
                                        int(self.general_block_size * zoom_factor)):
                                    if not chunq.blocks[block_x % self.general_chunk_size][
                                            block_y % self.general_chunk_size][self.player.mining_device.mode - 1].solid:
                                        chunq.solid_blocks += 1
                                        chunq.state = 0
                                    update_light_for_blocks.append(chunq.blocks[block_x % self.general_chunk_size]
                                                                   [block_y % self.general_chunk_size])
            self.update_light_around_block(update_light_for_blocks)

    def calculate_world_light(self, background, screen, max_value):
        value = 0
        self.display_loading_text(screen, background, "Calculating Light...", value)
        for chunq in self.chunks:
            black_blocks = 0
            for block_line in chunq.blocks:
                for block in block_line:
                    if block[0].solid or block[1].solid:
                        self.calc_light_around_block(block)
                        if block[0].brightness == 0:
                            black_blocks += 1
            if chunq.solid_blocks == 0:
                chunq.state = 2
            elif black_blocks == chunq.size ** 2:
                chunq.state = 1
            value += 1
            self.display_loading_text(screen, background, "Calculating Light...", round(value / max_value * 100))
        # a:y=sin(x)(1)/(tan(y)) (1-x^(2))0.02

    def calc_light_around_block(self, block):
        block[0].brightness = 0
        block[1].brightness = 0
        for x in range(-self.max_light_distance, self.max_light_distance + 1):
            for y in range(-self.max_light_distance, self.max_light_distance + 1):
                if math.sqrt(x ** 2 + y ** 2) <= self.max_light_distance:
                    try:
                        blocks = self.all_blocks[f"{block[0].position.x_value + x}_{block[0].position.y_value + y}"]
                    except KeyError:
                        continue
                    if blocks is not None:
                        if not blocks[0].solid and not blocks[1].solid:
                            try:
                                brightness = \
                                    1 - ((block[0].position - blocks[0].position).get_length() - 1) / self.max_light_distance
                            except ZeroDivisionError:
                                brightness = 1
                            if block[0].brightness < brightness:
                                block[0].brightness = brightness
                            if block[1].brightness < brightness:
                                block[1].brightness = brightness

    def update_light_around_block(self, block_list):
        updated_blocks = []
        updated_chunks = []
        for x in range(-self.max_light_distance, self.max_light_distance + 1):
            for y in range(-self.max_light_distance, self.max_light_distance + 1):
                if math.sqrt(x ** 2 + y ** 2) <= self.max_light_distance:
                    for block in block_list:
                        try:
                            blocks = self.all_blocks[f"{block[0].position.x_value + x}_{block[0].position.y_value + y}"]
                            if blocks is not None and (blocks[0].solid or blocks[1].solid) and blocks not in updated_blocks:
                                self.calc_light_around_block(blocks)
                                updated_blocks.append(blocks)
                                if blocks[0].chunk not in updated_chunks:
                                    updated_chunks.append(blocks[0].chunk)
                        except KeyError:
                            continue
        for chunq in updated_chunks:
            next_chunk = False
            for block_line in chunq.blocks:
                for blocks in block_line:
                    if blocks[0].brightness != 0:
                        next_chunk = True
                        break
                if next_chunk:
                    break
            if next_chunk:
                chunq.state = 0
                continue
            else:
                chunq.state = 1

    def get_relative_block(self, block, x_offset, y_offset):
        rel_block = self.all_blocks.get(f"{block.position.x_value + x_offset}_{block.position.y_value + y_offset}", None)
        if rel_block is None:
            if block.position.x_value + x_offset >= self.width * self.general_chunk_size / 2:
                rel_block = self.all_blocks.get(f"{block.position.x_value - self.width * self.general_chunk_size + x_offset}_{block.position.y_value + y_offset}")
            elif block.position.x_value + x_offset < self.width * self.general_chunk_size / 2:
                rel_block = self.all_blocks.get(f"{block.position.x_value + self.width * self.general_chunk_size + x_offset}_{block.position.y_value + y_offset}")
        return rel_block
