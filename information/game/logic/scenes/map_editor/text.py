import pygame
import logic.tools as tools


# Главный класс, отвечающий за отрисовку текста
class Text:
    def __init__(self, screen, x, y, font_name=None):
        self.screen = screen
        self.x = x
        self.y = y
        self.pos = (self.x, self.y)

        self.color = pygame.Color((255, 255, 255))
        self.font_name = tools.load_font(font_name)
        self.font = pygame.font.Font(self.font_name, 15)

    def render(self, coor, focus) -> None:
        """
        Метод отрисовки текста
        :return: None
        """
        if focus:
            text = f'{coor[0]};{coor[1]}'
        else:
            text = f'Not focused'
        text_surface = self.font.render(text, True, self.color)
        self.screen.blit(text_surface, self.pos)
