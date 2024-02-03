import pygame

import global_variable
from data.language import russian, english


class Button(pygame.sprite.Sprite):
    font = pygame.font.SysFont('Comic Sans MS', 15)

    def __init__(self, pos_x: int, pos_y: int, text: str, settings: dict):
        super().__init__()
        if settings['Language'] == 'English':
            lang = english.eng
        elif settings['Language'] == 'Русский':
            lang = russian.rus
        self.image = pygame.Surface((100, 20), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (70, 70, 70), self.image.get_rect(), 0, 20)
        text_surf = self.font.render(lang[text], False, 'White')
        self.image.blit(text_surf, (self.image.get_width() // 2 - text_surf.get_width() // 2,
                                    self.image.get_height() // 2 - text_surf.get_height() // 2))
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.image.get_rect().move(pos_x, pos_y)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)


class DeadScreen:
    def __init__(self, surface: pygame.Surface, settings: dict):
        # создание полупрозрачной поверхности
        self.screen = pygame.Surface((surface.get_width() * 0.6, surface.get_height() * 0.6), pygame.SRCALPHA)
        self.surface = surface
        scene_surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        pygame.draw.rect(scene_surface, (60, 60, 60), self.screen.get_rect(), 0, 20)
        scene_surface.set_alpha(150)
        self.screen.blit(scene_surface, (0, 0))
        pygame.draw.rect(self.screen, (255, 255, 255), self.screen.get_rect(), width=1, border_radius=20)

        # создание кнопок
        self.button_map = Button(int(self.screen.get_width() * 0.2 - 35), int(self.screen.get_height() * 0.2), 'Map',
                                 settings)
        self.button_menu = Button(int(self.screen.get_width() * 0.8 - 65), int(self.screen.get_height() * 0.2), 'Menu',
                                  settings)
        self.button_repeat = Button(int(self.screen.get_width() * 0.5 - 40), int(self.screen.get_height() * 0.7),
                                    'Repeat', settings)
        self.button_menu.draw(self.screen)
        self.button_map.draw(self.screen)
        self.button_repeat.draw(self.screen)

    def draw(self):
        self.surface.blit(self.screen, (self.surface.get_width() * 0.2, self.surface.get_height() * 0.2))

    def update(self, mos_pos: tuple[int, int], switch_scene) -> None or str:
        # проверка на то нажаты ли кнопки
        if self.surface.get_width() * 0.2 <= mos_pos[0] < self.surface.get_width() * 0.8 and \
                self.surface.get_height() * 0.2 <= mos_pos[1] < self.surface.get_height() * 0.8:
            if self.button_map.rect.collidepoint(mos_pos[0] - self.surface.get_width() * 0.2,
                                                 mos_pos[1] - self.surface.get_height() * 0.2):
                switch_scene('world_map')
                global_variable.is_music_play = False
                return 'YES'
            elif self.button_menu.rect.collidepoint(mos_pos[0] - self.surface.get_width() * 0.2,
                                                    mos_pos[1] - self.surface.get_height() * 0.2):
                switch_scene('menu_scene')
                global_variable.is_music_play = False
                return 'YES'
            elif self.button_repeat.rect.collidepoint(mos_pos[0] - self.surface.get_width() * 0.2,
                                                      mos_pos[1] - self.surface.get_height() * 0.2):
                switch_scene('game_scene')
                return 'YES'
