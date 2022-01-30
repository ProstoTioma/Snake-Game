import random
import time

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

        pygame.mixer.init()
        self.main_theme = pygame.mixer.Sound('resources/main_theme.wav')
        self.death_sound = pygame.mixer.Sound('resources/death.wav')
        self.fruit_sound = pygame.mixer.Sound('resources/eat_fruit.wav')
        self.main_theme.set_volume(0.05)
        self.death_sound.set_volume(0.01)
        self.fruit_sound.set_volume(0.01)

    def start(self):
        self.draw_background()
        self.draw_field()
        self.game.create_snake_segments(3)
        self.game.fruit_rect = self.game.generate_object(self.game.fruit)

        pygame.mixer.Sound.play(self.main_theme, -1)

        while True:
            if not self.game.gameOver:

                self.draw_field()
                self.game.sn.move(self.game.direction, self.field_squares, self.game.fruit_rect, self.game.fruit)
                self.draw_objects()
                self.game.eat_object()
                if self.game.is_eaten_object:
                    duration_check = random.randint(0, self.game.object_duration + 1)
                    if duration_check == self.game.object_duration:
                        self.game.time_delay = 0.1
                        self.game.is_eaten_object = False

                if not self.game.sn.is_alive:
                    self.main_theme.stop()
                    self.death_sound.play()
                    self.game.game_over()
            else:
                self.main_theme.stop()
                self.death_sound.play()
                self.game.game_over()
            # Listen to events
            key_w = False
            key_a = False
            key_s = False
            key_d = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.main_theme.stop()
                        self.death_sound.stop()
                        self.fruit_sound.stop()
                        self.main_theme.play(-1)
                        self.game.restart()
                    key_w = True if event.key == (pygame.K_w or pygame.K_UP) else False
                    key_a = True if event.key == (pygame.K_a or pygame.K_LEFT) else False
                    key_s = True if event.key == (pygame.K_s or pygame.K_RIGHT) else False
                    key_d = True if event.key == (pygame.K_d or pygame.K_DOWN) else False
            if key_w and self.game.direction != 'DOWN':
                self.game.direction = 'UP'
            elif key_s and self.game.direction != 'UP':
                self.game.direction = 'DOWN'
            elif key_a and self.game.direction != 'RIGHT':
                self.game.direction = 'LEFT'
            elif key_d and self.game.direction != 'LEFT':
                self.game.direction = 'RIGHT'

            pygame.display.update()
            time.sleep(self.game.time_delay)

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
        direction = self.game.direction
        for i in range(len(self.game.sn.segments)):
            segment = self.game.sn.segments[i]
            previous_segment = self.game.sn.segments[i - 1] if i != 0 else segment
            next_segment = self.game.sn.segments[i + 1] if i != len(self.game.sn.segments) - 1 else None
            if segment.x < previous_segment.x:
                if segment.y == previous_segment.y:
                    direction = 'right'
                elif segment.y < previous_segment.y:
                    direction = 'down'
                else:
                    direction = 'up'
                if next_segment is not None and segment.x == next_segment.x:
                    segment.name = 'twist'
                    if segment.y > next_segment.y:
                        direction = 'up'
                    else:
                        direction = 'right'

            elif segment.x > previous_segment.x:
                if segment.y == previous_segment.y:
                    direction = 'left'
                elif segment.y < previous_segment.y:
                    direction = 'down'
                else:
                    direction = 'up'
                if next_segment is not None and segment.x == next_segment.x:
                    segment.name = 'twist'
                    if segment.y > next_segment.y:
                        direction = 'down'
                    else:
                        direction = 'left'

            else:
                if segment.name != 'head':
                    if segment.y < previous_segment.y:
                        direction = 'down'
                        if next_segment is not None and segment.y == next_segment.y:
                            segment.name = 'twist'
                            if segment.x > next_segment.x:
                                direction = 'left'
                            else:
                                direction = 'right'
                    else:
                        direction = 'up'
                        if next_segment is not None and segment.x > next_segment.x:
                            segment.name = 'twist'
                            direction = 'down'
                        elif next_segment is not None and segment.x < next_segment.x:
                            segment.name = 'twist'
                            direction = 'up'

            body = pygame.image.load(f'resources/rotated_{direction}_{segment.name}.png')
            segment_rect = body.get_rect()
            body = pygame.transform.scale(body, (self.widthSq, self.widthSq))
            segment_rect.top = segment.y
            segment_rect.left = segment.x
            if not (segment.x <= self.field_squares[0].left - (self.widthSq * 3) or segment.x >= self.field_squares[
                -1].left + (
                            self.widthSq * 0.9) or segment.y <= self.field_squares[0].top - self.widthSq or segment.y >=
                    self.field_squares[-1].bottom):
                self.screen.blit(body, segment_rect)

        # Objects
        if len(self.game.boxes) != 0:
            for box in self.game.boxes:
                self.screen.blit(box[0], box[1])

        if self.game.object is not None:
            time_object = self.game.time_object * 2 if self.game.object.score == 2 else self.game.time_object // 3
            if self.game.object.score != 1 and self.game.object.score != 2:
                time_object = self.game.time_object
        else:
            time_object = self.game.time_object
        object_spawn = random.randint(0, time_object + 1)
        if object_spawn == self.game.time_object:
            if self.game.object is not None:
                self.game.object = None

            if self.game.object is None:
                self.game.object = random.choice(self.game.objects)
                if self.game.object.score == 0:
                    if self.game.box_limit == self.game.box_count:
                        while self.game.object.score == 0:
                            self.game.object = random.choice(self.game.objects)
                    else:
                        self.game.box_count += 1
                    self.game.object_rect = self.game.generate_object(self.game.object)

                    self.game.boxes.append((self.game.loaded_object, self.game.object_rect))
                else:
                    self.game.object_rect = self.game.generate_object(self.game.object)

        if self.game.object is not None:
            if self.game.object.score == 0:
                self.screen.blit(self.game.boxes[-1][0], self.game.boxes[-1][1])
            else:
                self.screen.blit(self.game.loaded_object, self.game.object_rect)

        # Fruits
        if not self.game.fruit.is_alive:
            self.game.fruit.is_alive = True
            if self.game.score == '        ':
                self.game.score = 0
            else:
                self.fruit_sound.play()
                self.game.score = str(int(self.game.score) + self.game.fruit.score)

            self.game.fruit = random.choice(self.game.fruits)
            self.game.fruit_rect = self.game.generate_object(self.game.fruit)

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
