import pygame
import scripts.tools as tools
from data.language import russian, english


def world_map_scene(screen: pygame.Surface, virtual_surface: pygame.Surface, switch_scene, settings: dict) -> None:
    world_map = tools.load_image('WorldMap/map_world_with_path.png')

    scroll_x = 0
    scroll_y = 0
    scroll_x_speed = 0
    scroll_y_speed = 0

    zoom = 1.5  # увеличение будет от 2 до 5

    background = tools.load_image('background.png')
    background = pygame.transform.scale(background, virtual_surface.get_size())

    dragging = False
    start_pos = (0, 0)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                switch_scene(None)
            elif event.type == pygame.MOUSEWHEEL:
                zoom += event.y * 0.5
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                dragging = True
                start_pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                dragging = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    switch_scene('menu_scene')
                if event.key == pygame.K_LEFT:
                    scroll_x_speed -= 10
                if event.key == pygame.K_RIGHT:
                    scroll_x_speed += 10
                if event.key == pygame.K_DOWN:
                    scroll_y_speed += 10
                if event.key == pygame.K_UP:
                    scroll_y_speed -= 10
            elif event.type == pygame.KEYUP:  # заканчиваем движение
                if event.key == pygame.K_LEFT:
                    scroll_x_speed += 10
                if event.key == pygame.K_RIGHT:
                    scroll_x_speed -= 10
                if event.key == pygame.K_DOWN:
                    scroll_y_speed -= 10
                if event.key == pygame.K_UP:
                    scroll_y_speed += 10
        scroll_x += scroll_x_speed * zoom
        scroll_y += scroll_y_speed * zoom
        if dragging:
            # Обновляем смещение при перемещении мышью
            current_pos = pygame.mouse.get_pos()
            scroll_x += start_pos[0] - current_pos[0]
            scroll_y += start_pos[1] - current_pos[1]
            start_pos = current_pos

        # Ограничиваем смещение, чтобы не выходить за пределы карты
        max_scroll_x = (world_map.get_width() * zoom - virtual_surface.get_width()) // 2
        max_scroll_y = (world_map.get_height() * zoom - virtual_surface.get_height()) // 2

        scroll_x = max(-max_scroll_x, min(max_scroll_x, scroll_x))
        scroll_y = max(-max_scroll_y, min(max_scroll_y, scroll_y))

        virtual_surface.fill((0, 0, 0))

        zoom = max(2, min(zoom, 3.5))

        # Рассчитываем новый размер карты с учетом масштаба
        scaled_width = int(world_map.get_width() * zoom)
        scaled_height = int(world_map.get_height() * zoom)

        # Масштабируем карту
        scaled_map = pygame.transform.scale(world_map, (scaled_width, scaled_height))

        virtual_surface.blit(background, (0, 0))
        virtual_surface.blit(scaled_map,
                             (virtual_surface.get_width() // 2 - scaled_map.get_width() // 2 - scroll_x,
                              virtual_surface.get_height() // 2 - scaled_map.get_height() // 2 - scroll_y))

        scaled_surface = pygame.transform.scale(virtual_surface, screen.get_size())
        screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()
