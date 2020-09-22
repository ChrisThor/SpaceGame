import world
import vector
import pygame
import health_bar


class SpaceObject:
    def __init__(self, name, mass, radius, x_speed, y_speed, x_position, y_position, particle_colour, particle_lifetime,
                 lifetime="INF", hp=3, static=False, show_health_bar=True):
        self.radius = radius                                    # measurement unit: meter
        self.name = name
        self.mass = mass                                        # measurement unit: kg
        self.speed = vector.Vector(x_speed, y_speed)            # measurement unit: meter/second
        self.position = vector.Vector(x_position, y_position)   # measurement unit: meter
        self.acceleration = vector.Vector()                     # measurement unit: meter/second²
        self.crashed = False
        self.relative_distance_to_hope_ship = vector.Vector()   # This is required to calculate this object's position
        self.particle_colour = particle_colour                  # on screen
        self.particle_lifetime = particle_lifetime
        self.lifetime = lifetime    # If given, unit must be seconds, not frames!
        self.health_bar = health_bar.HealthBar(hp, self.radius * 2)
        self.static = static        # If static, this space object will not be influenced by gravitational forces
        self.output_portal = None
        self.show_health_bar = show_health_bar
        self.surface = None

    def __add__(self, other):
        if other.name == "Bullet":
            self.get_damage(other)
        if not self.crashed:
            if not self.static:
                self.speed = (self.speed * self.mass + other.speed * other.mass) / (self.mass + other.mass)
                self.position = (self.position * self.mass + other.position * other.mass) / (self.mass + other.mass)
            self.mass += other.mass
            if other.name != "Bullet":
                self.health_bar += other.health_bar
        other.speed *= 0
        other.reset_acceleration()
        other.crashed = True
        return self

    def get_damage(self, bullet):
        self.health_bar.reduce_hp(bullet.damage)
        if self.health_bar.hp <= 0:
            self.mass = 0
            self.speed = vector.Vector()
            self.reset_acceleration()
            self.crashed = True

    def reset_acceleration(self):
        self.acceleration *= 0

    def generate_world(self, background, screen, resolution):
        width = int(self.radius * 2 / 2)
        self.surface = world.World(width, 32, background, screen, resolution)

    def print_stats(self):
        print(f"{self.name} ({self.mass} kg) \n"
              f"Lifetime: {self.lifetime} \n"
              f"X: {round(self.position.x_value, 2)}          \n"
              f"Y: {round(self.position.y_value, 2)}          \n"
              f"Speed: {round(self.speed.get_length(), 4)} m/s          \n"
              f"Speed X: {round(self.speed.x_value, 4)} m/s          \n"
              f"Speed Y: {round(self.speed.y_value, 4)} m/s          \n"
              f"Accel: {round(self.acceleration.get_length(), 4)} m/s²          \n"
              f"Accel X: {round(self.acceleration.x_value, 4)} m/s²          \n"
              f"Accel Y: {round(self.acceleration.y_value, 4)} m/s²          \n"
              f"{'-' * 25}")

    def accelerate(self, tickrate):
        self.speed += self.acceleration * tickrate

    def move(self, tickrate):
        self.position += self.speed * tickrate

    def do_tick(self, tickrate):
        self.accelerate(tickrate)
        self.move(tickrate)
        if self.lifetime != "INF":
            self.lifetime -= tickrate
            if self.lifetime <= 0:
                self.crashed = True

    def draw_speed_vector(self, background, pos_x_on_screen, pos_y_on_screen, zoom_factor):
        pygame.draw.line(background,
                         (255, 100, 100),
                         (pos_x_on_screen, pos_y_on_screen),
                         (pos_x_on_screen + self.speed.x_value * zoom_factor, pos_y_on_screen + self.speed.y_value * zoom_factor))
        return background

    def draw_acceleration_vector(self, background, pos_x_on_screen, pos_y_on_screen, zoom_factor):
        pygame.draw.line(background,
                         (0, 200, 200),
                         (pos_x_on_screen, pos_y_on_screen),
                         (pos_x_on_screen + self.acceleration.x_value * zoom_factor, pos_y_on_screen + self.acceleration.y_value * zoom_factor))
        return background

    def is_on_screen(self, screen_width, screen_height, pos_x_on_screen, pos_y_on_screen, radius):
        if -radius <= pos_x_on_screen <= screen_width + radius:
            if -radius <= pos_y_on_screen <= screen_height + radius:
                return True
        return False
