import pygame
import scripts.tools as tools


def menu_scene(screen: pygame.Surface, virtual_surface: pygame.Surface, switch_scene) -> None:
    background = tools.load_image('background.png')
    background = pygame.transform.scale(background, virtual_surface.get_size())
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                switch_scene(None)

        # отрисовываем всё на сцене
        virtual_surface.fill((0, 0, 0))
        virtual_surface.blit(background, (0, 0))
        # отрисовываем сцену на экране
        scaled_surface = pygame.transform.scale(virtual_surface, screen.get_size())
        screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()
