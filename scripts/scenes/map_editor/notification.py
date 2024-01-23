import pygame
import scripts.tools as tools
from scripts.scenes.map_editor.convert_index import ConvertTile


# Бета-версия оповещений
class Notification:
    def __init__(self, screen):
        self.screen = screen
        self.width = 200
        self.height = 35
        self.x = screen.get_width() - self.width - 20
        self.y = 20
        self.color = pygame.Color((10, 27, 61))
        self.border_color = pygame.Color((165, 165, 165))
        self.text_color = pygame.Color((255, 255, 255))
        self.alpha = 255
        self.start_time = pygame.time.get_ticks()
        self.elapsed_time = pygame.time.get_ticks() - self.start_time
        self.notification_group = pygame.sprite.Group()

        # Загругленная поверхность
        self.rounded_surface = pygame.Surface((200, 35))
        pygame.draw.rect(self.rounded_surface, self.color, (0, 0, self.width, self.height), border_radius=10)
        pygame.draw.rect(self.rounded_surface, self.border_color, (0, 0, self.width, self.height), 1, border_radius=10)

        # Текст
        text = 'начало работы'
        self.font_name = tools.load_font('minecraft_seven_2.ttf')
        self.font = pygame.font.Font(self.font_name, 15)
        self.text_render = self.font.render(text, True, self.text_color)

        # Все изображения иконок оповещений
        self.tile_images = {
            1: [tools.load_image('map_editor/editor_notification/notification.png'), 'notification']
        }

        image = self.tile_images[1][0]
        width_image, height_image = 25, 25
        self.scaled_image = pygame.transform.scale(image, (width_image, height_image))

    def render(self):
        self.elapsed_time = pygame.time.get_ticks() - self.start_time
        if self.elapsed_time < 2000:
            self.screen.blit(self.rounded_surface, (self.x, self.y))
            self.screen.blit(self.text_render, (self.x + 50, self.y + 6))
            self.screen.blit(self.text_render, (self.x + 50, self.y + 6))
            self.screen.blit(self.scaled_image, (self.x + 15, self.y + 5))

        else:
            if self.alpha > 0:
                self.alpha -= 3
                self.rounded_surface.set_alpha(self.alpha)
                self.text_render.set_alpha(self.alpha)
                self.scaled_image.set_alpha(self.alpha)
                self.screen.blit(self.rounded_surface, (self.x, self.y))
                self.screen.blit(self.text_render, (self.x + 50, self.y + 6))
                self.screen.blit(self.scaled_image, (self.x + 15, self.y + 5))

