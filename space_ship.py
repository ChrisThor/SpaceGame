import turnable_space_object
import bullet
import particle
import vector
import random


class SpaceShip(turnable_space_object.TurnableSpaceObject):
    def __init__(self, name, mass, radius, x_speed, y_speed, x_position, y_position, particle_colour,
                 particle_lifetime, hp=5, show_health_bar=True):
        super().__init__(name, mass, radius, x_speed, y_speed, x_position, y_position, particle_colour,
                         particle_lifetime, hp=hp, show_health_bar=show_health_bar)
        self.default_turn_value = 1.8
        self.thrust_strength = 4
        self.thrust = vector.Vector()
        self.tip = vector.Vector()
        self.bottom_left = vector.Vector()
        self.bottom_right = vector.Vector()
        self.bottom = vector.Vector()
        self.calculate_angle()

    def apply_thrust(self, direction, space, fps):
        if not self.crashed:
            self.thrust = self.angle_vector * (self.thrust_strength * direction)
            if direction != 0:
                for i in range(0, 60, fps):
                    red = random.randint(50, 255)
                    green = random.randint(0, 100)
                    # blue = random.randint(0, 255)
                    blue = 0
                    scatter = random.randint(-1000, 1000) / 100
                    speed_variation = random.randint(80, 120) / 100
                    lifetime = random.randint(1200, 1500) / 1000
                    space.particles.append(particle.Particle((red, green, blue),
                                                             self.position - self.speed * space.tickrate / 16,
                                                             self.speed + self.angle_vector *
                                                             (-8.5 * direction * speed_variation) * self.thrust_strength +
                                                             self.orthogonal_angle_vector * scatter,
                                                             lifetime,
                                                             self,
                                                             2))
        else:
            self.thrust *= 0

    def turn(self):
        self.tip = self.angle_vector * 4
        self.bottom = self.angle_vector * -1.33
        self.bottom_left = self.angle_vector * (-4) + self.orthogonal_angle_vector * 4
        self.bottom_right = self.angle_vector * (-4) + self.orthogonal_angle_vector * (-4)

    def turn_right(self, space, fps):
        if self.angle_speed < 6:
            self.accelerate_angle_speed(self.default_turn_value / fps)
            self.create_steering_particle(space, 1)

    def create_steering_particle(self, space, direction):
        if not self.crashed:
            brightness = random.randint(0, 100)
            space.particles.append(particle.Particle((130 - brightness, 130 - brightness, 255),
                                                     self.position + self.angle_vector * 3,
                                                     self.speed + self.orthogonal_angle_vector * 20 * direction,
                                                     1 / 6,
                                                     self,
                                                     1))

    def turn_left(self, space, fps):
        if -6 < self.angle_speed:
            self.accelerate_angle_speed(-self.default_turn_value / fps)
            self.create_steering_particle(space, -1)

    def print_stats(self):
        print(f"{self.name} ({self.mass} kg) \n"
              f"X: {round(self.position.x_value, 2)}          \n"
              f"Y: {round(self.position.y_value, 2)}          \n"
              f"Facing X: {round(self.angle_vector.x_value, 4)} Y: {round(self.angle_vector.y_value, 4)}         \n"
              f"Angle Speed: {round(self.angle_speed, 4)}         \n"
              f"Angle: {round(self.angle, 4)}         \n"
              f"Speed: {round(self.speed.get_length(), 4)} m/s          \n"
              f"Speed X: {round(self.speed.x_value, 4)} m/s          \n"
              f"Speed Y: {round(self.speed.y_value, 4)} m/s          \n"
              f"Accel: {round(self.acceleration.get_length(), 4)} m/s²          \n"
              f"Accel X: {round(self.acceleration.x_value, 4)} m/s²          \n"
              f"Accel Y: {round(self.acceleration.y_value, 4)} m/s²          \n"
              f"{'-' * 25}")

    def break_to_zero(self):
        speed = self.speed.get_length()
        if speed > 0.1:
            self.thrust = (self.speed.norm() * self.thrust_strength) * -1
        elif speed > 0.01:
            self.thrust = (self.speed.norm() * self.thrust_strength) * -0.1
        elif speed > 0.001:
            self.thrust = (self.speed.norm() * self.thrust_strength) * -0.01
        else:
            self.thrust = vector.Vector()
            self.speed = vector.Vector()

    def launch_bullet(self, space, fps):
        bullet_mass = 1
        bullet_radius = 2.7
        space.space_objects.append(bullet.Bullet(bullet_radius,
                                                 bullet_mass,
                                                 self.position + self.angle_vector * 15,
                                                 self.speed + self.angle_vector * 35,
                                                 1,
                                                 "Bullet",
                                                 (255, 50, 50),
                                                 3,
                                                 20))
        self.mass -= bullet_mass

    def accelerate_angle_speed(self, direction):
        self.angle_speed += direction
        if self.angle_speed < -6:
            self.angle_speed = -6
        elif self.angle_speed > 6:
            self.angle_speed = 6

    def move(self, tickrate):
        if not self.crashed:
            self.position += self.speed * tickrate
            self.angle += self.angle_speed * tickrate
            self.calculate_angle()
        else:
            self.speed *= 0

    def change_thrust_power(self, factor):
        if 4 <= self.thrust_strength * factor <= 128:
            self.thrust_strength *= factor
