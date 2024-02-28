import time

from logic import tools
from logic.entity.Tile import Tile


class DisappearingTile(Tile):
    def __init__(self, tile_type, pos_x, pos_y, *groups, is_touchable=True):
        super().__init__(tile_type, pos_x, pos_y, *groups, is_touchable=is_touchable)
        self.disappearing_time = None
        self.original_image = self.tile_images[tile_type].copy()  # Исходное изображение блока
        if '1' in tile_type:
            self.dotted_line = tools.load_image('disappearing_block/dotted_line_1.png')
        elif '2' in tile_type:
            self.dotted_line = tools.load_image('disappearing_block/dotted_line_2.png')
        elif '3' in tile_type:
            self.dotted_line = tools.load_image('disappearing_block/dotted_line_3.png')

    def update(self, player):
        if player.rect.move(0, 2).colliderect(self.rect) and not self.disappearing_time:
            # если игрок наступил на блок, и таймер ещё не идёт запускаем таймер
            self.disappearing_time = time.time() + 0.6
        if self.disappearing_time is not None and time.time() >= self.disappearing_time:
            # проверяем на то вышло ли время исчезновения
            self.image = self.dotted_line.copy()
            self.is_touchable = False
        if self.disappearing_time is not None and time.time() >= self.disappearing_time + 3:
            # Восстанавливаем изображение блока
            self.image = self.original_image.copy()
            self.is_touchable = True
            self.disappearing_time = None
