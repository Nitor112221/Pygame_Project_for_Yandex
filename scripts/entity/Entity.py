import pygame


class Entity(pygame.sprite.Sprite):
    gravity = 0.135

    def __init__(self, image: pygame.Surface, pos_x, pos_y, animation: dict, *group):
        super().__init__(*group)
        self.image = image
        self.animation = animation
        self.rect = self.image.get_rect().move(pos_x * 8, pos_y * 8)
        self.x_speed = 0
        self.y_speed = 0
        self.jump_speed = -4
        # Мертво ли существо или нет
        self.is_dead = False
        # Стоит ли игрок на земле или нет
        self.is_grounded = False
        # Способность производить удары игрока
        self.is_shoot = True
        # Находится ли игрок в здоровом положении (если он не принял удар)
        self.is_stop = True
        # состояние существа (бежит, прыгает, падает и тд)
        self.status: str = 'classic'
        #  параметры для аткаи
        self.attacking = False
        self.attack_time = None
        self.attack_cooldown = 100
        # направление в которое смотрит существо (left или right)
        self.direction = 'right'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.hp = 100
        self.max_hp = 100

    def update(self, tile_group):
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
        self.cooldowns()
        self.status = self.status.split('_')[0] + '_' + self.direction
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

        if self.status is None:
            self.status = 'classic_' + self.direction

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False

    def animate(self):
        try:
            animation = self.animation[self.status]
        except KeyError:
            animation = self.animation['classic_right']

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]

    def is_alive(self):
        if self.hp:
            return True
        else:
            return False

    def get_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
        return self.hp
