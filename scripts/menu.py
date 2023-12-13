import pygame


def menu_scene(screen, virtual_surface, switch_scene):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                switch_scene(None)

        # отрисовываем всё на сцене
        virtual_surface.fill((0, 0, 255))

        # отрисовываем сцену на экране
        scaled_surface = pygame.transform.scale(virtual_surface, screen.get_size())
        screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()
