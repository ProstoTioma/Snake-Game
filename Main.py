import pygame
import time
import random


class Main:
    def __init__(self, width, height):
        pygame.init()
        bg = (87, 138, 52)

        screen = pygame.display.set_mode((width, height))

        pygame.display.set_caption('Snake Game')

        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Score:', True, (255, 255, 255), bg)

        textRect = text.get_rect()

        pygame.display.flip()

        screen.fill(bg)

        abandonWidth = width * 0.1
        abandonHeight = height * 0.1

        n_sq = 14
        widthSq, heightSq = (width - (abandonWidth * 2)) / n_sq, (height - (abandonHeight * 2)) / n_sq

        rect1 = pygame.Rect(abandonWidth, abandonHeight, widthSq, heightSq)
        rect2 = pygame.Rect(abandonWidth + widthSq, abandonHeight, widthSq, heightSq)

        rect1_color = (142, 204, 57)
        rect2_color = (167, 217, 72)

        pygame.draw.rect(screen, rect1_color, rect1)
        pygame.draw.rect(screen, rect2_color, rect2)

        snake_squares = list()
        snake_squares.append(rect1)
        snake_squares.append(rect2)

        for i in range(n_sq):
            for j in range(3, n_sq, 2):
                rect1 = pygame.Rect(rect2.right, rect2.top, widthSq, heightSq)
                rect2 = pygame.Rect(rect1.right, rect1.top, widthSq, heightSq)
                snake_squares.append(rect1)
                snake_squares.append(rect2)
                pygame.draw.rect(screen, rect1_color, rect1)
                pygame.draw.rect(screen, rect2_color, rect2)
            if i >= (n_sq - 1):
                break
            rect1 = pygame.Rect(abandonWidth, rect2.bottom, widthSq, heightSq)
            rect2 = pygame.Rect(abandonWidth + widthSq, rect2.bottom, widthSq, heightSq)
            snake_squares.append(rect1)
            snake_squares.append(rect2)
            rect1_color, rect2_color = rect2_color, rect1_color
            pygame.draw.rect(screen, rect1_color, rect1)
            pygame.draw.rect(screen, rect2_color, rect2)

        print(snake_squares)

        apple = pygame.image.load('resources/apple.png')
        apple_rect = apple.get_rect()
        apple_rect.left = random.choice(snake_squares).left
        apple_rect.bottom = random.choice(snake_squares).bottom + abandonHeight + heightSq
        apple = pygame.transform.scale(apple, (widthSq, heightSq))

        while True:
            time.sleep(0.07)
            screen.blit(apple, apple_rect)
            screen.blit(text, textRect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
            pygame.display.update()


if __name__ == '__main__':
    main = Main(800, 600)
