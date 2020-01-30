import random


class Block:
    def __init__(self,
                 position,
                 size,
                 chunk,
                 colour=(123, 123, 123),
                 name="Test Block",
                 description="This is a test description",
                 solid=True,
                 hardness=1):
        self.position = position
        self.chunk = chunk
        self.colour = colour
        self.alternate_colour = None
        self.name = name
        self.description = description
        # if random.randint(0, 1) == 0:
        #     solid = False
        self.solid = solid
        self.hardness = hardness
        self.size = size

    def dismantle(self, mining_device, tickrate):
        if self.hardness > 0:
            self.hardness -= mining_device.mining_speed * tickrate
        else:
            self.solid = False


class AirBlock(Block):
    def __init__(self, position):
        super().__init__(position, solid=False)
