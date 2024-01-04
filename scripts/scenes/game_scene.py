import pygame
import scripts.tools as tools

from data.language import russian, english
from scripts.camera import Camera


def game_scene(screen: pygame.Surface, virtual_surface: pygame.Surface, switch_scene, settings: dict) -> None:
    virtual_surface = pygame.Surface((384, 192))

    clock = pygame.time.Clock()
    fps = 60

    tools.tile_init()
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()

    level_x, level_y, orientation_tile = tools.generate_level(tools.load_level('level_1'), (all_sprites, tiles_group))
    player = tools.Player(0, 0, all_sprites, player_group)
    player_speed_x = 0
    player_speed_y = 0
    camera = Camera((level_x, level_y), virtual_surface.get_size(), orientation_tile)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                switch_scene(None)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    player_speed_y = 4
                if event.key == pygame.K_UP:
                    player_speed_y = -4
                if event.key == pygame.K_LEFT:
                    player_speed_x = -4
                if event.key == pygame.K_RIGHT:
                    player_speed_x = 4
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    player_speed_y = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player_speed_x = 0

                # Обновление позиции игрока в зависимости от скорости
        player.rect.x += player_speed_x
        player.rect.y += player_speed_y

        virtual_surface.fill((0, 0, 0))

        # изменяем ракурс камеры
        camera.update(player)
        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)

        tiles_group.draw(virtual_surface)
        player_group.draw(virtual_surface)
        scaled_surface = pygame.transform.scale(virtual_surface, screen.get_size())
        screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()
        clock.tick(fps)
