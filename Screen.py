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
        self.trophy_score = 0
        self.direction = 'RIGHT'

        self.screen = pygame.display.set_mode((self.width, self.height))

        self.abandonWidth = self.width * 0.1
        self.abandonHeight = self.height * 0.1

        self.widthSq, self.heightSq = (self.width - (self.abandonWidth * 2)) // self.n_sq, (
                self.height - (self.abandonHeight * 2)) // self.n_sq

        self.sn = snake.Snake(self.widthSq, self.heightSq)

    def start(self):
        self.draw_background()
        self.create_snake_segments(3)

        while True:
            if not self.gameOver:
                self.draw_field()
                self.draw_objects()
                self.sn.move(self.direction, self.field_squares, self.apple_rect, self.apple)
                if not self.sn.is_alive:
                    self.game_over()
            else:
                self.game_over()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.restart()
                    if (event.key == pygame.K_UP or event.key == pygame.K_w) and self.direction != 'DOWN':
                        self.direction = 'UP'
                    elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and self.direction != 'UP':
                        self.direction = 'DOWN'
                    elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and self.direction != 'RIGHT':
                        self.direction = 'LEFT'
                    elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and self.direction != 'LEFT':
                        self.direction = 'RIGHT'

            pygame.display.update()

    def restart(self):
        if self.score > self.trophy_score:
            self.trophy_score = self.score
        self.score = 0
        self.sn.is_alive = True
        self.gameOver = False
        del self.sn.segments[:]
        self.create_snake_segments(3)
        self.direction = 'RIGHT'

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
        score = font.render(f'{self.score}', True, (255, 255, 255), self.bg)
        trophy = font.render(f'{self.trophy_score}', True, (255, 255, 255), self.bg)

        scoreRect = score.get_rect()
        scoreRect.center = (self.width // 10, self.abandonHeight // 2)

        trophyRect = trophy.get_rect()
        trophyRect.center = (self.width // 10 + self.widthSq * 3, self.abandonHeight // 2)

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
        self.screen.blit(score, scoreRect)
        self.screen.blit(trophy, trophyRect)

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
            if not (segment.x <= self.field_squares[0].left - (self.widthSq * 3) or segment.x >= self.field_squares[
                -1].left + (
                            self.widthSq * 0.9) or segment.y <= self.field_squares[0].top - self.widthSq or segment.y >=
                    self.field_squares[-1].bottom):
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
        decorate_trophy = pygame.image.load('./resources/trophy.png')
        apple_rect = decorate_fruit.get_rect()
        trophy_rect = decorate_trophy.get_rect()
        decorate_fruit = pygame.transform.scale(decorate_fruit, (32, 32))
        decorate_trophy = pygame.transform.scale(decorate_trophy, (32, 32))
        apple_rect.center = (self.width // 10, self.abandonHeight)
        trophy_rect.center = (self.width // 10 + self.widthSq * 3, self.abandonHeight)
        self.screen.blit(decorate_fruit, apple_rect)
        self.screen.blit(decorate_trophy, trophy_rect)

    def create_snake_segments(self, n):
        self.sn.segments.append(snake.Segment(self.field_squares[len(self.field_squares) // 2 + self.n_sq // 2].x,
                                              self.field_squares[len(self.field_squares) // 2 + self.n_sq // 2].y,
                                              'head'))
        for i in range(1, n):
            self.sn.segments.append(
                snake.Segment(self.sn.segments[0].x - self.widthSq * i, self.sn.segments[0].y, 'body'))


if __name__ == '__main__':
    main = Screen()
    main.start()
