import pygame
import time

import global_variable


class Entity(pygame.sprite.Sprite):
    # базовый класс для всех существ
    gravity = 0.135

    def __init__(self, image: pygame.Surface, pos_x, pos_y, *group):
        super().__init__(*group)
        self.image = image
        self.rect = self.image.get_rect().move(pos_x * 8, pos_y * 8)
        self.x_speed = 0
        self.y_speed = 0
        self.speed = 2
        self.jump_speed = -4
        # Мертво ли существо или нет
        self.is_dead = False

        # Стоит ли существо на земле или нет
        self.is_grounded = False

        # состояние существа (бежит, прыгает, падает и тд)
        self.status: str = 'classic'

        #  параметры для аткаи
        self.attacking = False
        self.attack_time = None
        self.attack_cooldown = 100

        # направление в которое смотрит существо (left или right)
        self.direction = 'right'

        # параметры анимации
        self.frame_index = 0
        self.animation_speed = 0.15

        self.hp = 100
        self.max_hp = 100

        # неуязвимость
        self.invulnerability = False
        self.time_invulnerability = None

        # объект класса Weapon, нужен для нанесения урона
        self.weapon = None

    def update(self, tile_group):
        self.cooldowns()
        # обработка передвижений
        self.y_speed += self.gravity
        self.y_speed = min(self.y_speed, 4)
        self.rect.x += self.x_speed
        self.check_collision_x(tile_group)
        self.rect.y += self.y_speed
        self.check_collision_y(tile_group)
        if self.x_speed > 0:
            self.direction = 'right'
        elif self.x_speed < 0:
            self.direction = 'left'
        # соприкосновение с шипами
        if not self.invulnerability:
            for sprite in tile_group:
                if sprite.tile_type == 'spike' and pygame.sprite.collide_mask(self, sprite):
                    self.get_damage(15)
                    break
        self.get_status()
        self.animate()

    def check_collision_x(self, tile_group):
        # Проверка столкновений по оси X
        collisions = pygame.sprite.spritecollide(self, [tile for tile in tile_group if tile.is_touchable], False)
        for tile in collisions:
            if self.x_speed > 0:
                self.rect.right = tile.rect.left
            elif self.x_speed < 0:
                self.rect.left = tile.rect.right

    def jump(self):
        if self.is_grounded:
            self.y_speed += self.jump_speed
            self.status = 'jump_' + self.direction
            self.is_grounded = False

    def check_collision_y(self, tile_group):
        # Проверка столкновений по оси Y
        collisions = pygame.sprite.spritecollide(self, [tile for tile in tile_group if tile.is_touchable], False)
        for tile in collisions:
            if self.y_speed > 0:
                self.rect.bottom = tile.rect.top
                self.y_speed = 0
                self.is_grounded = True
            elif self.y_speed < 0:
                self.rect.top = tile.rect.bottom
                self.y_speed = 0

    def get_status(self):
        # idle status
        if self.x_speed == 0 and self.y_speed == 0 and self.is_grounded and not self.attacking:
            self.status = 'idle_' + self.direction

        # walk status
        if self.x_speed != 0 and self.y_speed == 0 and self.is_grounded and not self.attacking:
            self.status = 'walk_' + self.direction

        # fall status
        if self.y_speed > 0.5:
            self.status = 'fall_' + self.direction

        if self.attacking:
            self.status = 'attack_' + self.direction

        if not self.is_alive():
            if self.is_dead is False:
                global_variable.statistics['Kills'] += 1
                self.frame_index = 0
            self.is_dead = True
            self.status = 'dead_' + self.direction
            self.animation_speed = 0.07
            self.weapon = None
            self.attacking = False

        if self.status is None:
            self.status = 'classic_' + self.direction

    def cooldowns(self):
        # обработка перезарядок
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.weapon = None

        if self.time_invulnerability is not None and time.time() >= self.time_invulnerability:
            self.time_invulnerability = None
            self.invulnerability = False

    def animate(self):
        # обработка анимаций
        try:
            animation = self.animation[self.status]
        except KeyError:
            animation = self.animation['classic_' + self.direction]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
            if not self.is_alive():
                self.kill()

        self.image = animation[int(self.frame_index)]

    def is_alive(self):
        if self.hp:
            return True
        else:
            return False

    def get_damage(self, amount):
        if not self.invulnerability:
            self.hp -= amount
            if self.hp <= 0:
                self.hp = 0
            self.invulnerability = True
            self.time_invulnerability = time.time() + 0.5
