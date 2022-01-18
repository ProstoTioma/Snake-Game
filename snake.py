class Snake:
    def __init__(self, speed):
        self.is_alive = True
        self.segments = list()
        self.speed = speed

    def move(self, direction):
        if self.is_alive:
            for segment in self.segments:
                if direction == 'RIGHT':
                    segment.x += self.speed
                elif direction == 'LEFT':
                    segment.x -= self.speed
                elif direction == 'UP':
                    segment.y -= self.speed
                elif direction == 'DOWN':
                    segment.y += self.speed


class Segment:
    def __init__(self, x, y):
        self.x = x
        self.y = y
