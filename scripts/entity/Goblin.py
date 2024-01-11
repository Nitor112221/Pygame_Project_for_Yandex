import pygame

from scripts.entity.Enemy import Enemy
import scripts.tools as tools


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
                     'classic_left': [tools.load_image('goblin/goblin_idle/idle1.png', reverse=True)],
                     'classic_right': [tools.load_image('goblin/goblin_idle/idle1.png')]
                     }
        super().__init__(pos_x, pos_y, animation, animation['idle_right'][0], *gruop)
