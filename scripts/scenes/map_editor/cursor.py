import pygame
import scripts.tools as tools


# Главный класс, отвечающий за смену курсора
class Cursor:
    def __init__(self, screen):
        self.hand_cursor = tools.load_image('cursor_map_editor/hand.png', -1)
        self.list_cursors = [self.hand_cursor]  # [...] - можно добавить еще много разных курсоров
        self.screen = screen

    def prewiew(self, index, position_mouse):
        group_cursors = pygame.sprite.Group()
        position_mouse_x = position_mouse[0]
        position_mouse_y = position_mouse[1]
        cursor = pygame.sprite.Sprite()
        cursor.image = self.list_cursors[index]
        cursor.rect = cursor.image.get_rect()
        cursor.rect.x, cursor.rect.y = position_mouse_x - 7, position_mouse_y
        group_cursors.add(cursor)
        group_cursors.draw(self.screen)
