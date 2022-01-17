import pygame
import time
import random


class Main:
    snake_squares = list()

    def __init__(self, width, height):
        pygame.init()
        bg = (87, 138, 52)

        self.screen = pygame.display.set_mode((width, height))

        pygame.display.set_caption('Snake Game')

        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Score:', True, (255, 255, 255), bg)

        textRect = text.get_rect()

        pygame.display.flip()

        self.screen.fill(bg)

        self.abandonWidth = width * 0.1
        self.abandonHeight = height * 0.1

        n_sq = 14
        self.widthSq, self.heightSq = (width - (self.abandonWidth * 2)) / n_sq, (
                height - (self.abandonHeight * 2)) / n_sq

        rect1 = pygame.Rect(self.abandonWidth, self.abandonHeight, self.widthSq, self.heightSq)
        rect2 = pygame.Rect(self.abandonWidth + self.widthSq, self.abandonHeight, self.widthSq, self.heightSq)

        rect1_color = (142, 204, 57)
        rect2_color = (167, 217, 72)

        pygame.draw.rect(self.screen, rect1_color, rect1)
        pygame.draw.rect(self.screen, rect2_color, rect2)

        self.snake_squares.append(rect1)
        self.snake_squares.append(rect2)

        for i in range(n_sq):
            for j in range(3, n_sq, 2):
                rect1 = pygame.Rect(rect2.right, rect2.top, self.widthSq, self.heightSq)
                rect2 = pygame.Rect(rect1.right, rect1.top, self.widthSq, self.heightSq)
                self.snake_squares.append(rect1)
                self.snake_squares.append(rect2)
                pygame.draw.rect(self.screen, rect1_color, rect1)
                pygame.draw.rect(self.screen, rect2_color, rect2)
            if i >= (n_sq - 1):
                break
            rect1 = pygame.Rect(self.abandonWidth, rect2.bottom, self.widthSq, self.heightSq)
            rect2 = pygame.Rect(self.abandonWidth + self.widthSq, rect2.bottom, self.widthSq, self.heightSq)
            self.snake_squares.append(rect1)
            self.snake_squares.append(rect2)
            rect1_color, rect2_color = rect2_color, rect1_color
            pygame.draw.rect(self.screen, rect1_color, rect1)
            pygame.draw.rect(self.screen, rect2_color, rect2)

        print(self.snake_squares)

        while True:
            time.sleep(0.07)
            self.screen.blit(text, textRect)
            self.generate_fruit('resources/apple.png')

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
            pygame.display.update()

    def generate_fruit(self, fruit):
        fruit = pygame.image.load(fruit.path)
        fruit_rect = fruit.get_rect()
        square = random.choice(self.snake_squares)
        fruit_rect.left = square.left
        fruit_rect.bottom = square.bottom + self.abandonHeight + self.heightSq
        fruit = pygame.transform.scale(fruit, (self.widthSq, self.heightSq))
        self.screen.blit(fruit, fruit_rect)
        return square


if __name__ == '__main__':
    main = Main(800, 600)
