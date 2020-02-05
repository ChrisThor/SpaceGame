import pygame
import planet_creation
import time
import gravitation
import space_object
import space_ship
import vector
import star
import world
import random
import portal
import math
from save_space_objects import save_space_objects, load_space_objects


def draw_stars(static_stars, small_stars, big_stars, background, hope_ship, center_x, center_y):
    for static_star in static_stars:
        pygame.draw.rect(background,
                         static_star.colour,
                         (static_star.position.x_value, static_star.position.y_value, static_star.size,
                          static_star.size))
    for small_star in small_stars:
        pos_x_on_screen = (center_x + (small_star.position.x_value - hope_ship.position.x_value / 3))
        pos_y_on_screen = (center_y + (small_star.position.y_value - hope_ship.position.y_value / 3))
        while pos_x_on_screen < -small_star.size:
            small_star.position.x_value += 2 * center_x
            pos_x_on_screen = (center_x + (small_star.position.x_value - hope_ship.position.x_value / 3))
        while pos_x_on_screen > 2 * center_x:
            small_star.position.x_value -= 2 * center_x
            pos_x_on_screen = (center_x + (small_star.position.x_value - hope_ship.position.x_value / 3))
        while pos_y_on_screen < -small_star.size:
            small_star.position.y_value += 2 * center_y
            pos_y_on_screen = (center_y + (small_star.position.y_value - hope_ship.position.y_value / 3))
        while pos_y_on_screen > 2 * center_y:
            small_star.position.y_value -= 2 * center_y
            pos_y_on_screen = (center_y + (small_star.position.y_value - hope_ship.position.y_value / 3))
        pygame.draw.rect(background,
                         small_star.colour,
                         (pos_x_on_screen, pos_y_on_screen, small_star.size, small_star.size))
    for big_star in big_stars:
        pos_x_on_screen = (center_x + (big_star.position.x_value - hope_ship.position.x_value / 1.8))
        pos_y_on_screen = (center_y + (big_star.position.y_value - hope_ship.position.y_value / 1.8))
        while pos_x_on_screen < -big_star.size:
            big_star.position.x_value += 2 * center_x
            pos_x_on_screen = (center_x + (big_star.position.x_value - hope_ship.position.x_value / 1.8))
        while pos_x_on_screen > 2 * center_x:
            big_star.position.x_value -= 2 * center_x
            pos_x_on_screen = (center_x + (big_star.position.x_value - hope_ship.position.x_value / 1.8))
        while pos_y_on_screen < -big_star.size:
            big_star.position.y_value += 2 * center_y
            pos_y_on_screen = (center_y + (big_star.position.y_value - hope_ship.position.y_value / 1.8))
        while pos_y_on_screen > 2 * center_y:
            big_star.position.y_value -= 2 * center_y
            pos_y_on_screen = (center_y + (big_star.position.y_value - hope_ship.position.y_value / 1.8))
        pygame.draw.rect(background,
                         big_star.colour,
                         (pos_x_on_screen, pos_y_on_screen, big_star.size, big_star.size))
    return background


def main():
    pygame.init()
    print("\033[2J")
    pygame.display.set_caption("SPAACE")

    screen_height = 1000
    screen_width = 1800
    static_stars = star.create_static_stars(screen_height, screen_width)
    small_stars = star.create_small_stars(screen_height, screen_width)
    big_stars = star.create_big_stars(screen_height, screen_width)

    screen = pygame.display.set_mode((screen_width, screen_height))

    background = pygame.Surface(screen.get_size())
    background.fill((22, 22, 22))
    background = background.convert()

    screen.blit(background, (0, 0))

    clock = pygame.time.Clock()

    fps = 60
    playtime = 0.0
    speed_factor = 1
    zoom_factor = 2
    world_zoom_factor = 3
    center_x = int(screen_width / 2)
    center_y = int(screen_height / 2)

    space = gravitation.Space(fps)
    hope_ship = space_ship.SpaceShip("Hope", 1e4, 5, 0, 0, 50, 50, (0, 255, 0), 8)
    space.space_objects.append(hope_ship)
    space.space_objects.append(space_object.SpaceObject("Großer Brocken", 1e14, 20, 0, 0, 0, 0, (50, 50, 255), 8,
                                                        static=True))
    # space.space_objects.append(portal.Portal(3e4, 0, 0, 50, 0, (123, 123, 123), 3, 20, math.pi / 2))
    # space.space_objects.append(portal.Portal(3e4, 0, 0, 0, -50, (123, 123, 123), 3, 20, math.pi / 2))
    # space.space_objects[1].connect_portals(space.space_objects[2])

    # for i in range(150):
    #     space.space_objects.append(space_object.SpaceObject("Ding", 1e14, 15, 0, 0, random.randint(-3500, 3500),
    #                                                         random.randint(-1600, 1600),
    #                                                         (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 5,
    #                                                         show_health_bar=False))

    template_planet_surface = world.World(10, 32)

    template_space_object = None

    running = True
    break_to_zero = False
    thrust_forward = False
    thrust_backwards = False
    turn_left = False
    turn_right = False
    draw_vectors = False
    debug_mode = False
    paused = False
    change_temp_mass = False
    particle_tick = 0
    framerate_stability_value = 0
    loop_type = 1
    frame_start = time.time()
    frame_end = time.time()

    while running:
        milliseconds = clock.tick(fps)
        delta_frame = frame_end - frame_start

        frame_start = time.time()
        fps, framerate_stability_value = manage_framerate(delta_frame, fps, framerate_stability_value, space)

        if loop_type == 0:
            background.fill((22, 22, 22))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_UP:
                        thrust_forward = True
                    elif event.key == pygame.K_DOWN:
                        thrust_backwards = True
                    elif event.key == pygame.K_LEFT:
                        turn_left = True
                    elif event.key == pygame.K_RIGHT:
                        turn_right = True
                    elif event.key == pygame.K_g:
                        break_to_zero = True
                    elif event.key == pygame.K_F1:
                        if zoom_factor > 0.25:
                            zoom_factor /= 2
                        if round(zoom_factor, 1) == 1.00:
                            zoom_factor = 1
                    elif event.key == pygame.K_F2:
                        if zoom_factor < 128:
                            zoom_factor *= 2
                        if round(zoom_factor, 1) == 1.00:
                            zoom_factor = 1
                    elif event.key == pygame.K_F3:
                        if debug_mode:
                            debug_mode = False
                            print("\033[2J")
                        else:
                            debug_mode = True
                    elif event.key == pygame.K_SPACE:
                        if not paused:
                            hope_ship.launch_bullet(space, fps)
                    elif event.key == pygame.K_w:
                        if not paused:
                            hope_ship.change_thrust_power(2)
                    elif event.key == pygame.K_s:
                        if not paused:
                            hope_ship.change_thrust_power(0.5)
                    elif event.key == pygame.K_v:
                        if draw_vectors:
                            draw_vectors = False
                        else:
                            draw_vectors = True
                    elif event.key == pygame.K_p:
                        if paused:
                            paused = False
                        else:
                            paused = True
                    elif event.key == pygame.K_e:
                        if not paused:
                            speed_factor += 1
                        else:
                            paused = False
                    elif event.key == pygame.K_q:
                        if speed_factor - 1 == 0:
                            paused = True
                        elif not paused:
                            speed_factor -= 1
                    elif event.key == pygame.K_c:
                        if template_space_object is not None:
                            template_space_object.static = True
                    elif event.key == pygame.K_x:
                        if change_temp_mass:
                            change_temp_mass = False
                        else:
                            change_temp_mass = True
                    elif event.key == pygame.K_F5:
                        save_space_objects(space.space_objects)
                    elif event.key == pygame.K_F9:
                        hope_ship = load_space_objects(space, hope_ship)
                        space.particles = []
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        thrust_forward = False
                        thrust_backwards = False
                        hope_ship.apply_thrust(0, space, fps)
                    elif event.key == pygame.K_g:
                        hope_ship.apply_thrust(0, space, fps)
                        break_to_zero = False
                    elif event.key == pygame.K_LEFT:
                        turn_left = False
                    elif event.key == pygame.K_RIGHT:
                        turn_right = False
                    elif event.key == pygame.K_c:
                        if template_space_object is not None:
                            template_space_object.static = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    keys = pygame.mouse.get_pressed()
                    if keys[0] == 1:
                        if template_space_object is None:
                            mouse_position = pygame.mouse.get_pos()
                            pos_x = (mouse_position[0] - center_x) / zoom_factor + hope_ship.position.x_value
                            pos_y = (mouse_position[1] - center_y) / zoom_factor + hope_ship.position.y_value
                            template_space_object = planet_creation.NewPlanet(vector.Vector(pos_x, pos_y))
                        else:
                            space.space_objects.append(space_object.SpaceObject("SpaceObject",
                                                                                template_space_object.mass,
                                                                                template_space_object.radius,
                                                                                template_space_object.speed.x_value,
                                                                                template_space_object.speed.y_value,
                                                                                template_space_object.position.x_value,
                                                                                template_space_object.position.y_value,
                                                                                template_space_object.particle_colour,
                                                                                template_space_object.particle_lifetime,
                                                                                static=template_space_object.static))
                            template_space_object = None
                    elif event.button == 3 and template_space_object is not None:
                        mouse_position = pygame.mouse.get_pos()
                        end_x = (mouse_position[0] - center_x) / zoom_factor + hope_ship.position.x_value
                        end_y = (mouse_position[1] - center_y) / zoom_factor + hope_ship.position.y_value
                        speed_x = end_x - template_space_object.position.x_value
                        speed_y = end_y - template_space_object.position.y_value
                        template_space_object.speed = vector.Vector(speed_x, speed_y)
                    elif event.button == 4 and template_space_object is not None:
                        if change_temp_mass:
                            template_space_object.change_mass(1)
                        else:
                            template_space_object.change_radius(3)
                    elif event.button == 5 and template_space_object is not None:
                        if change_temp_mass:
                            template_space_object.change_mass(-1)
                        else:
                            template_space_object.change_radius(-3)
            if not paused:
                if break_to_zero:
                    hope_ship.break_to_zero()
                elif thrust_forward:
                    hope_ship.apply_thrust(1, space, fps)
                elif thrust_backwards:
                    hope_ship.apply_thrust(-1, space, fps)
                if turn_left:
                    hope_ship.turn_left(space, fps)
                elif turn_right:
                    hope_ship.turn_right(space, fps)
                if template_space_object is not None:
                    paused = True
            elif template_space_object is not None:
                relative_distance_to_hope_ship = (template_space_object.position - hope_ship.position) * zoom_factor
                pos_x_on_screen = int(center_x + relative_distance_to_hope_ship.x_value)
                pos_y_on_screen = int(center_y + relative_distance_to_hope_ship.y_value)
                template_space_object.draw_speed_vector(background, zoom_factor, pos_x_on_screen, pos_y_on_screen)

            print("\033[H", end="")
            if not paused:

                for c in range(speed_factor):
                    playtime += milliseconds / 1000
                    if particle_tick >= 1 / 3:
                        particle_tick = 0
                    else:
                        particle_tick += space.tickrate
                    for p in space.particles:
                        p.tick(space.tickrate)
                        if p.lifetime <= 0:
                            space.particles.remove(p)
                    space.apply_forces(hope_ship, debug_mode, particle_tick)

            draw_frame(background, big_stars, center_x, center_y, draw_vectors, hope_ship, screen,
                       screen_height, screen_width, small_stars, space, static_stars, template_space_object, zoom_factor)
        elif loop_type == 1:
            background.fill((150, 150, 255))
            running, world_zoom_factor = template_planet_surface.access_surface(background, center_x, center_y, world_zoom_factor, space.tickrate)
            screen.blit(background, (0, 0))
            pygame.display.flip()
        if not paused:
            pygame.display.set_caption(f"SPAACE fps: {fps} - playtime: {round(playtime, 2)}")
        else:
            pygame.display.set_caption(f"SPAACE fps: {fps} - playtime: {round(playtime, 2)}  PAUSED")
            if particle_tick >= 1 / 3:
                particle_tick = 0

        frame_end = time.time()
        print(f"Deltaframe: {round(delta_frame, 4)}    ")
        print(f"Tickrate:   {round(space.tickrate, 4)}   \n"
              f"                                   ")
    pygame.quit()


def display_text(msg, zoom_factor):
    font = pygame.font.SysFont("Rockwell Condensed", int(20 * zoom_factor))
    text = font.render(f"{msg / 1000000000000}e12 kg", True, (255, 255, 0))
    text = text.convert_alpha()
    return text


def draw_frame(background, big_stars, center_x, center_y, draw_vectors, hope_ship, screen,
               screen_height, screen_width, small_stars, space, static_stars, template_space_object, zoom_factor):
    draw_stars(static_stars, small_stars, big_stars, background, hope_ship, center_x, center_y)
    draw_particles(background, center_x, center_y, hope_ship, screen_width, space, zoom_factor)
    draw_space_objects(background, center_x, center_y, draw_vectors, hope_ship,
                       screen_height, screen_width, space, zoom_factor, template_space_object)
    screen.blit(background, (0, 0))
    if template_space_object is not None:
        test = display_text(template_space_object.mass, zoom_factor)
        relative_distance_to_hope_ship = (template_space_object.position - hope_ship.position) * zoom_factor
        pos_x_on_screen = int(center_x + relative_distance_to_hope_ship.x_value)
        pos_y_on_screen = int(center_y + relative_distance_to_hope_ship.y_value)
        screen.blit(test, (pos_x_on_screen + template_space_object.radius,
                           pos_y_on_screen + template_space_object.radius))
    pygame.display.flip()


def draw_space_objects(background, center_x, center_y, draw_vectors, hope_ship, screen_height,
                       screen_width, space, zoom_factor, temp_space_object):
    for space_thing in space.space_objects:
        if not space_thing.crashed:
            space_thing.relative_distance_to_hope_ship = (space_thing.position - hope_ship.position) * zoom_factor
            pos_x_on_screen = int(center_x + space_thing.relative_distance_to_hope_ship.x_value)
            pos_y_on_screen = int(center_y + space_thing.relative_distance_to_hope_ship.y_value)

            if space_thing.name != "Hope" and space_thing.name != "Portal":
                radius = int(space_thing.radius * zoom_factor)
                if space_thing.is_on_screen(screen_width, screen_height, pos_x_on_screen, pos_y_on_screen, radius):
                    pygame.draw.circle(background,
                                       (255, 255, 255),
                                       (pos_x_on_screen, pos_y_on_screen),
                                       radius,
                                       int(2 * zoom_factor))
            else:
                if space_thing.name == "Hope":
                    pygame.draw.polygon(background, (255, 255, 255),
                                        ((center_x + space_thing.tip.x_value * zoom_factor,
                                          center_y + space_thing.tip.y_value * zoom_factor),
                                         (center_x + space_thing.bottom_left.x_value * zoom_factor,
                                          center_y + space_thing.bottom_left.y_value * zoom_factor),
                                         (center_x + space_thing.bottom.x_value * zoom_factor,
                                          center_y + space_thing.bottom.y_value * zoom_factor),
                                         (center_x + space_thing.bottom_right.x_value * zoom_factor,
                                          center_y + space_thing.bottom_right.y_value * zoom_factor)))
                elif space_thing.name == "Portal":
                    pygame.draw.polygon(background, (255, 255, 255),
                                        ((pos_x_on_screen + space_thing.corner0.x_value * zoom_factor,
                                          pos_y_on_screen + space_thing.corner0.y_value * zoom_factor),
                                         (pos_x_on_screen + space_thing.corner1.x_value * zoom_factor,
                                          pos_y_on_screen + space_thing.corner1.y_value * zoom_factor),
                                         (pos_x_on_screen + space_thing.corner2.x_value * zoom_factor,
                                          pos_y_on_screen + space_thing.corner2.y_value * zoom_factor),
                                         (pos_x_on_screen + space_thing.corner3.x_value * zoom_factor,
                                          pos_y_on_screen + space_thing.corner3.y_value * zoom_factor)))
            if draw_vectors:
                background = space_thing.draw_speed_vector(background, pos_x_on_screen, pos_y_on_screen,
                                                           zoom_factor)
                background = space_thing.draw_acceleration_vector(background, pos_x_on_screen, pos_y_on_screen,
                                                                  zoom_factor)
            if space_thing.show_health_bar:
                space_thing.health_bar.draw_bar(background, zoom_factor, pos_x_on_screen, pos_y_on_screen, space_thing.radius)
        else:
            if space_thing.name != "Hope":
                space.space_objects.remove(space_thing)
                print("\033[2J")

    if temp_space_object is not None:
        relative_distance_to_hope_ship = (temp_space_object.position - hope_ship.position) * zoom_factor
        pos_x_on_screen = int(center_x + relative_distance_to_hope_ship.x_value)
        pos_y_on_screen = int(center_y + relative_distance_to_hope_ship.y_value)
        pygame.draw.circle(background,
                           (255, 255, 255),
                           (pos_x_on_screen, pos_y_on_screen),
                           int(temp_space_object.radius * zoom_factor),
                           int(2 * zoom_factor))


def draw_particles(background, center_x, center_y, hope_ship, screen_width, space, zoom_factor):
    for p in space.particles:
        visible = True
        for space_thing in space.space_objects:
            if not (space_thing.name == "Hope" or (
                    p.position - space_thing.position).get_length() > space_thing.radius) and not space_thing.crashed:
                visible = False
                if p.vanishable:
                    space.particles.remove(p)
                break
        if visible:
            pos_x_on_screen = int(center_x + (
                    p.position.x_value - hope_ship.position.x_value) * zoom_factor - p.size * zoom_factor / 2)
            pos_y_on_screen = int(center_y + (
                    p.position.y_value - hope_ship.position.y_value) * zoom_factor - p.size * zoom_factor / 2)
            if p.is_on_screen(screen_width, screen_width, pos_x_on_screen, pos_y_on_screen):
                pygame.draw.rect(background, p.colour,
                                 (pos_x_on_screen,
                                  pos_y_on_screen,
                                  p.size * zoom_factor,
                                  p.size * zoom_factor))


def manage_framerate(delta_frame, fps, framerate_stability_value, space):
    if fps == 120:
        if delta_frame > 1 / 122:
            fps = 60
            space.tickrate = 1 / fps
        framerate_stability_value = 0
    if fps == 60:
        if delta_frame > 1 / 61:
            fps = 30
            space.tickrate = 1 / fps
            framerate_stability_value = 0
        elif delta_frame < 1 / 122:
            if framerate_stability_value > 1:
                fps = 120
                space.tickrate = 1 / fps
                framerate_stability_value = 0
            else:
                framerate_stability_value += space.tickrate
        else:
            framerate_stability_value = 0
    if fps == 30:
        if delta_frame > 1 / 30.5:
            fps = 15
            space.tickrate = 1 / fps
            framerate_stability_value = 0
        elif delta_frame < 1 / 61:
            if framerate_stability_value > 1:
                fps = 60
                space.tickrate = 1 / fps
                framerate_stability_value = 0
            else:
                framerate_stability_value += space.tickrate
        else:
            framerate_stability_value = 0
    if fps == 15:
        if delta_frame > 1 / 15:
            fps = 10
            space.tickrate = 1 / fps
            framerate_stability_value = 0
        elif delta_frame < 1 / 30.5:
            if framerate_stability_value > 1:
                fps = 30
                space.tickrate = 1 / fps
                framerate_stability_value = 0
            else:
                framerate_stability_value += space.tickrate
        else:
            framerate_stability_value = 0
    if fps == 10:
        if delta_frame < 1 / 15:
            if framerate_stability_value > 1:
                fps = 15
                space.tickrate = 1 / fps
                framerate_stability_value = 0
            else:
                framerate_stability_value += space.tickrate
        else:
            framerate_stability_value = 0
    return fps, framerate_stability_value


if __name__ == '__main__':
    main()
