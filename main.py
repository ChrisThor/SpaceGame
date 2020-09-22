import sys
import pygame
import planet_creation
import time
import gravitation
import space_object
import space_ship
import vector
import star
import tooltips
import world
from screenshot import take_screenshot as t_s
import random
import portal
import math
from save_space_objects import save_space_objects, load_space_objects


class SpaceGame:
    def __init__(self, resolution=(1800, 1000), fullscreen=False):
        self.resolution = resolution
        self.static_stars = star.create_static_stars(resolution[1], resolution[0])
        self.small_stars = star.create_small_stars(resolution[1], resolution[0])
        self.big_stars = star.create_big_stars(resolution[1], resolution[0])

        if fullscreen:
            self.screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(resolution)
        pygame.display.set_caption("STARBOUNCE")

        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill((22, 22, 22))
        self.background = self.background.convert()

        self.screen.blit(self.background, (0, 0))

        self.clock = pygame.time.Clock()

        self.fps = 60
        self.playtime = 0.0
        self.speed_factor = 1
        self.zoom_factor = 2
        self.world_zoom_factor = 3
        self.center_x = int(resolution[0] / 2)
        self.center_y = int(resolution[1] / 2)

        self.space = gravitation.Space(self.fps)
        self.hope_ship = space_ship.SpaceShip("Hope", 1e4, 5, 0, 0, 50, 50, (0, 255, 0), 8)
        self.space.space_objects.append(self.hope_ship)
        self.space.space_objects.append(space_object.SpaceObject("Großer Brocken", 1e14, 20, 0, 0, 0, 0, (50, 50, 255),
                                                                 8, static=True))
        self.template_planet_surface = None
        self.tooltip = tooltips.Tooltips()

        self.template_space_object = None

        self.running = True
        self.break_to_zero = False
        self.thrust_forward = False
        self.thrust_backwards = False
        self.turn_left = False
        self.turn_right = False
        self.draw_vectors = False
        self.debug_mode = False
        self.paused = False
        self.change_temp_mass = False
        self.takescreenshot = False
        self.show_tooltips = False
        self.particle_tick = 0
        self.framerate_stability_value = 0
        self.loop_type = 0
        self.frame_start = time.time()
        self.frame_end = self.frame_start + 1 / self.fps
        self.delta_frame = self.frame_end - self.frame_start

    def do_main_loop(self):
        while self.running:
            milliseconds = self.clock.tick(self.fps)
            self.delta_frame = self.frame_end - self.frame_start

            self.frame_start = time.time()
            self.manage_framerate()

            if self.loop_type == 0:
                self.do_space_loop(milliseconds)
            elif self.loop_type == 1:
                self.background.fill((150, 150, 255))
                self.running, self.world_zoom_factor, self.loop_type = \
                    self.template_planet_surface.access_surface(self.background,
                                                                self.center_x,
                                                                self.center_y,
                                                                self.world_zoom_factor,
                                                                self.space.tickrate,
                                                                self.loop_type)
                self.screen.blit(self.background, (0, 0))
                pygame.display.flip()
                if self.loop_type == 0:
                    self.paused = True
            if not self.paused:
                pygame.display.set_caption(f"STARBOUNCE fps: {self.fps} - playtime: {round(self.playtime, 2)}")
            else:
                pygame.display.set_caption(f"STARBOUNCE fps: {self.fps} - playtime: {round(self.playtime, 2)}  PAUSED")
                if self.particle_tick >= 1 / 3:
                    self.particle_tick = 0

            self.frame_end = time.time()
        pygame.quit()

    def get_smallest_distance_to_object(self):
        try:
            nearest_space_thing = self.space.space_objects[1]
            smallest_distance = 100
            for space_thing in self.space.space_objects:
                new_distance = (self.hope_ship.position - space_thing.position).get_length()
                if new_distance < smallest_distance and new_distance != 0:
                    smallest_distance = new_distance
                    nearest_space_thing = space_thing
        except IndexError:
            return None, None
        return nearest_space_thing, smallest_distance

    def do_space_loop(self, milliseconds):
        self.background.fill((22, 22, 22))
        nearest_space_thing, smallest_distance = self.get_smallest_distance_to_object()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_UP:
                    self.thrust_forward = True
                elif event.key == pygame.K_DOWN:
                    self.thrust_backwards = True
                elif event.key == pygame.K_LEFT:
                    self.turn_left = True
                elif event.key == pygame.K_RIGHT:
                    self.turn_right = True
                elif event.key == pygame.K_g:
                    self.break_to_zero = True
                elif event.key == pygame.K_h:
                    if self.show_tooltips:
                        self.show_tooltips = False
                    else:
                        self.show_tooltips = True
                elif event.key == pygame.K_F1:
                    if self.zoom_factor > 0.25:
                        self.zoom_factor /= 2
                    if round(self.zoom_factor, 1) == 1.00:
                        zoom_factor = 1
                elif event.key == pygame.K_F2:
                    if self.zoom_factor < 128:
                        self.zoom_factor *= 2
                    if round(self.zoom_factor, 1) == 1.00:
                        self.zoom_factor = 1
                elif event.key == pygame.K_F3:
                    if self.debug_mode:
                        self.debug_mode = False
                    else:
                        self.debug_mode = True
                elif event.key == pygame.K_F12:
                    self.takescreenshot = True
                elif event.key == pygame.K_SPACE:
                    if not self.paused and not self.hope_ship.crashed:
                        self.hope_ship.launch_bullet(self.space, self.fps)
                elif event.key == pygame.K_w:
                    if not self.paused:
                        self.hope_ship.change_thrust_power(2)
                elif event.key == pygame.K_s:
                    if not self.paused:
                        self.hope_ship.change_thrust_power(0.5)
                elif event.key == pygame.K_v:
                    if self.draw_vectors:
                        self.draw_vectors = False
                    else:
                        self.draw_vectors = True
                elif event.key == pygame.K_p:
                    if self.paused:
                        self.paused = False
                    else:
                        self.paused = True
                elif event.key == pygame.K_l:
                    if not self.hope_ship.crashed and smallest_distance is not None:
                        if smallest_distance < nearest_space_thing.radius + 30 and nearest_space_thing.radius > 5:
                            if nearest_space_thing.surface is None:
                                nearest_space_thing.generate_world(self.background, self.screen, self.resolution)
                                self.template_planet_surface = nearest_space_thing.surface
                            else:
                                self.template_planet_surface = nearest_space_thing.surface
                                self.template_planet_surface.player.position = self.template_planet_surface.player.start_position
                            self.loop_type = 1
                elif event.key == pygame.K_e:
                    if not self.paused:
                        self.speed_factor *= 2
                    else:
                        self.paused = False
                elif event.key == pygame.K_q:
                    if self.speed_factor / 2 < 1:
                        self.paused = True
                    elif not self.paused:
                        self.speed_factor = int(self.speed_factor / 2)
                elif event.key == pygame.K_c:
                    if self.template_space_object is not None:
                        if self.template_space_object.static:
                            self.template_space_object.static = False
                        else:
                            self.template_space_object.static = True
                elif event.key == pygame.K_x:
                    if self.change_temp_mass:
                        self.change_temp_mass = False
                    else:
                        self.change_temp_mass = True
                elif event.key == pygame.K_F5:
                    save_space_objects(self.space.space_objects)
                elif event.key == pygame.K_F9:
                    self.hope_ship = load_space_objects(self.space, self.hope_ship)
                    self.space.particles = []
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    self.thrust_forward = False
                    self.thrust_backwards = False
                    self.hope_ship.apply_thrust(0, self.space, self.fps)
                elif event.key == pygame.K_g:
                    self.hope_ship.apply_thrust(0, self.space, self.fps)
                    self.break_to_zero = False
                elif event.key == pygame.K_LEFT:
                    self.turn_left = False
                elif event.key == pygame.K_RIGHT:
                    self.turn_right = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                keys = pygame.mouse.get_pressed()
                if keys[0] == 1:
                    if self.template_space_object is None:
                        mouse_position = pygame.mouse.get_pos()
                        pos_x = (mouse_position[0] - self.center_x) / self.zoom_factor + self.hope_ship.position.x_value
                        pos_y = (mouse_position[1] - self.center_y) / self.zoom_factor + self.hope_ship.position.y_value
                        self.template_space_object = planet_creation.NewPlanet(vector.Vector(pos_x, pos_y))
                    else:
                        self.space.space_objects.append(
                            space_object.SpaceObject("SpaceObject",
                                                     self.template_space_object.mass,
                                                     self.template_space_object.radius,
                                                     self.template_space_object.speed.x_value,
                                                     self.template_space_object.speed.y_value,
                                                     self.template_space_object.position.x_value,
                                                     self.template_space_object.position.y_value,
                                                     self.template_space_object.particle_colour,
                                                     self.template_space_object.particle_lifetime,
                                                     static=self.template_space_object.static))
                        self.template_space_object = None
                elif event.button == 3 and self.template_space_object is not None:
                    mouse_position = pygame.mouse.get_pos()
                    end_x = (mouse_position[0] - self.center_x) / self.zoom_factor + self.hope_ship.position.x_value
                    end_y = (mouse_position[1] - self.center_y) / self.zoom_factor + self.hope_ship.position.y_value
                    speed_x = end_x - self.template_space_object.position.x_value
                    speed_y = end_y - self.template_space_object.position.y_value
                    self.template_space_object.speed = vector.Vector(speed_x, speed_y)
                elif event.button == 4 and self.template_space_object is not None:
                    if self.change_temp_mass:
                        self.template_space_object.change_mass(1)
                    else:
                        self.template_space_object.change_radius(3)
                elif event.button == 5 and self.template_space_object is not None:
                    if self.change_temp_mass:
                        self.template_space_object.change_mass(-1)
                    else:
                        self.template_space_object.change_radius(-3)
        if not self.paused:
            if self.break_to_zero:
                self.hope_ship.break_to_zero()
            elif self.thrust_forward:
                self.hope_ship.apply_thrust(1, self.space, self.fps)
            elif self.thrust_backwards:
                self.hope_ship.apply_thrust(-1, self.space, self.fps)
            if self.turn_left:
                self.hope_ship.turn_left(self.space, self.fps)
            elif self.turn_right:
                self.hope_ship.turn_right(self.space, self.fps)
            if self.template_space_object is not None:
                self.paused = True
        elif self.template_space_object is not None:
            relative_distance_to_hope_ship = (self.template_space_object.position - self.hope_ship.position) * self.zoom_factor
            pos_x_on_screen = int(self.center_x + relative_distance_to_hope_ship.x_value)
            pos_y_on_screen = int(self.center_y + relative_distance_to_hope_ship.y_value)
            self.template_space_object.draw_speed_vector(self.background, self.zoom_factor, pos_x_on_screen, pos_y_on_screen)

        print("\033[H", end="")
        if not self.paused:

            for c in range(self.speed_factor):
                self.playtime += milliseconds / 1000
                if self.particle_tick >= 1 / 3:
                    self.particle_tick = 0
                else:
                    self.particle_tick += self.space.tickrate
                for p in self.space.particles:
                    p.tick(self.space.tickrate)
                    if p.lifetime <= 0:
                        self.space.particles.remove(p)
                self.space.apply_forces(self.hope_ship, self.debug_mode, self.particle_tick)
        if not self.hope_ship.crashed and smallest_distance is not None and smallest_distance < nearest_space_thing.radius + 30 and nearest_space_thing.radius > 5:
            show_text("fonts/Roboto_Mono/RobotoMono-LightItalic.ttf", 50, (255, 0, 255), "Land (l)",
                      (50, self.resolution[1] - 100), self.background)
        self.draw_frame()
        if self.takescreenshot:
            t_s(self.background)
            self.takescreenshot = False

    def draw_frame(self):
        self.draw_stars()
        self.draw_particles()
        self.draw_space_objects()
        self.tooltip.show_tooltips(self.background, self.show_tooltips)
        self.screen.blit(self.background, (0, 0))
        if self.template_space_object is not None:
            test = display_text(self.template_space_object.mass, self.zoom_factor)
            relative_distance_to_hope_ship = (self.template_space_object.position - self.hope_ship.position) * self.zoom_factor
            pos_x_on_screen = int(self.center_x + relative_distance_to_hope_ship.x_value)
            pos_y_on_screen = int(self.center_y + relative_distance_to_hope_ship.y_value)
            self.screen.blit(test, (pos_x_on_screen + self.template_space_object.radius,
                               pos_y_on_screen + self.template_space_object.radius))
        pygame.display.flip()

    def draw_stars(self):
        for static_star in self.static_stars:
            pygame.draw.rect(self.background,
                             static_star.colour,
                             (static_star.position.x_value, static_star.position.y_value, static_star.size,
                              static_star.size))
        for small_star in self.small_stars:
            pos_x_on_screen = (self.center_x + (small_star.position.x_value - self.hope_ship.position.x_value / 3))
            pos_y_on_screen = (self.center_y + (small_star.position.y_value - self.hope_ship.position.y_value / 3))
            while pos_x_on_screen < -small_star.size:
                small_star.position.x_value += 2 * self.center_x
                pos_x_on_screen = (self.center_x + (small_star.position.x_value - self.hope_ship.position.x_value / 3))
            while pos_x_on_screen > 2 * self.center_x:
                small_star.position.x_value -= 2 * self.center_x
                pos_x_on_screen = (self.center_x + (small_star.position.x_value - self.hope_ship.position.x_value / 3))
            while pos_y_on_screen < -small_star.size:
                small_star.position.y_value += 2 * self.center_y
                pos_y_on_screen = (self.center_y + (small_star.position.y_value - self.hope_ship.position.y_value / 3))
            while pos_y_on_screen > 2 * self.center_y:
                small_star.position.y_value -= 2 * self.center_y
                pos_y_on_screen = (self.center_y + (small_star.position.y_value - self.hope_ship.position.y_value / 3))
            pygame.draw.rect(self.background,
                             small_star.colour,
                             (pos_x_on_screen, pos_y_on_screen, small_star.size, small_star.size))
        for big_star in self.big_stars:
            pos_x_on_screen = (self.center_x + (big_star.position.x_value - self.hope_ship.position.x_value / 1.8))
            pos_y_on_screen = (self.center_y + (big_star.position.y_value - self.hope_ship.position.y_value / 1.8))
            while pos_x_on_screen < -big_star.size:
                big_star.position.x_value += 2 * self.center_x
                pos_x_on_screen = (self.center_x + (big_star.position.x_value - self.hope_ship.position.x_value / 1.8))
            while pos_x_on_screen > 2 * self.center_x:
                big_star.position.x_value -= 2 * self.center_x
                pos_x_on_screen = (self.center_x + (big_star.position.x_value - self.hope_ship.position.x_value / 1.8))
            while pos_y_on_screen < -big_star.size:
                big_star.position.y_value += 2 * self.center_y
                pos_y_on_screen = (self.center_y + (big_star.position.y_value - self.hope_ship.position.y_value / 1.8))
            while pos_y_on_screen > 2 * self.center_y:
                big_star.position.y_value -= 2 * self.center_y
                pos_y_on_screen = (self.center_y + (big_star.position.y_value - self.hope_ship.position.y_value / 1.8))
            pygame.draw.rect(self.background,
                             big_star.colour,
                             (pos_x_on_screen, pos_y_on_screen, big_star.size, big_star.size))

    def draw_particles(self):
        for p in self.space.particles:
            visible = True
            for space_thing in self.space.space_objects:
                if not (space_thing.name == "Hope" or (
                        p.position - space_thing.position).get_length() > space_thing.radius) and not space_thing.crashed:
                    visible = False
                    if p.vanishable:
                        self.space.particles.remove(p)
                    break
            if visible:
                pos_x_on_screen = int(self.center_x + (
                        p.position.x_value - self.hope_ship.position.x_value) * self.zoom_factor - p.size * self.zoom_factor / 2)
                pos_y_on_screen = int(self.center_y + (
                        p.position.y_value - self.hope_ship.position.y_value) * self.zoom_factor - p.size * self.zoom_factor / 2)
                if p.is_on_screen(self.resolution[0], self.resolution[1], pos_x_on_screen, pos_y_on_screen):
                    pygame.draw.rect(self.background, p.colour,
                                     (pos_x_on_screen,
                                      pos_y_on_screen,
                                      p.size * self.zoom_factor,
                                      p.size * self.zoom_factor))

    def draw_space_objects(self):
        for space_thing in self.space.space_objects:
            if not space_thing.crashed:
                space_thing.relative_distance_to_hope_ship = (space_thing.position - self.hope_ship.position) * self.zoom_factor
                pos_x_on_screen = int(self.center_x + space_thing.relative_distance_to_hope_ship.x_value)
                pos_y_on_screen = int(self.center_y + space_thing.relative_distance_to_hope_ship.y_value)

                if space_thing.name != "Hope" and space_thing.name != "Portal":
                    radius = int(space_thing.radius * self.zoom_factor)
                    if space_thing.is_on_screen(self.resolution[0], self.resolution[1], pos_x_on_screen, pos_y_on_screen, radius):
                        pygame.draw.circle(self.background,
                                           (255, 255, 255),
                                           (pos_x_on_screen, pos_y_on_screen),
                                           radius,
                                           int(2 * self.zoom_factor))
                else:
                    if space_thing.name == "Hope":
                        pygame.draw.polygon(self.background, (255, 255, 255),
                                            ((self.center_x + space_thing.tip.x_value * self.zoom_factor,
                                              self.center_y + space_thing.tip.y_value * self.zoom_factor),
                                             (self.center_x + space_thing.bottom_left.x_value * self.zoom_factor,
                                              self.center_y + space_thing.bottom_left.y_value * self.zoom_factor),
                                             (self.center_x + space_thing.bottom.x_value * self.zoom_factor,
                                              self.center_y + space_thing.bottom.y_value * self.zoom_factor),
                                             (self.center_x + space_thing.bottom_right.x_value * self.zoom_factor,
                                              self.center_y + space_thing.bottom_right.y_value * self.zoom_factor)))
                    elif space_thing.name == "Portal":
                        pygame.draw.polygon(self.background, (255, 255, 255),
                                            ((pos_x_on_screen + space_thing.corner0.x_value * self.zoom_factor,
                                              pos_y_on_screen + space_thing.corner0.y_value * self.zoom_factor),
                                             (pos_x_on_screen + space_thing.corner1.x_value * self.zoom_factor,
                                              pos_y_on_screen + space_thing.corner1.y_value * self.zoom_factor),
                                             (pos_x_on_screen + space_thing.corner2.x_value * self.zoom_factor,
                                              pos_y_on_screen + space_thing.corner2.y_value * self.zoom_factor),
                                             (pos_x_on_screen + space_thing.corner3.x_value * self.zoom_factor,
                                              pos_y_on_screen + space_thing.corner3.y_value * self.zoom_factor)))
                if self.draw_vectors:
                    self.background = space_thing.draw_speed_vector(self.background, pos_x_on_screen, pos_y_on_screen,
                                                               self.zoom_factor)
                    self.background = space_thing.draw_acceleration_vector(self.background, pos_x_on_screen, pos_y_on_screen,
                                                                      self.zoom_factor)
                if space_thing.show_health_bar:
                    space_thing.health_bar.draw_bar(self.background, self.zoom_factor, pos_x_on_screen, pos_y_on_screen,
                                                    space_thing.radius)
            else:
                if space_thing.name != "Hope":
                    self.space.space_objects.remove(space_thing)
                    print("\033[2J")

        if self.template_space_object is not None:
            relative_distance_to_hope_ship = (self.template_space_object.position - self.hope_ship.position) * self.zoom_factor
            pos_x_on_screen = int(self.center_x + relative_distance_to_hope_ship.x_value)
            pos_y_on_screen = int(self.center_y + relative_distance_to_hope_ship.y_value)
            pygame.draw.circle(self.background,
                               (255, 255, 255),
                               (pos_x_on_screen, pos_y_on_screen),
                               int(self.template_space_object.radius * self.zoom_factor),
                               int(2 * self.zoom_factor))

    def manage_framerate(self):
        if self.delta_frame < .25:
            """
            This if-statement prevents giant steps and tickrates. When the window is moved, processing stops until it is
            released. 0.25 seconds should be a good balance, as I assume that there will never be a normal frame that takes
            longer to calculate than that.
            """
            self.space.tickrate = self.delta_frame
            self.fps = int(1 / self.delta_frame)


def main():
    pygame.init()
    # space.space_objects.append(portal.Portal(3e4, 0, 0, 50, 0, (123, 123, 123), 3, 20, math.pi / 2))
    # space.space_objects.append(portal.Portal(3e4, 0, 0, 0, -50, (123, 123, 123), 3, 20, math.pi / 2))
    # space.space_objects[1].connect_portals(space.space_objects[2])

    # for i in range(150):
    #     space.space_objects.append(space_object.SpaceObject("Ding", 1e14, 15, 0, 0, random.randint(-3500, 3500),
    #                                                         random.randint(-1600, 1600),
    #                                                         (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 5,
    #                                                         show_health_bar=False))

    # template_planet_surface = world.World(10, 32, background, screen)

    if len(sys.argv) > 0:   # if you'd like to have fullscreen, add it like this: res_x res_y True
        if len(sys.argv) == 3:
            game = SpaceGame((int(sys.argv[1]), int(sys.argv[2])))
        elif len(sys.argv) == 4:
            print(sys.argv)
            game = SpaceGame((int(sys.argv[1]), int(sys.argv[2])), fullscreen=bool(sys.argv[3]))
        else:
            exit("You should use three parameters")
    else:
        game = SpaceGame()
    game.do_main_loop()


def show_text(font_type, font_size, font_colour, text, position, background):
    font = pygame.font.Font(font_type, font_size)
    font_text = font.render(text, True, font_colour).convert_alpha()
    background.blit(font_text, position)


def display_text(msg, zoom_factor):
    font = pygame.font.SysFont("Rockwell Condensed", int(20 * zoom_factor))
    text = font.render(f"{msg / 1000000000000}e12 kg", True, (255, 255, 0))
    text = text.convert_alpha()
    return text


if __name__ == '__main__':
    main()
