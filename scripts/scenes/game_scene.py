import pygame
import scripts.tools as tools
from scripts.entity.entity import Entity

from data.language import russian, english
from scripts.camera import Camera


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

    # загрузка 1 лвл, создание игрока и базового перемещения камеры
    level_x, level_y, orientation_tile = tools.generate_level(tools.load_level('level_1'), (all_sprites, tiles_group))
    player = Entity(tools.load_image('player/player.png'), 24, 1, all_sprites, player_group)
    camera = Camera((level_x, level_y), virtual_surface.get_size(), orientation_tile)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                switch_scene(None)
            # обработка движений с неотпусканием клавиш
            elif event.type == pygame.KEYDOWN:  # начинаем движение
                if event.key == pygame.K_DOWN:
                    player.y_speed += 4
                if event.key == pygame.K_UP:
                    player.y_speed += -4
                if event.key == pygame.K_LEFT:
                    player.x_speed += -4
                if event.key == pygame.K_RIGHT:
                    player.x_speed += 4
            elif event.type == pygame.KEYUP:  # заканчиваем движение
                if event.key == pygame.K_DOWN:
                    player.y_speed -= 4
                if event.key == pygame.K_UP:
                    player.y_speed += 4
                if event.key == pygame.K_LEFT:
                    player.x_speed += 4
                if event.key == pygame.K_RIGHT:
                    player.x_speed -= 4

        virtual_surface.fill((0, 0, 0))

        # изменяем ракурс камеры
        camera.update(player)
        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)

        # отображаем все тайлы и игрока
        tiles_group.draw(virtual_surface)
        player_group.update(tiles_group)
        player_group.draw(virtual_surface)

        # трансформируем виртуальную поверхность и растягиваем её на весь экран
        scaled_surface = pygame.transform.scale(virtual_surface, screen.get_size())
        screen.blit(scaled_surface, (0, 0))

        pygame.display.flip()
        clock.tick(fps)
