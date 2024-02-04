import pygame
import scripts.tools as tools
from scripts.entity.BaseHero import BaseHero

from scripts.camera import Camera
import global_variable
from scripts.entity.Goblin import Goblin
from scripts.scenes.dead_screen import DeadScreen
from scripts.scenes.pause_scene import PauseScene


def save_progress():
    # структура файла с тэгами:
    # (x;y;название уровня, который открывают;
    # доступен ли для запуска;уровни, которые станут доступными после прохождения этого),тоже самое и тд
    tags = []
    with open('data/Saves/tag_coords', 'r') as file:
        for coords in file.readline().split(','):
            coords = coords.replace('(', '').replace(')', '')
            coords = coords.split(';')
            tags.append(coords)
    level = int(global_variable.current_level[-1]) - 1
    change_lvl = [i for i in tags[level][4].split(',') if i]
    for i in change_lvl:
        tags[int(i)][3] = 'True'
    with open('data/Saves/tag_coords', 'w') as file:
        tag = []
        for coords in tags:
            coords = ';'.join(coords)
            coords = '(' + coords + ')'
            tag.append(coords)
        file.write(','.join(tag))


def game_scene(screen: pygame.Surface, virtual_surface: pygame.Surface, switch_scene, settings: dict) -> None:
    # неиспользованный аргумент virtual_surface (нажен для полиморфизма)
    pygame.mixer.music.stop()
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

    # полезные флаги
    dead_scene = None
    is_activity = True
    is_pause = False
    pause_scene = None

    # загрузка лвла, создание игрока и базового перемещения камеры
    level_x, level_y, orientation_tile, player_pos, goblins = tools.generate_level(
        tools.load_level(global_variable.current_level),
        (all_sprites, tiles_group))
    if player_pos is None:
        player_pos = (0, 0)
    player = BaseHero(player_pos[0], player_pos[1], settings, all_sprites, player_group)
    # размещение врагов по уровню
    for coords in goblins:
        Goblin(int(coords[0]), int(coords[1]), all_sprites, enemy)
    camera = Camera((level_x, level_y), virtual_surface.get_size(), orientation_tile)

    heal_bar = pygame.Surface((100, 15))
    heal_bar.fill((35, 64, 128))  # цвет, который сделаем прозрачным
    heal_bar.set_colorkey((35, 64, 128))

    # установка курсора мыши на свой
    cursor_img = pygame.transform.scale(tools.load_image('cursor.png'), (12, 12))
    cursor_group = pygame.sprite.Group()
    cursor = pygame.sprite.Sprite(cursor_group)
    cursor.image = cursor_img
    cursor.rect = cursor.image.get_rect()

    running = True
    while running:
        heal_bar.fill((35, 64, 128))  # цвет, который сделаем прозрачным
        heal_bar.set_colorkey((35, 64, 128))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                switch_scene(None)
            elif event.type == pygame.MOUSEMOTION:
                cursor.rect.topleft = tools.hover(event.pos, screen, virtual_surface)  # обнавляем положение курсора
            elif event.type == pygame.MOUSEBUTTONUP:
                if dead_scene is not None:  # получаем результаты и обрабатываем нажатия на экране смерти
                    result = dead_scene.update(tools.hover(pygame.mouse.get_pos(), screen, virtual_surface),
                                               switch_scene)
                    if result is not None:
                        running = False
                if pause_scene is not None:  # получаем и обрабатываем результат нажатия при октрытом меню
                    result = pause_scene.update(tools.hover(pygame.mouse.get_pos(), screen, virtual_surface),
                                                switch_scene)
                    if result == 'continue':
                        is_pause = False
                        pause_scene = None

                    if result == 'map':
                        global_variable.is_music_play = False
                        running = False

            # обработка паузы
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                is_pause = not is_pause
                if is_pause:
                    pause_scene = PauseScene(virtual_surface, settings)
                else:
                    pause_scene = None
            if is_activity and not is_pause:
                player.handler_event(event)

        # запуск смерти персонажа
        if not player.is_alive() and dead_scene is None:
            dead_scene = DeadScreen(virtual_surface, settings)
            is_activity = False

        virtual_surface.fill((0, 0, 0))

        # изменяем ракурс камеры
        camera.update(player)
        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)

        if not is_pause:  # если игра не на паузе, то обнавляем всё
            tiles_group.update(player)
            enemy.update(player, tiles_group)
            if is_activity:
                player_group.update(tiles_group, enemy)
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

        # отрисовка хилбара
        pygame.draw.rect(heal_bar, (193, 0, 0),
                         pygame.Rect(0, 0, int((heal_bar.get_width()) * (player.hp / player.max_hp)),
                                     heal_bar.get_height() - 8), 0, 20)
        pygame.draw.rect(heal_bar, (220, 220, 220),
                         pygame.Rect(0, 0, heal_bar.get_width(), heal_bar.get_height() - 8), 1,
                         20)

        virtual_surface.blit(heal_bar, (5, 5))
        if dead_scene is not None:
            dead_scene.draw()
        if pause_scene is not None and is_pause:
            pause_scene.draw()

        cursor_group.draw(virtual_surface)

        # если игрок вышел за границу уровня, то он его прошёл
        if player.rect.x >= virtual_surface.get_width():
            save_progress()
            global_variable.is_music_play = False
            running = False
            switch_scene('world_map')

        # трансформируем виртуальную поверхность и растягиваем её на весь экран
        scaled_surface = pygame.transform.scale(virtual_surface, screen.get_size())
        screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()
        clock.tick(fps)
