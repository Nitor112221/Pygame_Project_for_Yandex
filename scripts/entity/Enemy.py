import pygame

from scripts.entity.Entity import Entity
import scripts.tools as tools


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

    def update(self, player, tile_group):
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

    def draw(self, surface: pygame.Surface):
        if self.irascibilis:
            pygame.draw.rect(surface, 'red', self.rect, 1)
        surface.blit(self.image, self.rect)
