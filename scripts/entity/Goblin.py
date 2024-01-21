import pygame

from scripts.entity.Enemy import Enemy
import scripts.tools as tools
from scripts.entity.weapon import Weapon


class Goblin(Enemy):
    def __init__(self, pos_x, pos_y, *gruop):
        animation = {'walk_left': [tools.load_image('goblin/goblin_walk/walk1.png', reverse=True),
                                   tools.load_image('goblin/goblin_walk/walk2.png', reverse=True),
                                   tools.load_image('goblin/goblin_walk/walk3.png', reverse=True),
                                   tools.load_image('goblin/goblin_walk/walk4.png', reverse=True),
                                   tools.load_image('goblin/goblin_walk/walk5.png', reverse=True),
                                   tools.load_image('goblin/goblin_walk/walk6.png', reverse=True)],
                     'walk_right': [tools.load_image('goblin/goblin_walk/walk1.png'),
                                    tools.load_image('goblin/goblin_walk/walk2.png'),
                                    tools.load_image('goblin/goblin_walk/walk3.png'),
                                    tools.load_image('goblin/goblin_walk/walk4.png'),
                                    tools.load_image('goblin/goblin_walk/walk5.png'),
                                    tools.load_image('goblin/goblin_walk/walk6.png')],
                     'idle_left': [tools.load_image('goblin/goblin_idle/idle1.png', reverse=True),
                                   tools.load_image('goblin/goblin_idle/idle2.png', reverse=True),
                                   tools.load_image('goblin/goblin_idle/idle3.png', reverse=True),
                                   tools.load_image('goblin/goblin_idle/idle4.png', reverse=True),
                                   tools.load_image('goblin/goblin_idle/idle5.png', reverse=True),
                                   tools.load_image('goblin/goblin_idle/idle6.png', reverse=True),
                                   tools.load_image('goblin/goblin_idle/idle7.png', reverse=True),
                                   tools.load_image('goblin/goblin_idle/idle8.png', reverse=True)],
                     'idle_right': [tools.load_image('goblin/goblin_idle/idle1.png'),
                                    tools.load_image('goblin/goblin_idle/idle2.png'),
                                    tools.load_image('goblin/goblin_idle/idle3.png'),
                                    tools.load_image('goblin/goblin_idle/idle4.png'),
                                    tools.load_image('goblin/goblin_idle/idle5.png'),
                                    tools.load_image('goblin/goblin_idle/idle6.png'),
                                    tools.load_image('goblin/goblin_idle/idle7.png'),
                                    tools.load_image('goblin/goblin_idle/idle8.png')],
                     'attack_right': [tools.load_image('goblin/goblin_attack/attack1.png'),
                                      tools.load_image('goblin/goblin_attack/attack2.png'),
                                      tools.load_image('goblin/goblin_attack/attack3.png'),
                                      tools.load_image('goblin/goblin_attack/attack4.png'),
                                      tools.load_image('goblin/goblin_attack/attack5.png'),
                                      tools.load_image('goblin/goblin_attack/attack6.png'),
                                      tools.load_image('goblin/goblin_attack/attack7.png'),
                                      tools.load_image('goblin/goblin_attack/attack8.png'),
                                      tools.load_image('goblin/goblin_attack/attack9.png'),
                                      tools.load_image('goblin/goblin_attack/attack10.png'),
                                      tools.load_image('goblin/goblin_attack/attack11.png')],
                     'attack_left': [tools.load_image('goblin/goblin_attack/attack1.png', reverse=True),
                                     tools.load_image('goblin/goblin_attack/attack2.png', reverse=True),
                                     tools.load_image('goblin/goblin_attack/attack3.png', reverse=True),
                                     tools.load_image('goblin/goblin_attack/attack4.png', reverse=True),
                                     tools.load_image('goblin/goblin_attack/attack5.png', reverse=True),
                                     tools.load_image('goblin/goblin_attack/attack6.png', reverse=True),
                                     tools.load_image('goblin/goblin_attack/attack7.png', reverse=True),
                                     tools.load_image('goblin/goblin_attack/attack8.png', reverse=True),
                                     tools.load_image('goblin/goblin_attack/attack9.png', reverse=True),
                                     tools.load_image('goblin/goblin_attack/attack10.png', reverse=True),
                                     tools.load_image('goblin/goblin_attack/attack11.png', reverse=True)],
                     'classic_left': [tools.load_image('goblin/goblin_idle/idle1.png', reverse=True)],
                     'classic_right': [tools.load_image('goblin/goblin_idle/idle1.png')]
                     }
        super().__init__(pos_x, pos_y, animation, animation['idle_right'][0], *gruop)
        self.attack_cooldown = 1500
        self.max_hp = 50
        self.hp = 50

    def update(self, player, tile_group):
        if not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.weapon = Weapon(self, 'hummer')
        if self.attacking:
            self.animation_speed = 0.1
        else:
            self.animation_speed = 0.15
        super().update(player, tile_group)
