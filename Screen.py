import random
import time
import snake
import pygame

import fruits


class Screen:
    field_squares = list()
    n_sq = 14
    sn = snake.Snake(20)

    def __init__(self, width=800, height=600):
        self.bg = (87, 138, 52)
        self.width = width
        self.height = height
        self.apple = fruits.Fruit('resources/apple.png', 1)
        self.loaded_fruit = None
        self.apple_rect = None

        self.screen = pygame.display.set_mode((self.width, self.height))

        self.abandonWidth = self.width * 0.1
        self.abandonHeight = self.height * 0.1

        self.widthSq, self.heightSq = (self.width - (self.abandonWidth * 2)) / self.n_sq, (
                self.height - (self.abandonHeight * 2)) / self.n_sq

    def start(self):
        pygame.init()
        pygame.display.set_caption('Snake Game')
        self.screen.fill(self.bg)
        self.draw_field()

        self.sn.segments.append(snake.Segment(self.width / 2, self.height / 2))
        self.sn.segments.append(snake.Segment(self.sn.segments[0].x + self.widthSq, self.sn.segments[0].y))
        self.sn.segments.append(snake.Segment(self.sn.segments[0].x + self.widthSq * 2, self.sn.segments[0].y))

        direction = 'DOWN'
        while True:
            time.sleep(0.1)
            self.draw_field()
            self.draw_objects()
            self.sn.move(direction)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        direction = 'UP'
                    elif event.key == pygame.K_DOWN:
                        direction = 'DOWN'
                    elif event.key == pygame.K_LEFT:
                        direction = 'LEFT'
                    elif event.key == pygame.K_RIGHT:
                        direction = 'RIGHT'

            pygame.display.update()

    def draw_field(self):

        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Score:', True, (255, 255, 255), self.bg)

        textRect = text.get_rect()

        pygame.display.flip()

        rect1 = pygame.Rect(self.abandonWidth, self.abandonHeight, self.widthSq, self.heightSq)
        rect2 = pygame.Rect(self.abandonWidth + self.widthSq, self.abandonHeight, self.widthSq, self.heightSq)

        rect1_color = (142, 204, 57)
        rect2_color = (167, 217, 72)

        pygame.draw.rect(self.screen, rect1_color, rect1)
        pygame.draw.rect(self.screen, rect2_color, rect2)

        for i in range(self.n_sq):
            for j in range(3, self.n_sq, 2):
                rect1 = pygame.Rect(rect2.right, rect2.top, self.widthSq, self.heightSq)
                rect2 = pygame.Rect(rect1.right, rect1.top, self.widthSq, self.heightSq)
                self.field_squares.append(rect1)
                self.field_squares.append(rect2)
                pygame.draw.rect(self.screen, rect1_color, rect1)
                pygame.draw.rect(self.screen, rect2_color, rect2)
            if i >= (self.n_sq - 1):
                break
            rect1 = pygame.Rect(self.abandonWidth, rect2.bottom, self.widthSq, self.heightSq)
            rect2 = pygame.Rect(self.abandonWidth + self.widthSq, rect2.bottom, self.widthSq, self.heightSq)
            self.field_squares.append(rect1)
            self.field_squares.append(rect2)
            rect1_color, rect2_color = rect2_color, rect1_color
            pygame.draw.rect(self.screen, rect1_color, rect1)
            pygame.draw.rect(self.screen, rect2_color, rect2)
            self.field_squares.append(rect1)
            self.field_squares.append(rect2)
        self.screen.blit(text, textRect)

    def generate_fruit(self, fruit):
        fruit = pygame.image.load(fruit.path)
        fruit_rect = fruit.get_rect()
        square = random.choice(self.field_squares)
        fruit_rect.left = square.left
        fruit_rect.bottom = square.bottom + self.abandonHeight + self.heightSq
        fruit = pygame.transform.scale(fruit, (self.widthSq, self.heightSq))
        self.loaded_fruit = fruit
        self.apple_rect = fruit_rect
        return square

    def draw_objects(self):
        for segment in self.sn.segments:
            segment_rect = pygame.Rect(segment.x, segment.y, self.widthSq, self.heightSq)
            pygame.draw.rect(self.screen, (240, 120, 0), segment_rect)
        if not self.apple.is_alive:
            apple_sq = self.generate_fruit(self.apple)
            self.apple.is_alive = True
        self.screen.blit(self.loaded_fruit, self.apple_rect)


if __name__ == '__main__':
    main = Screen()
    main.start()
