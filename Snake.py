import time


class Snake:
    def __init__(self, sq_width, sq_height):
        self.is_alive = True
        self.segments = list()
        self.sq_width = sq_width
        self.sq_height = sq_height

    def move(self, direction, field_sq, fruit_rect, fruit):
        speed = self.sq_width
        for segment in self.segments:
            if segment.x <= field_sq[0].left - (self.sq_width * 3) or segment.x >= field_sq[-1].left + (
                    self.sq_width * 0.9) or \
                    segment.y <= field_sq[0].top - self.sq_width or segment.y >= field_sq[-1].bottom:
                self.is_alive = False
            elif segment.x == self.segments[0].x and segment.y == self.segments[0].y and segment.name != 'head':
                self.is_alive = False

        if self.is_alive:
            change_x = 0
            change_y = 0
            head = self.segments[0]
            if head.x == fruit_rect.x and head.y == fruit_rect.y:
                fruit.is_alive = False
                self.segments.append(Segment(self.segments[-1].x, self.segments[-1].y, 'tail'))
                self.segments[-2].name = 'body'
            if direction == 'RIGHT':
                change_x = speed
                change_y = 0
            elif direction == 'UP':
                change_y = speed
                change_x = 0
            elif direction == 'LEFT':
                change_x = -speed
                change_y = 0
            elif direction == 'DOWN':
                change_y = -speed
                change_x = 0
            self.segments.insert(0, Segment(head.x + change_x, head.y - change_y, 'head'))
            self.segments[1].name = 'body'
            del self.segments[-1]
            self.segments[-1].name = 'tail'


class Segment:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
