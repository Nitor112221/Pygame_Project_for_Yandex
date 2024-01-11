import pygame

from scripts.entity.Entity import Entity
import scripts.tools as tools


def line_rect_intersection(x1, y1, x2, y2, rect):
    return True


class Enemy(Entity):
    def __init__(self, pos_x: int, pos_y: int, animation: dict, image: pygame.Surface, *group):
        super().__init__(image, pos_x, pos_y, animation, *group)
        self.sight_distance = 8 * 10
        self.irascibilis = False

    def update(self, player, tile_group):
        super().update(tile_group)
        if ((abs(self.rect.centerx - player.rect.x) ** 2) + (
                abs(self.rect.centery - player.rect.y) ** 2)) ** 0.5 <= self.sight_distance:
            for sprite in tile_group:
                if not line_rect_intersection(*self.rect.center, *player.rect.center, sprite.rect):
                    self.irascibilis = False
                    return
            self.irascibilis = True
        else:
            self.irascibilis = False

    def draw(self, surface: pygame.Surface):
        if self.irascibilis:
            pygame.draw.rect(surface, 'red', self.rect, 1)
        surface.blit(self.image, self.rect)
