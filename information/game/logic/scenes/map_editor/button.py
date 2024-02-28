import pygame
import logic.tools as tools


# Главный класс, отвечающий за кнопочки
class Button:
    def __init__(self, screen):
        self.screen = screen
        self.width_screen = screen.get_width()
        self.height_screen = screen.get_height()
        self.width = 30
        self.height = 30
        self.right = 10
        self.bottom = 10
        self.coor_x = self.width_screen - self.width - self.right
        self.coor_y = self.height_screen - self.height - self.bottom
        self.group = pygame.sprite.Group()

        self.tile_images = {
            1: tools.load_image('map_editor/menu_buttons/editor_back.png')
        }

    def render(self) -> None:
        """
        Метод отрисовки всех кнопок
        :return: None
        """
        self.group = pygame.sprite.Group()
        for key, value in self.tile_images.items():
            btn = pygame.sprite.Sprite(self.group)
            scaled_image = pygame.transform.scale(value, (self.width, self.height))
            btn.image = scaled_image
            btn.rect = btn.image.get_rect()
            btn.rect.x = self.screen.get_width() - self.width - self.right
            btn.rect.y = self.screen.get_height() - self.height - self.bottom
        self.group.draw(self.screen)

    def chek_clicked(self, coords):
        """
        Метод проверки нажатия на кнопку редактора
        :param coords: tuple
        :return: None
        """
        for sprite in self.group:
            if sprite.rect.collidepoint(coords):
                return sprite
        return None
