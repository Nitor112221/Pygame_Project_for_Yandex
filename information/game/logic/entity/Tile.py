import pygame
import logic.tools as tools


class Tile(pygame.sprite.Sprite):
    tile_images = {
        'platform': tools.load_image('platform/platform.png'),
        'platform_horizontal': tools.load_image('platform/platform_horizontal.png'),
        'platform_vertical': tools.load_image('platform/platform_vertical.png'),
        'disappearing_block1': tools.load_image('disappearing_block/disappearing_block_1.png', -2),
        'disappearing_block2': tools.load_image('disappearing_block/disappearing_block_2.png', -2),
        'disappearing_block3': tools.load_image('disappearing_block/disappearing_block_3.png', -2),
        'spike': tools.load_image('spike/spike_classic.png'),
        'dirt': tools.load_image('dirt/dirt.png'),
        'dirtu': tools.load_image('dirt/dirt_up.png'),
        'dirth': tools.load_image('dirt/dirt_down.png'),
        'dirtl': tools.load_image('dirt/dirt_left.png'),
        'dirtr': tools.load_image('dirt/dirt_right.png'),
        'dirtq': tools.load_image('dirt/dirt_up_left.png'),
        'dirtw': tools.load_image('dirt/dirt_down_left.png'),
        'dirte': tools.load_image('dirt/dirt_up_right.png'),
        'dirtt': tools.load_image('dirt/dirt_down_right.png')
    }

    def __init__(self, tile_type, pos_x, pos_y, *groups, is_touchable=True):
        self.tile_type = tile_type
        self.is_touchable = is_touchable
        super().__init__(*groups)
        if tile_type is not None:
            self.image = self.tile_images[tile_type].copy()
            self.rect = self.image.get_rect().move(
                8 * pos_x, 8 * pos_y)
        else:  # создание ориентировочного тайла, нужного для ориентации камеры
            self.image = self.tile_images['platform'].copy()
            self.rect = pygame.Rect(0, 0, 0, 0).move(
                8 * pos_x, 8 * pos_y)

    def update(self, player):
        # метод, который добавляет разным блокам уникальное поведение (пока что есть только исчезающие блоки)
        pass
