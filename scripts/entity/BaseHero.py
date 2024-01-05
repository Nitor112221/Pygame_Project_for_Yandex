from scripts.entity.entity import Entity
import pygame
import scripts.tools as tools


class BaseHero(Entity):
    def __init__(self, pos_x, pos_y, *group):
        super().__init__(tools.load_image('player/player.png'), pos_x, pos_y, *group)

    def handler_event(self, event):
        # обработка движений с неотпусканием клавиш
        if event.type == pygame.KEYDOWN:  # начинаем действие
            if event.key == pygame.K_SPACE:
                self.jump()
            if event.key == pygame.K_LEFT:
                self.x_speed += -4
            if event.key == pygame.K_RIGHT:
                self.x_speed += 4
        elif event.type == pygame.KEYUP:  # заканчиваем движение
            if event.key == pygame.K_SPACE:
                self.y_speed = max(0, self.y_speed)
            if event.key == pygame.K_LEFT:
                self.x_speed += 4
            if event.key == pygame.K_RIGHT:
                self.x_speed -= 4

    def jump(self):
        if self.is_grounded:
            self.y_speed += self.jump_speed
        self.is_grounded = False
