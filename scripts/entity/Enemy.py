import pygame

from scripts.entity.Entity import Entity
import scripts.tools as tools


class Enemy(Entity):
    def __init__(self, pos_x: int, pos_y: int, animation: dict, image: pygame.Surface, *group):
        super().__init__(image, pos_x, pos_y, animation, *group)
