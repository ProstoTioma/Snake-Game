import fruits
import snake
import random
import pygame


class Game:
    def __init__(self, widthSq, heightSq, screen, field_squares, n_sq, width, height):
        self.widthSq = widthSq
        self.heightSq = heightSq
        self.n_sq = n_sq
        self.width = width
        self.height = height

        self.sn = snake.Snake(widthSq, heightSq)

        self.apple = fruits.Fruit('resources/apple.png', 1)
        self.banana = fruits.Fruit('resources/banane.png', 2)
        self.cherry = fruits.Fruit('resources/cherry.png', 3)
        self.grape = fruits.Fruit('resources/grape.png', 4)
        self.pineapple = fruits.Fruit('resources/pineapple.png', 5)
        self.strawberry = fruits.Fruit('resources/strawberry.png', 5)
        self.mushroom = fruits.Fruit('resources/mushroom.png', 0)

        self.fruits = [self.apple, self.banana, self.cherry, self.grape, self.pineapple, self.strawberry, self.mushroom]
        self.fruit = self.apple
        self.loaded_fruit = None
        self.fruit_rect = None

        self.gameOver = False
        self.score = '0'
        self.trophy_score = 0

        self.direction = 'RIGHT'

        self.screen = screen

        self.field_squares = field_squares

    def restart(self):
        print(self.sn.segments[0].x, self.sn.segments[0].y)
        if int(self.score) > int(self.trophy_score):
            self.trophy_score = self.score
        self.score = '       '
        self.sn.is_alive = True
        self.apple.is_alive = False
        self.gameOver = False
        self.fruit = self.apple
        self.generate_fruit(self.fruit)
        del self.sn.segments[:]
        self.create_snake_segments(3)
        print(self.sn.segments[0].x, self.sn.segments[0].y)
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
    def generate_fruit(self, fruit):
        fruit = pygame.image.load(fruit.path)
        fruit = pygame.transform.scale(fruit, (self.widthSq, self.heightSq))
        fruit_rect = fruit.get_rect()
        generated_in_snake = False
        square = random.choice(self.field_squares)
        while True:
            if generated_in_snake:
                square = random.choice(self.field_squares)
                generated_in_snake = False
            for segment in self.sn.segments:
                if segment.x == square.x and segment.y == square.y:
                    generated_in_snake = True
            if not generated_in_snake:
                break
        self.loaded_fruit = fruit
        self.fruit_rect = fruit_rect
        return square

    def create_snake_segments(self, n):
        self.sn.segments.append(snake.Segment(self.field_squares[len(self.field_squares) // 2 + self.n_sq // 2].x,
                                              self.field_squares[len(self.field_squares) // 2 + self.n_sq // 2].y,
                                              'head'))
        for i in range(1, n):
            self.sn.segments.append(
                snake.Segment(self.sn.segments[0].x - self.widthSq * i, self.sn.segments[0].y, 'body'))
