import pygame
import scripts.tools as tools
from scripts.scenes.game_scene import game_scene
import global_variable
from data.language import russian, english


class Tag(pygame.sprite.Sprite):
    def __init__(self, pos_x: int, pos_y: int, level: str, *group, is_available=False):
        super().__init__(*group)
        self.image = tools.load_image('WorldMap/tag.png')
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.is_available = is_available
        self.scroll_y = 0
        self.level = level

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect.move(0, -self.scroll_y))

    def update(self, mouse_pos: tuple[int, int], screen: pygame.Surface, virtual_surface: pygame.Surface, zoom,
               scroll_x, scroll_y):
        rect_scaled = pygame.Rect(
            (self.rect.x - scroll_x // zoom - virtual_surface.get_width() // 12) * zoom,
            (self.rect.y - scroll_y // zoom - virtual_surface.get_height() // 2.91) * zoom,
            self.rect.w * zoom,
            self.rect.h * zoom)

        if rect_scaled.collidepoint(tools.hover(mouse_pos, screen, virtual_surface)):
            self.scroll_y = 20
        else:
            self.scroll_y = 0

    def click(self):
        if self.scroll_y != 0:
            global_variable.current_level = self.level
            return True


def world_map_scene(screen: pygame.Surface, virtual_surface: pygame.Surface, switch_scene, settings: dict) -> None:
    world_map = tools.load_image('WorldMap/map_world_with_path.png')

    all_sprite = pygame.sprite.Group()
    tag_group = pygame.sprite.Group()

    with open('data/Saves/tag_coords', 'r') as file:
        for coords in file.readline().split(','):
            coords = coords.replace('(', '').replace(')', '')
            coords = coords.split(';')
            Tag(int(coords[0]), int(coords[1]), str(coords[2]), all_sprite, tag_group)

    fps = 60
    clock = pygame.time.Clock()

    scroll_x = 0
    scroll_y = 0
    scroll_x_speed = 0
    scroll_y_speed = 0

    zoom = 2

    background = tools.load_image('background.png')
    background = pygame.transform.scale(background, virtual_surface.get_size())

    dragging = False
    start_pos = (0, 0)
    running = True
    while running:
        world_map_art = world_map.copy()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                switch_scene(None)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                dragging = True
                start_pos = pygame.mouse.get_pos()
                for sprite in tag_group:
                    if sprite.click():
                        running = False
                        switch_scene(game_scene)
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

        virtual_surface.fill((0, 0, 0))

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

        tag_group.update(pygame.mouse.get_pos(), screen, virtual_surface, zoom, scroll_x, scroll_y)
        for sprite in tag_group:
            sprite.draw(world_map_art)

        # Рассчитываем новый размер карты с учетом масштаба
        scaled_width = int(world_map.get_width() * zoom)
        scaled_height = int(world_map.get_height() * zoom)

        # Масштабируем карту
        scaled_map = pygame.transform.scale(world_map_art, (scaled_width, scaled_height))

        virtual_surface.blit(background, (0, 0))
        virtual_surface.blit(scaled_map,
                             (virtual_surface.get_width() // 2 - scaled_map.get_width() // 2 - scroll_x,
                              virtual_surface.get_height() // 2 - scaled_map.get_height() // 2 - scroll_y))

        scaled_surface = pygame.transform.scale(virtual_surface, screen.get_size())
        screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()
        clock.tick(fps)
