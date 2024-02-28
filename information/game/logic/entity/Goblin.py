from logic.entity.Enemy import Enemy
import logic.tools as tools
import os


class Goblin(Enemy):
    # анимации
    animation = {'walk_left': [tools.load_image('goblin\\goblin_walk\\' + i, reverse=True) for i in
                               os.listdir('data/images/goblin/goblin_walk')],
                 'walk_right': [tools.load_image('goblin\\goblin_walk\\' + i) for i in
                                os.listdir('data/images/goblin/goblin_walk')],
                 'idle_left': [tools.load_image('goblin\\goblin_idle\\' + i, reverse=True) for i in
                               os.listdir('data/images/goblin/goblin_idle')],
                 'idle_right': [tools.load_image('goblin\\goblin_idle\\' + i) for i in
                                os.listdir('data/images/goblin/goblin_idle')],
                 'attack_right': [tools.load_image('goblin\\goblin_attack\\' + i, reverse=True) for i in
                                  os.listdir('data/images/goblin/goblin_attack')],
                 'attack_left': [tools.load_image('goblin\\goblin_attack\\' + i) for i in
                                 os.listdir('data/images/goblin/goblin_attack')],
                 'classic_left': [tools.load_image('goblin/goblin_idle/idle1.png', reverse=True)],
                 'classic_right': [tools.load_image('goblin/goblin_idle/idle1.png')],
                 'dead_right': [tools.load_image('goblin\\goblin_dead\\' + i, reverse=True) for i in
                                os.listdir('data/images/goblin/goblin_dead')],
                 'dead_left': [tools.load_image('goblin\\goblin_dead\\' + i) for i in
                               os.listdir('data/images/goblin/goblin_dead')],
                 }

    def __init__(self, pos_x, pos_y, *gruop):

        super().__init__(pos_x, pos_y, self.animation['idle_right'][0], *gruop)
        self.attack_cooldown = 1500
        self.max_hp = 50
        self.hp = 50
        self.speed = 1
        self.sight_distance = 8 * 20  # радиус зрения

    def update(self, player, tile_group):
        if self.attacking:
            self.animation_speed = 0.1
        else:
            self.animation_speed = 0.15
        super().update(player, tile_group)
