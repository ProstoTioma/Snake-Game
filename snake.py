import time


class Snake:
    def __init__(self, sq_width, sq_height):
        self.is_alive = True
        self.segments = list()
        self.sq_width = sq_width
        self.sq_height = sq_height

    def move(self, direction, field_sq, apple_rect, apple):
        speed = self.sq_width
        for segment in self.segments:
            if segment.x <= field_sq[0].left - (self.sq_width * 3) or segment.x >= field_sq[-1].left + (
                    self.sq_width * 0.9) or \
                    segment.y <= field_sq[0].top - self.sq_width or segment.y >= field_sq[-1].bottom:
                self.is_alive = False
            elif segment.x == self.segments[0].x and segment.y == self.segments[0].y and segment.name != 'head':
                self.is_alive = False

        if self.is_alive:
            head = self.segments[0]
            if round(head.x / 10) * 10 == round(apple_rect.x / 10) * 10 and round(head.y / 10) * 10 == round(
                    apple_rect.y / 10) * 10:
                apple.is_alive = False
                self.segments.append(Segment(self.segments[-1].x, self.segments[-1].y, 'body'))
            if direction == 'RIGHT':
                self.segments.insert(0, Segment(head.x + speed, head.y, 'head'))
                self.segments[1].name = 'body'
                del self.segments[-1]
            elif direction == 'UP':
                self.segments.insert(0, Segment(head.x, head.y - speed, 'head'))
                self.segments[1].name = 'body'
                del self.segments[-1]
            elif direction == 'LEFT':
                self.segments.insert(0, Segment(head.x - speed, head.y, 'head'))
                self.segments[1].name = 'body'
                del self.segments[-1]
            elif direction == 'DOWN':
                self.segments.insert(0, Segment(head.x, head.y + speed, 'head'))
                self.segments[1].name = 'body'
                del self.segments[-1]
        time.sleep(0.1)


class Segment:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
