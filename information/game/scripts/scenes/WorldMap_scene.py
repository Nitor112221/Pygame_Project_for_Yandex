import pygame
import logic.tools as tools
from logic.scenes.game_scene import game_scene
import global_variable


class Tag(pygame.sprite.Sprite):
    # класс реализующий метку на карте игрового мира
    def __init__(self, pos_x: int, pos_y: int, level: str, unlock: bool, *group):
        super().__init__(*group)
        self.image_list = [tools.load_image('WorldMap/tag.png'), tools.load_image('WorldMap/tag_unlock.png')]
        self.image = self.image_list[1 if unlock else 0]
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.scroll_y = 0  # переменная отвечает за подпрыгивание значка при навидении
        self.level = level  # название уровня на который ведёт
        self.unlock = unlock  # можно ли зайти

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
        if self.scroll_y != 0 and self.unlock:
            global_variable.current_level = self.level
            return True


def world_map_scene(screen: pygame.Surface, virtual_surface: pygame.Surface, switch_scene, settings: dict) -> None:
    world_map = tools.load_image('WorldMap/map_world_with_path.png')

    all_sprite = pygame.sprite.Group()
    tag_group = pygame.sprite.Group()

    # создание всех тэгов на карте
    with open('data/Saves/tag_coords', 'r') as file:
        for coords in file.readline().split(','):
            coords = coords.replace('(', '').replace(')', '')
            coords = coords.split(';')
            Tag(int(coords[0]), int(coords[1]), str(coords[2]), True if coords[3] == 'True' else False,
                all_sprite, tag_group)

    # базовые параметры
    fps = 60
    clock = pygame.time.Clock()

    scroll_x = 0
    scroll_y = 0
    scroll_x_speed = 0
    scroll_y_speed = 0

    zoom = 2

    background = tools.load_image('background.png')
    background = pygame.transform.scale(background, virtual_surface.get_size())

    # установка курсора мыши на свой
    cursor_img = pygame.transform.scale(tools.load_image('cursor.png'), (60, 60))
    cursor_group = pygame.sprite.Group()
    cursor = pygame.sprite.Sprite(cursor_group)
    cursor.image = cursor_img
    cursor.rect = cursor.image.get_rect()
    focused = True

    dragging = False
    start_pos = (0, 0)

    running = True
    while running:
        world_map_art = world_map.copy()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                switch_scene(None)
            elif event.type == pygame.MOUSEMOTION:  # обновление положения курсора
                if pygame.mouse.get_focused():
                    focused = True
                    cursor.rect.topleft = tools.hover(event.pos, screen, virtual_surface)  # обнавляем положение курсора
                else:
                    focused = False
            # перемещение карты мышкой
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                dragging = True
                start_pos = pygame.mouse.get_pos()
                for sprite in tag_group:
                    if sprite.click():
                        running = False
                        switch_scene(game_scene)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                dragging = False
            # перемещение по карте с помощью клавиатуры
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

        if focused:
            cursor_group.draw(virtual_surface)

        scaled_surface = pygame.transform.scale(virtual_surface, screen.get_size())
        screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()
        global_variable.increase_volume(settings)
        clock.tick(fps)
