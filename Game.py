import Object
import Snake
import random
import pygame


class Game:
    def __init__(self, widthSq, heightSq, screen, field_squares, n_sq, width, height):
        self.widthSq = widthSq
        self.heightSq = heightSq
        self.n_sq = n_sq
        self.width = width
        self.height = height

        self.sn = Snake.Snake(widthSq, heightSq)

        self.apple = Object.Object('resources/apple.png', 1)
        self.banana = Object.Object('resources/banana.png', 2)
        self.cherry = Object.Object('resources/cherry.png', 3)
        self.grape = Object.Object('resources/grape.png', 4)
        self.pineapple = Object.Object('resources/pineapple.png', 5)
        self.strawberry = Object.Object('resources/strawberry.png', 5)

        self.fruits = [self.apple, self.banana, self.cherry, self.grape, self.pineapple, self.strawberry]
        self.fruit = self.apple
        self.loaded_fruit = None
        self.fruit_rect = None

        self.turtle = Object.Object('resources/turtle.png', 1)
        self.bunny = Object.Object('resources/bunny.png', 2)
        self.box = Object.Object('resources/box.png', 0)
        self.mushroom = Object.Object('resources/mushroom.png', -1)

        self.objects = [self.turtle, self.bunny, self.mushroom, self.box]
        self.boxes = []
        self.object = None
        self.is_eaten_object = False
        self.loaded_object = None
        self.object_rect = None
        self.box_count = 0
        self.box_limit = 5

        self.time_object = 200
        self.object_duration = 100

        self.gameOver = False
        self.score = '0'
        self.trophy_score = 0

        self.direction = 'RIGHT'

        self.screen = screen

        self.field_squares = field_squares

        self.time_delay = 0.1

    def restart(self):
        if int(self.score) > int(self.trophy_score):
            self.trophy_score = self.score
        self.score = '        '
        self.sn.is_alive = True
        self.apple.is_alive = False
        self.object = None
        self.gameOver = False
        self.fruit = self.apple
        self.generate_object(self.fruit)
        del self.boxes[:]
        self.time_delay = 0.1
        del self.sn.segments[:]
        self.create_snake_segments(3)
        self.direction = 'RIGHT'

    def game_over(self):
        self.sn.is_alive = False
        self.gameOver = True
        font = pygame.font.Font('freesansbold.ttf', round(self.heightSq))
        text = font.render('Game over! Press R to restart', True, (0, 0, 0), (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (self.width // 2, self.height // 2)

        self.screen.blit(text, textRect)

    # Generate a fruit on the random square
    def generate_object(self, game_object):
        is_fruit = False
        if game_object in self.fruits:
            game_object = pygame.image.load(game_object.path)
            game_object = pygame.transform.scale(game_object, (self.widthSq, self.heightSq))
            object_rect = game_object.get_rect()
            self.loaded_fruit = game_object
            self.fruit_rect = object_rect
            is_fruit = True
        else:
            game_object = pygame.image.load(game_object.path)
            game_object = pygame.transform.scale(game_object, (self.widthSq, self.heightSq))
            object_rect = game_object.get_rect()
            self.loaded_object = game_object
            self.object_rect = object_rect
        return self.object_collision(is_fruit)

    def create_snake_segments(self, n):
        self.sn.segments.append(Snake.Segment(self.field_squares[len(self.field_squares) // 2 + self.n_sq // 2].x,
                                              self.field_squares[len(self.field_squares) // 2 + self.n_sq // 2].y,
                                              'head'))
        for i in range(1, n):
            if i == n - 1:
                name = 'tail'
            else:
                name = 'body'
            self.sn.segments.append(
                Snake.Segment(self.sn.segments[0].x - self.widthSq * i, self.sn.segments[0].y, name))

    # Check if object spawns not in the snake or fruit and return correct square
    def object_collision(self, is_fruit):
        collision = False
        square = random.choice(self.field_squares)

        while True:
            if collision:
                square = random.choice(self.field_squares)
                collision = False
            for segment in self.sn.segments:
                if segment.x == square.x and segment.y == square.y:
                    collision = True

            if not is_fruit:
                if square.x == self.fruit_rect.x and square.y == self.fruit_rect.y:
                    collision = True

                for box in self.boxes:
                    if square.x == box.x and square.y == box.y:
                        collision = True

            if not collision:
                break

        return square

    def eat_object(self):
        for box in self.boxes:
            if self.sn.segments[0].x == box[1].x and self.sn.segments[0].y == box[1].y:
                self.sn.is_alive = False
        if self.object is not None:
            if self.sn.segments[0].x == self.object_rect.x and self.sn.segments[0].y == self.object_rect.y:
                if self.object.score == 1:
                    self.time_delay = 0.3
                    self.is_eaten_object = True
                    self.object = None

                elif self.object.score == 2:
                    self.time_delay = 0.05
                    self.is_eaten_object = True
                    self.object = None

                elif self.object.score == 0:
                    self.sn.is_alive = False

                elif self.object.score == -1:
                    self.score = int(self.score) - 5
                    self.object = None
