import pygame
import scripts.tools as tools


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
            1: tools.load_image('menu_buttons/editor_back.png')
        }

    def render(self):
        for key, value in self.tile_images.items():
            btn = pygame.sprite.Sprite(self.group)
            scaled_image = pygame.transform.scale(value, (self.width, self.height))
            btn.image = scaled_image
            btn.rect = btn.image.get_rect()
            btn.rect.x, btn.rect.y = self.coor_x, self.coor_y
        self.group.draw(self.screen)

    def chek_clicked(self, coords):
        for sprite in self.group:
            if sprite.rect.collidepoint(coords):
                return sprite
        return None
