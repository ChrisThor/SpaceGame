import math


class Vector:
    def __init__(self, x=0.0, y=0.0):
        self.x_value = x
        self.y_value = y

    def __add__(self, other):
        return Vector(self.x_value + other.x_value, self.y_value + other.y_value)

    def __sub__(self, other):
        return Vector(self.x_value - other.x_value, self.y_value - other.y_value)

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __str__(self):
        return f"X: {self.x_value} Y: {self.y_value} Len: {self.get_length()}"

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector(self.x_value * other, self.y_value * other)
        else:
            return self.x_value * other.x_value + self.y_value * other.y_value

    def __imul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if not isinstance(other, int) and not isinstance(other, float):
            raise TypeError("Vectors can only be divided by numbers")
        else:
            return Vector(self.x_value / other, self.y_value / other)

    def get_length(self):
        return math.sqrt(self.x_value**2 + self.y_value**2)

    def norm(self):
        try:
            length = self.get_length()
            y_value = self.y_value / length
            x_value = self.x_value / length
        except ZeroDivisionError:
            return Vector()
        return Vector(x_value, y_value)
