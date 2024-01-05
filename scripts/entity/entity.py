import pygame


class Entity(pygame.sprite.Sprite):
    gravity = 0.1

    def __init__(self, image: pygame.Surface, pos_x, pos_y, *group):
        super().__init__(*group)
        self.image = image
        self.rect = self.image.get_rect().move(pos_x * 8, pos_y * 8)
        self.x_speed = 0
        self.y_speed = 0
        self.jump_speed = -4
        # Мертв ли игрок или нет
        self.is_dead = False
        # Стоит ли игрок на земле или нет
        self.is_grounded = False
        # Способность производить удары игрока
        self.is_shoot = True
        # Находится ли игрок в здоровом положении (если он не принял удар)
        self.is_stop = True

    def update(self, tile_group):
        self.y_speed += self.gravity
        self.rect.x += self.x_speed
        self.check_collision_x(tile_group)
        self.rect.y += self.y_speed
        self.check_collision_y(tile_group)

    def check_collision_x(self, tile_group):
        # Проверка столкновений по оси X
        collisions = pygame.sprite.spritecollide(self, tile_group, False)
        for tile in collisions:
            if self.x_speed > 0:
                self.rect.right = tile.rect.left
            elif self.x_speed < 0:
                self.rect.left = tile.rect.right

    def check_collision_y(self, tile_group):
        # Проверка столкновений по оси Y
        collisions = pygame.sprite.spritecollide(self, tile_group, False)
        for tile in collisions:
            if self.y_speed > 0:
                self.rect.bottom = tile.rect.top
                self.y_speed = 0
                self.is_grounded = True
            elif self.y_speed < 0:
                self.rect.top = tile.rect.bottom
                self.y_speed = 0
