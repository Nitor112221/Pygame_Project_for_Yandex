from scripts.entity.Entity import Entity
import pygame
import scripts.tools as tools


class BaseHero(Entity):
    def __init__(self, pos_x: int, pos_y: int, settings: dict, *group):
        animation = {
            'walk_left': [tools.load_image('player/KnightWalk2.png', reverse=True),
                          tools.load_image('player/KnightIdle2.png', reverse=True),
                          tools.load_image('player/KnightIdle1.png', reverse=True),
                          tools.load_image('player/KnightWalk1.png', reverse=True)],
            'walk_right': [tools.load_image('player/KnightWalk2.png'),
                           tools.load_image('player/KnightIdle2.png'),
                           tools.load_image('player/KnightIdle1.png'),
                           tools.load_image('player/KnightWalk1.png')],
            'jump_left': [tools.load_image('player/KnightJump.png', reverse=True)],
            'jump_right': [tools.load_image('player/KnightJump.png')],
            'fall_left': [tools.load_image('player/KnightFall.png', reverse=True)],
            'fall_right': [tools.load_image('player/KnightFall.png')],
            'idle_left': [tools.load_image('player/KnightIdle1.png', reverse=True),
                          tools.load_image('player/KnightIdle1.png', reverse=True),
                          tools.load_image('player/KnightIdle2.png', reverse=True),
                          tools.load_image('player/KnightIdle2.png', reverse=True)],
            'idle_right': [tools.load_image('player/KnightIdle1.png'),
                           tools.load_image('player/KnightIdle1.png'),
                           tools.load_image('player/KnightIdle2.png'),
                           tools.load_image('player/KnightIdle2.png')],
            'classic_left': [tools.load_image('player/Knight.png', reverse=True)],
            'classic_right': [tools.load_image('player/Knight.png')]
        }

        super().__init__(tools.load_image('player/Knight.png'), pos_x, pos_y, animation, *group)
        self.settings = settings

    def handler_event(self, event):
        # обработка движений с неотпусканием клавиш
        if event.type == pygame.KEYDOWN:  # начинаем действие
            if event.key == getattr(pygame, f"K_{self.settings['Jump'].upper()}"):
                self.jump()
            if event.key == getattr(pygame, f"K_{self.settings['Left'].lower()}"):
                self.x_speed += -2
            if event.key == getattr(pygame, f"K_{self.settings['Right'].lower()}"):
                self.x_speed += 2
            if event.key == getattr(pygame, f"K_{self.settings['Down'].lower()}"):
                self.y_speed += 2
        elif event.type == pygame.KEYUP:  # заканчиваем движение
            if event.key == getattr(pygame, f"K_{self.settings['Jump'].upper()}"):
                self.y_speed = max(-2, self.y_speed)
            if event.key == getattr(pygame, f"K_{self.settings['Left'].lower()}"):
                self.x_speed += 2
            if event.key == getattr(pygame, f"K_{self.settings['Right'].lower()}"):
                self.x_speed -= 2
            if event.key == getattr(pygame, f"K_{self.settings['Down'].lower()}"):
                self.y_speed = max(self.y_speed, self.y_speed - 2)

    def jump(self):
        if self.is_grounded:
            self.y_speed += self.jump_speed
            self.status = 'jump_' + self.direction
            self.is_grounded = False
