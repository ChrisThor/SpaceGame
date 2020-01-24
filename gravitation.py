import math
import space_object
import particle
import vector


class Space:
    def __init__(self, fps):
        self.running = True
        self.space_objects = []
        self.gravitational_constant = 6.6743e-11 * 2
        self.tickrate = 1 / fps
        self.particles = []

    def calculate_acceleration_from_force(self, space_object1: space_object.SpaceObject,
                                          space_object2: space_object.SpaceObject):
        """
        Calculates gravitational force between two objects in space. It's a kind of magic
        :param space_object1:
        :param space_object2:
        :return:
        """
        distance = vector.Vector(space_object2.position.x_value - space_object1.position.x_value,
                                 space_object2.position.y_value - space_object1.position.y_value)
        if distance.get_length() < space_object1.radius + space_object2.radius or \
                distance.get_length() < space_object1.radius + space_object2.radius:
            if space_object1.mass < space_object2.mass and not space_object1.static:
                space_object2 += space_object1
            else:
                space_object1 += space_object2
        elif not space_object1.static:
            try:
                direction_x = (1 / math.sqrt(distance.x_value**2 + distance.y_value**2)) * distance.x_value
            except ZeroDivisionError:
                direction_x = 0
            try:
                direction_y = (1 / math.sqrt(distance.x_value**2 + distance.y_value**2)) * distance.y_value
            except ZeroDivisionError:
                direction_y = 0
            if distance.get_length() == 0:
                force = 0
            else:
                force = self.gravitational_constant * space_object2.mass / distance.get_length() ** 2
            force_vector = vector.Vector(force * direction_x, force * direction_y)
            return force_vector
        return vector.Vector()

    def apply_forces(self, hope_ship, debug_mode, particle_tick):
        """
        Calculates repeatedly acceleration and moves all space objects respectively. The for-loop's length is dependent
        on the duration of the simulation and the tickrate, which is currently defined in the constructor of SPACE
        """
        self.calculate_gravitational_acceleration(particle_tick)
        self.apply_space_ship_thrust(hope_ship)
        self.apply_acceleration(debug_mode)
        self.move_particles()

    def apply_space_ship_thrust(self, hope_ship):
        hope_ship.acceleration += hope_ship.thrust

    def apply_acceleration(self, debug_mode):
        """
        Applies the calculated acceleration vectors to their space objects
        :return:
        """
        for space_thing in self.space_objects:
            space_thing.do_tick(self.tickrate)
            if debug_mode:
                space_thing.print_stats()

    def calculate_gravitational_acceleration(self, particle_tick):
        """
        This function calculates their gravitational force on every space object.

        It also produces particles for every space object to avoid having to go through another loop
        :return:
        """
        for space_thing in range(len(self.space_objects)):
            space_thing1: space_object.SpaceObject = self.space_objects[space_thing]
            space_thing1.reset_acceleration()

            if not space_thing1.crashed and particle_tick >= 1 / 3:
                self.particles.append(particle.Particle(space_thing1.particle_colour,
                                                        space_thing1.position,
                                                        vector.Vector(),
                                                        space_thing1.particle_lifetime,
                                                        space_thing1,
                                                        2,
                                                        False))

            for other_space_thing in range(len(self.space_objects)):
                if space_thing != other_space_thing:
                    space_thing2: space_object.SpaceObject = self.space_objects[other_space_thing]
                    if not space_thing1.crashed and not space_thing2.crashed:
                        space_thing1.acceleration += self.calculate_acceleration_from_force(space_thing1, space_thing2)
                        if space_thing1.crashed:
                            space_thing1.reset_acceleration()
            if space_thing1.output_portal is not None:
                if (space_thing1.output_portal.position - space_thing1.position).get_length() > space_thing1.radius:
                    space_thing1.output_portal = None

    def move_particles(self):
        for particel in self.particles:
            particel.move(self.tickrate)
