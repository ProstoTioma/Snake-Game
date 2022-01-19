class Snake:
    def __init__(self, speed, sq_width, sq_height):
        self.is_alive = True
        self.segments = list()
        self.speed = speed
        self.sq_width = sq_width
        self.sq_height = sq_height

    def move(self, direction):
        speed = self.speed * self.sq_width
        if self.is_alive:
            for i in range(0, len(self.segments)):
                segment = self.segments[i]
                previous_segment = self.segments[i - 1]

                if direction == 'RIGHT':
                    if i != len(self.segments) - 1:
                        next_segment = self.segments[i + 1]
                        if i == 0:
                            segment.x += speed
                        elif round(segment.x) == round(next_segment.x):
                            if round(segment.y) != round(previous_segment.y):
                                if round(segment.y) > round(previous_segment.y):
                                    segment.y -= speed
                                elif round(segment.y) < round(previous_segment.y):
                                    segment.y += speed

                            elif round(segment.y) == round(previous_segment.y):
                                segment.x += speed
                        elif round(segment.x) == round(previous_segment.x):
                            if round(segment.y) > round(previous_segment.y):
                                segment.y -= speed
                            elif round(segment.y) < round(previous_segment.y):
                                segment.y += speed
                        elif round(segment.x) != round(previous_segment.x):
                            segment.x += speed
                    else:
                        if round(segment.y) == round(previous_segment.y):
                            segment.x += speed
                        elif round(segment.y) > round(previous_segment.y):
                            segment.y -= speed
                        elif round(segment.y) < round(previous_segment.y):
                            segment.y += speed

                elif direction == 'LEFT':
                    segment.x -= speed

                elif direction == 'UP':
                    if i == 0:
                        segment.y -= speed
                    elif round(segment.x) != round(previous_segment.x):
                        segment.x += speed
                    elif round(segment.x) == round(previous_segment.x):
                        segment.y -= speed

                elif direction == 'DOWN':
                    if i == 0:
                        segment.y += speed
                    elif round(segment.x) != round(previous_segment.x):
                        segment.x += speed
                    elif round(segment.x) == round(previous_segment.x):
                        segment.y += speed


class Segment:
    def __init__(self, x, y):
        self.x = x
        self.y = y
