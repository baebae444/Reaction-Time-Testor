import pygame
from gui import ReactionTimeApp

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Reaction Time Tester")
    app = ReactionTimeApp(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        app.update()
        app.render()
        pygame.display.flip()

    pygame.quit()