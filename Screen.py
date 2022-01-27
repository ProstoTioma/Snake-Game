import random

import pygame

import Game


class Screen:
    field_squares = list()
    n_sq = 16

    def __init__(self, width=1000, height=1000):
        self.bg = (87, 138, 52)
        self.width = width
        self.height = height

        self.screen = pygame.display.set_mode((self.width, self.height))

        self.abandonWidth = self.width * 0.1
        self.abandonHeight = self.height * 0.1

        self.widthSq, self.heightSq = (self.width - (self.abandonWidth * 2)) // self.n_sq, (
                self.height - (self.abandonHeight * 2)) // self.n_sq

        self.game = Game.Game(self.widthSq, self.heightSq, self.screen, self.field_squares, self.n_sq, self.width,
                              self.height)

    def start(self):
        self.draw_background()
        self.draw_field()
        self.game.create_snake_segments(3)
        self.game.fruit_rect = self.game.generate_fruit(self.game.fruit)

        while True:
            if not self.game.gameOver:
                self.draw_field()
                self.game.sn.move(self.game.direction, self.field_squares, self.game.fruit_rect, self.game.fruit)
                self.draw_objects()
                if not self.game.sn.is_alive:
                    self.game.game_over()
            else:
                self.game.game_over()
            # Listen to events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.game.restart()
                    if (event.key == pygame.K_UP or event.key == pygame.K_w) and self.game.direction != 'DOWN':
                        self.game.direction = 'UP'
                    elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and self.game.direction != 'UP':
                        self.game.direction = 'DOWN'
                    elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and self.game.direction != 'RIGHT':
                        self.game.direction = 'LEFT'
                    elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and self.game.direction != 'LEFT':
                        self.game.direction = 'RIGHT'

            pygame.display.update()

    # Draw squares and score
    def draw_field(self):
        del self.field_squares[:]
        font = pygame.font.Font('freesansbold.ttf', 32)
        score = font.render(f'{self.game.score}', True, (255, 255, 255), self.bg)
        trophy = font.render(f'{self.game.trophy_score}', True, (255, 255, 255), self.bg)

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

    # Draw snake and fruit
    def draw_objects(self):
        for segment in self.game.sn.segments:
            segment_rect = pygame.Rect(segment.x, segment.y, self.widthSq, self.heightSq)
            if not (segment.x <= self.field_squares[0].left - (self.widthSq * 3) or segment.x >= self.field_squares[
                -1].left + (
                            self.widthSq * 0.9) or segment.y <= self.field_squares[0].top - self.widthSq or segment.y >=
                    self.field_squares[-1].bottom):
                pygame.draw.rect(self.screen, (240, 120, 0), segment_rect)

        if not self.game.fruit.is_alive:
            self.game.fruit.is_alive = True
            if self.game.score == '       ':
                self.game.score = 0
            else:
                self.game.score = str(int(self.game.score) + self.game.fruit.score)
            self.game.fruit = random.choice(self.game.fruits)
            self.game.fruit_rect = self.game.generate_fruit(self.game.fruit)

        self.screen.blit(self.game.loaded_fruit, self.game.fruit_rect)

    # Draw background, score and trophy images
    def draw_background(self):
        pygame.init()
        pygame.display.set_caption('Snake Game')

        self.screen.fill(self.bg)
        self.draw_field()
        decorate_fruit = pygame.image.load(self.game.fruit.path)
        decorate_trophy = pygame.image.load('./resources/trophy.png')
        apple_rect = decorate_fruit.get_rect()
        trophy_rect = decorate_trophy.get_rect()
        decorate_fruit = pygame.transform.scale(decorate_fruit, (32, 32))
        decorate_trophy = pygame.transform.scale(decorate_trophy, (32, 32))
        apple_rect.center = (self.width // 10, self.abandonHeight)
        trophy_rect.center = (self.width // 10 + self.widthSq * 3, self.abandonHeight)
        self.screen.blit(decorate_fruit, apple_rect)
        self.screen.blit(decorate_trophy, trophy_rect)
