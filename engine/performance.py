from time import time

class Performance:
    def __init__(self):
        self.start_time = time()
        self.end_time = time()
        self.total_time = 0.0
        self.frames = 0

    def start(self):
        self.start_time = time()

    def end(self):
        self.end_time = time()
        self.total_time += (self.end_time - self.start_time)
        self.frames += 1

    def get_fps(self):
        # Pygame does have a built-in FPS counter, but this is a custom implementation just in case
        # we want to use it in a different context or for a different purpose.
        if self.frames == 0:
            return 0.0
        return self.frames / self.total_time
    
    def average_time(self):
        if self.frames == 0:
            return 0.0
        return self.total_time / self.frames