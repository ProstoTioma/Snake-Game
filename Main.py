import pygame
import time

class Main:
    def __init__(self, width, height):
        pygame.init()
        bg = (124, 193, 121)

        screen = pygame.display.set_mode((width, height))

        pygame.display.set_caption('Snake Game')

        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Score:', True, (255, 255, 255), bg)

        textRect = text.get_rect()

        pygame.display.flip()

        screen.fill(bg)

        gameRect = pygame.Rect(width * 0.07, height * 0.07, width * 0.87, height * 0.87)

        pygame.draw.rect(screen, (11, 140, 32), gameRect)

        while True:

            screen.blit(text, textRect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            a = 11
            pygame.display.update()


if __name__ == '__main__':
    main = Main(800, 600)
