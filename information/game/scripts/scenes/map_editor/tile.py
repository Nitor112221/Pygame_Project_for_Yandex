import pygame
import scripts.tools as tools
from scripts.scenes.map_editor.convert_index import ConvertTile


# Главный класс, отвечающий за тайлы для рисования
class Tile:
    def __init__(self, screen):
        super().__init__()
        self.tile_group = pygame.sprite.Group()
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.convert_tile = ConvertTile()

        # Создание дополнительной поверхности
        self.selected_tile = False
        size_side = w, h = 12, 12
        self.additional_surface = pygame.Surface(size_side)
        self.additional_surface.set_colorkey((0, 0, 0))
        additional_color = pygame.Color((0, 214, 27))
        radius = w // 2
        # Рисование окружности на дополнительной поверхности
        pygame.draw.circle(self.additional_surface, additional_color, (w - radius, h - radius), radius)
        self.last_coor_x, self.last_coor_y = None, None

        self.color = pygame.Color(70, 70, 70, 255)
        self.bottom = 10
        self.left = 10
        self.cell_size = 40
        self.alpha = 128
        self.current_index = 0
        self.shift_x = 0
        self.last_left_coorx = 0
        self.last_right_coorx = self.screen_width

        self.tile_images = {
            '1.': tools.load_image('platform/platform.png'),
            '2.': tools.load_image('platform/platform_horizontal.png'),
            '3.': tools.load_image('platform/platform_vertical.png'),
            '4.-': tools.load_image('platform/platform.png'),
            '5.-': tools.load_image('platform/platform_horizontal.png'),
            '6.-': tools.load_image('platform/platform_vertical.png'),
            '7.': tools.load_image('disappearing_block/disappearing_block_1.png', -2),
            '8.': tools.load_image('disappearing_block/disappearing_block_2.png', -2),
            '9.': tools.load_image('disappearing_block/disappearing_block_3.png', -2),
            '10.': tools.load_image('spike/spike_classic.png')
        }

    # Метод отрисовки всех тайлов на экране
    def render(self, current_index_tile):
        # Необхлодимо очистить группу, чтобы внести спрайы с новыми координатами и отрисовать их
        self.tile_group = pygame.sprite.Group()
        current_index = 0
        for key, value in self.convert_tile.tile_images.items():
            tile = pygame.sprite.Sprite(self.tile_group)
            scaled_image = pygame.transform.scale(value[0], (self.cell_size, self.cell_size))

            if key[-1] == '-':
                scaled_image.set_alpha(self.alpha)

            tile.image = scaled_image
            tile.rect = tile.image.get_rect()
            tile.rect.x, tile.rect.y = current_index * self.cell_size + current_index * self.left + 10 + self.shift_x, \
                self.screen.get_height() - self.cell_size - self.bottom
            if current_index == 0:
                self.last_left_coorx = tile.rect.x
            current_index += 1
            self.last_right_coorx = tile.rect.x
            if current_index - 1 == current_index_tile:
                self.last_coor_x, self.last_coor_y = tile.rect.x, tile.rect.y

        self.tile_group.draw(self.screen)
        if self.selected_tile:
            if None not in (self.last_coor_x, self.last_coor_y):
                self.screen.blit(self.additional_surface, (self.last_coor_x - 5, self.last_coor_y - 5))

    # Метод для проверки нажатия на тайл
    def chek_clicked(self, coords):
        current_index_tile = 0
        for sprite in self.tile_group:
            if sprite.rect.collidepoint(coords):
                self.current_index = current_index_tile
                color = pygame.Color((255, 0, 0, 255))
                pygame.draw.rect(self.screen,
                                 color,
                                 (sprite.rect[0],
                                  sprite.rect[1],
                                  sprite.rect[2],
                                  sprite.rect[3]), 2)
                return sprite, current_index_tile
            current_index_tile += 1
        return None

    # Метод возврата тайла по текущему индексу для дальнейших действий
    def return_sprite(self, index):
        count = 0
        for sprite in self.tile_group:
            if index == count:
                return sprite
            count += 1
