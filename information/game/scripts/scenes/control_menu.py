import pygame
import logic.tools as tools
from data.language import russian, english

# Инициализация Pygame
pygame.init()


class ControlScene:
    def __init__(self, width: int, height: int, settings: dict):
        self.width, self.height = round(width * 0.6), round(height * 0.6)
        self.settings = settings
        self.options = list(settings.items())  # Используем ключи словаря settings как опции
        self.options.pop(0)  # удаляем языки из списка
        self.current_shift = 0  # сдвиг при просмотре

    def draw(self, surface: pygame.Surface):  # Метод отрисовки меню изменения настроек
        background_scene = pygame.Surface((self.width, self.height))
        background_scene.fill(pygame.Color('White'))  # Заполнение поверхности белым цветом
        background_scene.set_alpha(50)
        surface.blit(background_scene, (surface.get_width() * 0.2, surface.get_height() * 0.2))

        # устанавлеваем перевод в зависимости от выбранного
        if self.settings['Language'] == 'English':
            lang = english.eng
        elif self.settings['Language'] == 'Русский':
            lang = russian.rus

        # делаем прозрачный экран с интерфесом
        settings_scene = pygame.Surface((self.width, self.height))
        settings_scene.fill((255, 255, 255))
        settings_scene.set_colorkey((255, 255, 255))

        pygame.draw.rect(surface, (255, 255, 255),  # Рамка вокруг
                         (surface.get_width() * 0.2, surface.get_height() * 0.2, self.width, self.height), width=3,
                         border_radius=20)

        font = pygame.font.SysFont('Comic Sans MS', 36)
        text_color = pygame.Color((0, 0, 0))

        # инструкция как файлы в записимости от языка
        if self.settings['Language'] == 'Русский':
            text = font.render('Назад: Esc', True, text_color)
        elif self.settings['Language'] == 'English':
            text = font.render('Back: Esc', True, text_color)
        surface.blit(text, (surface.get_width() * 0.2 + 10, surface.get_height() * 0.2 + 10))

        # ограничения прокрутки в верх и вниз взависиомсти от колличества элементов
        min_limit = -(len(self.options) - 11) * 50
        if min_limit > 0:
            min_limit = 0
        self.current_shift = max(min_limit,
                                 min(0, self.current_shift))

        # отрисовка опций
        for i, option in enumerate(self.options):
            text = font.render(f'{lang[option[0]]}: {option[1]}', False, text_color)
            text_rect = text.get_rect(center=(settings_scene.get_width() * 0.5,
                                              settings_scene.get_height() * 0.125 + i * 50 + self.current_shift))
            settings_scene.blit(text, text_rect)

        surface.blit(settings_scene, (surface.get_width() * 0.2, surface.get_height() * 0.2))

    def handle_event(self, event, virtual_surface, screen):
        # оброботчик событий
        # (что бы не нарушать концепцию полиморфизма, мы получаем также virtual_surface, screen, которые не исопльзуем)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # если нажата кнопка Esc посылаем сигнал на закрытие окна
                tools.save_user_options(self.settings)  # Сохранение настроек
                return 'Close'
        elif event.type == pygame.MOUSEWHEEL:  # прокрутка колёсика мыши
            self.current_shift += event.y * 15

