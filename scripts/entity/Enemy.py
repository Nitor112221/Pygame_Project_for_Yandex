import pygame

from scripts.entity.Entity import Entity
import scripts.tools as tools
from scripts.entity.weapon import Weapon


def intersection(ax1: int, ay1: int, ax2: int, ay2: int, bx1: int, by1: int, bx2: int, by2: int):
    v1 = (bx2 - bx1) * (ay1 - by1) - (by2 - by1) * (ax1 - bx1)
    v2 = (bx2 - bx1) * (ay2 - by1) - (by2 - by1) * (ax2 - bx1)
    v3 = (ax2 - ax1) * (by1 - ay1) - (ay2 - ay1) * (bx1 - ax1)
    v4 = (ax2 - ax1) * (by2 - ay1) - (ay2 - ay1) * (bx2 - ax1)
    return (v1 * v2 < 0) and (v3 * v4 < 0)


class Enemy(Entity):
    def __init__(self, pos_x: int, pos_y: int, animation: dict, image: pygame.Surface, *group):
        super().__init__(image, pos_x, pos_y, animation, *group)
        self.sight_distance = 8 * 15
        self.irascibilis = False
        self.heal_bar = pygame.Surface((self.rect.width - 8, 4))
        self.heal_bar.fill((35, 64, 128))  # цвет, который сделаем прозрачным
        self.heal_bar.set_colorkey((35, 64, 128))
        self.jump_speed = -3.5
        self.jump_cooldown = 1000
        self.jump_time = None

    def update(self, player, tile_group):
        if self.weapon is not None and not self.is_dead:
            self.weapon.update()
            self.weapon.collide(player)
        if self.irascibilis:
            if self.rect.x + 12 <= player.rect.right and self.rect.right - 12 >= player.rect.x:
                self.x_speed = 0
                if not self.attacking:
                    self.attacking = True
                    self.frame_index = 0
                    self.attack_time = pygame.time.get_ticks()
                    self.weapon = Weapon(self, 'hummer')
                    self.speed = 0.5
                else:
                    self.speed = 1.5
            elif player.rect.right < self.rect.x + 12:
                self.x_speed = -self.speed
            elif self.rect.right + 12 < player.rect.x:
                self.x_speed = self.speed / 3
            else:
                self.x_speed = 0
            if self.rect.bottom > player.rect.bottom and self.jump_time is None:
                self.jump()
                self.jump_time = pygame.time.get_ticks()
        else:
            self.x_speed = 0

        super().update(tile_group)
        if ((abs(self.rect.centerx - player.rect.x) ** 2) + (
                abs(self.rect.centery - player.rect.y) ** 2)) ** 0.5 <= self.sight_distance:
            for sprite in tile_group:
                if intersection(self.rect.centerx, self.rect.centery, player.rect.centerx, player.rect.centery,
                                *sprite.rect.topleft, *sprite.rect.bottomleft) or \
                        intersection(self.rect.centerx, self.rect.centery, player.rect.centerx, player.rect.centery,
                                     *sprite.rect.topleft, *sprite.rect.topright) or \
                        intersection(self.rect.centerx, self.rect.centery, player.rect.centerx, player.rect.centery,
                                     *sprite.rect.bottomright, *sprite.rect.bottomleft) or \
                        intersection(self.rect.centerx, self.rect.centery, player.rect.centerx, player.rect.centery,
                                     *sprite.rect.topright, *sprite.rect.bottomright):
                    self.irascibilis = False
                    return
            self.irascibilis = True
        else:
            self.irascibilis = False

    def cooldowns(self):
        super().cooldowns()
        current_time = pygame.time.get_ticks()

        if self.jump_time is not None:
            if current_time - self.jump_time >= self.jump_cooldown:
                self.jump_time = None

    def draw(self, surface: pygame.Surface):
        # нужен для отладки и тестирования
        # if self.irascibilis:
        #     pygame.draw.rect(surface, 'red', self.rect, 1)
        self.heal_bar.fill((35, 64, 128))  # цвет, который сделаем прозрачным
        self.heal_bar.set_colorkey((35, 64, 128))
        pygame.draw.rect(self.heal_bar, (193, 0, 0),
                         pygame.Rect(0, 0, int((self.heal_bar.get_width()) * (self.hp / self.max_hp)),
                                     self.heal_bar.get_height()), 0, 20)
        surface.blit(self.heal_bar, (self.rect.x + 4, self.rect.y))
        surface.blit(self.image, self.rect)
