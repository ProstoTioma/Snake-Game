import random
import time
import snake
import pygame

import fruits


class Screen:
    field_squares = list()
    n_sq = 16

    def __init__(self, width=1000, height=1000):
        self.bg = (87, 138, 52)
        self.width = width
        self.height = height
        self.apple = fruits.Fruit('resources/apple.png', 1)
        self.loaded_fruit = None
        self.apple_rect = None
        self.gameOver = False
        self.time_out = 0.5
        self.score = 'f'

        self.screen = pygame.display.set_mode((self.width, self.height))

        self.abandonWidth = self.width * 0.1
        self.abandonHeight = self.height * 0.1

        self.widthSq, self.heightSq = (self.width - (self.abandonWidth * 2)) // self.n_sq, (
                self.height - (self.abandonHeight * 2)) // self.n_sq

        self.sn = snake.Snake(self.widthSq, self.heightSq)

    def start(self):
        self.draw_background()

        self.sn.segments.append(snake.Segment(self.field_squares[len(self.field_squares) // 2 + self.n_sq // 2].x,
                                              self.field_squares[len(self.field_squares) // 2 + self.n_sq // 2].y,
                                              'head'))
        self.sn.segments.append(snake.Segment(self.sn.segments[0].x - self.widthSq, self.sn.segments[0].y, 'body'))
        self.sn.segments.append(snake.Segment(self.sn.segments[0].x - self.widthSq * 2, self.sn.segments[0].y, 'body'))
        self.sn.segments.append(snake.Segment(self.sn.segments[0].x - self.widthSq * 3, self.sn.segments[0].y, 'body'))

        direction = 'RIGHT'
        while True:
            if not self.gameOver:
                self.draw_field()
                self.draw_objects()
                self.sn.move(direction, self.field_squares, self.apple_rect, self.apple)
                if not self.sn.is_alive:
                    self.game_over()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        break
                    if event.type == pygame.KEYDOWN:
                        if (event.key == pygame.K_UP or event.key == pygame.K_w) and direction != 'DOWN':
                            direction = 'UP'
                        elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction != 'UP':
                            direction = 'DOWN'
                        elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction != 'RIGHT':
                            direction = 'LEFT'
                        elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direction != 'LEFT':
                            direction = 'RIGHT'
            else:
                self.game_over()

            pygame.display.update()

    def game_over(self):
        self.sn.is_alive = False
        self.gameOver = True
        font = pygame.font.Font('freesansbold.ttf', 64)
        text = font.render('GAME OVER!', True, (0, 0, 0), (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (self.width // 2, self.height // 2)

        self.screen.blit(text, textRect)

    def draw_field(self):

        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(f'{self.score}', True, (255, 255, 255), self.bg)

        textRect = text.get_rect()
        textRect.center = (self.width // 10, self.abandonHeight // 2)

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
        while True:
            square = random.choice(self.field_squares)
            for segment in self.sn.segments:
                if segment.x == square.x and segment.y == square.y:
                    continue
            break
        fruit_rect.left = square.left - self.widthSq
        fruit_rect.bottom = square.bottom + self.abandonHeight + self.heightSq
        fruit = pygame.transform.scale(fruit, (self.widthSq, self.heightSq))
        self.loaded_fruit = fruit
        self.apple_rect = fruit_rect
        return square

    def draw_objects(self):
        for segment in self.sn.segments:
            segment_rect = pygame.Rect(segment.x, segment.y, self.widthSq, self.heightSq)
            if not (segment.x <= self.field_squares[0].left - (self.widthSq * 3) or segment.x >= self.field_squares[-1].left + (
                    self.widthSq * 0.9) or segment.y <= self.field_squares[0].top - self.widthSq or segment.y >= self.field_squares[-1].bottom):
                pygame.draw.rect(self.screen, (240, 120, 0), segment_rect)
        if not self.apple.is_alive:
            self.apple_rect = self.generate_fruit(self.apple)
            self.apple.is_alive = True
            if self.score == 'f':
                self.score = 0
            else:
                self.score += self.apple.score
        self.screen.blit(self.loaded_fruit, self.apple_rect)

    def draw_background(self):
        pygame.init()
        pygame.display.set_caption('Snake Game')

        self.screen.fill(self.bg)
        self.draw_field()
        decorate_fruit = pygame.image.load(self.apple.path)
        apple_rect = decorate_fruit.get_rect()
        decorate_fruit = pygame.transform.scale(decorate_fruit, (32, 32))
        apple_rect.center = (self.width // 10, self.abandonHeight)
        self.screen.blit(decorate_fruit, apple_rect)


if __name__ == '__main__':
    main = Screen()
    main.start()
