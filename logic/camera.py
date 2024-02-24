class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self, size: tuple[int, int], screen_size: tuple[int, int], orientation_tile):
        self.dx = 0
        self.dy = 0
        self.width = size[0]
        self.height = size[1]
        self.screen_size = screen_size

        # ориентировочный тайл, что бы правильно расчитать сдвиг и ограничения
        self.orientation_tile = orientation_tile

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        # находим центр персонажа
        target_x = target.rect.x + target.rect.w // 2
        target_y = target.rect.y + target.rect.h // 2

        # Рассчитываем сдвиг
        self.dx = -(target_x - self.screen_size[0] // 2)
        self.dy = -(target_y - self.screen_size[1] // 2)

        # ограничения камеры по границам уровня
        if self.orientation_tile.rect.x <= -self.width * 8 + self.screen_size[0] - 8 and \
                target_x >= self.screen_size[0] // 2:
            self.dx = 0  # справа

        if self.orientation_tile.rect.bottom <= -self.height * 8 + self.screen_size[1] - 8 and \
                target_y >= self.screen_size[1] // 2:
            self.dy = 0  # снизу

        if self.orientation_tile.rect.right >= 0 and \
                target_x <= self.screen_size[0] // 2:
            self.dx = 0  # слева

        if self.orientation_tile.rect.top >= 0 and \
                target_y <= self.screen_size[1] // 2:
            self.dy = 0  # сверху
