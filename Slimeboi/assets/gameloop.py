import config

class Gameloop:
    def __init__(self, dataobject, tickrate, time):
        self.time_prev = time
        self.accumulator = 0
        self.tickrate = tickrate
        self.ticktime = 1 / self.tickrate
        self.dilation = 1

        # Object to maintain
        # Must have a tick() function
        self.dataobject = dataobject

    def tick(self, time):
        delta_time = time - self.time_prev
        self.accumulator += delta_time
        self.time_prev = time

        # Game Ticks
        loops = self.accumulator // (self.ticktime * self.dilation)
        loops_left = loops
        self.accumulator -= loops * (self.ticktime * self.dilation)
        while loops_left > 0:
            self.dataobject.tick()
            loops_left -= 1

        return loops