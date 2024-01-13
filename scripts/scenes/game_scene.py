import pygame
import scripts.tools as tools
from scripts.entity.BaseHero import BaseHero

from data.language import russian, english
from scripts.camera import Camera
import global_variable
from scripts.entity.Goblin import Goblin
from scripts.scenes.dead_screen import DeadScreen


def game_scene(screen: pygame.Surface, virtual_surface: pygame.Surface, switch_scene, settings: dict) -> None:
    # создаём новую виртуальную поверхность размерами 48 на 24 игровых тайла
    virtual_surface = pygame.Surface((384, 192))

    # ограничение по фпс
    clock = pygame.time.Clock()
    fps = 60

    # подготовка для работы со спрайтами и тайлами
    tools.tile_init()
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    enemy = pygame.sprite.Group()
    dead_scene = None
    is_activity = True
    # загрузка 1 лвл, создание игрока и базового перемещения камеры
    level_x, level_y, orientation_tile = tools.generate_level(tools.load_level(global_variable.current_level),
                                                              (all_sprites, tiles_group))
    player = BaseHero(24, 1, settings, all_sprites, player_group)
    with open('data/levels/' + global_variable.current_level + '_enemy', 'r') as file:
        for coords in file.readline().split(','):
            coords = coords.replace('(', '').replace(')', '')
            coords = coords.split(';')
            Goblin(int(coords[0]), int(coords[1]), all_sprites, enemy)
    camera = Camera((level_x, level_y), virtual_surface.get_size(), orientation_tile)
    heal_bar = pygame.Surface((100, 15))
    heal_bar.fill((35, 64, 128))  # цвет, который сделаем прозрачным
    heal_bar.set_colorkey((35, 64, 128))
    running = True
    while running:
        heal_bar.fill((35, 64, 128))  # цвет, который сделаем прозрачным
        heal_bar.set_colorkey((35, 64, 128))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                switch_scene(None)
            if is_activity:
                player.handler_event(event)

        if not player.is_alive():
            dead_scene = DeadScreen(virtual_surface)
            is_activity = False

        virtual_surface.fill((0, 0, 0))

        # изменяем ракурс камеры
        camera.update(player)
        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)

        tiles_group.update(player)
        enemy.update(player, tiles_group)
        if is_activity:
            player_group.update(tiles_group)
        if player.rect.top >= virtual_surface.get_height():
            player.get_damage(9999999999999999999999999999999)
        # отображаем все тайлы и игрока
        tiles_group.draw(virtual_surface)
        for en in enemy:
            if en.rect.top >= level_y * 8:
                en.kill()
            else:
                en.draw(virtual_surface)
        player_group.draw(virtual_surface)

        pygame.draw.rect(heal_bar, (193, 0, 0),
                         pygame.Rect(0, 0, int((heal_bar.get_width()) * (player.hp / player.max_hp)),
                                     heal_bar.get_height() - 8), 0, 20)
        pygame.draw.rect(heal_bar, (220, 220, 220),
                         pygame.Rect(0, 0, heal_bar.get_width(), heal_bar.get_height() - 8), 1,
                         20)

        virtual_surface.blit(heal_bar, (5, 5))
        if dead_scene is not None:
            dead_scene.draw()
        # трансформируем виртуальную поверхность и растягиваем её на весь экран
        scaled_surface = pygame.transform.scale(virtual_surface, screen.get_size())
        screen.blit(scaled_surface, (0, 0))

        pygame.display.flip()
        clock.tick(fps)
