import pygame
import scripts.tools as tools

# Инициализация Pygame
pygame.init()


class LanguageScene:
    def __init__(self, width: int, height: int, settings: dict):
        self.width, self.height = round(width * 0.6), round(height * 0.6)
        self.languages = ["English", "Русский"]  # Список поддерживаемых языков
        self.settings = settings
        self.selected_language = settings['Language']

    def draw(self, surface: pygame.Surface):  # Метод отрисовки меню выбора языков
        scene_surface = pygame.Surface((self.width, self.height))
        scene_surface.fill(pygame.Color('White'))
        scene_surface.set_alpha(50)
        surface.blit(scene_surface, (surface.get_width() * 0.2, surface.get_height() * 0.2))

        pygame.draw.rect(surface, (255, 255, 255),  # Рамка вокруг меню
                         (surface.get_width() * 0.2, surface.get_height() * 0.2, self.width, self.height), width=3,
                         border_radius=20)

        font = pygame.font.SysFont('Comic Sans MS', 36)
        text_color = pygame.Color((0, 0, 0))

        if self.selected_language == 'Русский':
            text = font.render('Назад: Esc', True, text_color)
        elif self.selected_language == 'English':
            text = font.render('Back: Esc', True, text_color)
        surface.blit(text, (surface.get_width() * 0.2 + 10, surface.get_height() * 0.2 + 10))

        for i, language in enumerate(self.languages):
            text = font.render(language, True, text_color)
            text_rect = text.get_rect(center=(surface.get_width() * 0.5,
                                              surface.get_height() * 0.3 + i * 50))
            surface.blit(text, text_rect)

        # Отображение подчеркивания под выбранным языком
        if self.selected_language is not None:
            selected_text = font.render(self.selected_language, True, text_color)
            selected_rect = selected_text.get_rect(center=(surface.get_width() * 0.5,
                                                           surface.get_height() * 0.3 + self.languages.index(
                                                               self.selected_language) * 50 + 40))
            underline = pygame.Surface((selected_text.get_width(), 4))
            underline.fill(pygame.Color((0, 0, 0)))
            underline_pos = (selected_rect.x, selected_rect.bottom - 50)
            surface.blit(underline, underline_pos)

    def handle_event(self, event, surface: pygame.Surface, screen):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in (pygame.BUTTON_LEFT, pygame.BUTTON_RIGHT):
                mouse_pos = self.hover(pygame.mouse.get_pos(), screen, surface)
                # Используем координаты мыши относительно окна
                if self.is_inside_menu(mouse_pos, surface):
                    index = (mouse_pos[1] - round(surface.get_height() * 0.275)) // 50
                    if 0 <= index < len(self.languages):
                        # если мышка указывает на существующий язык и произошёл клик, то выбранный язык меняется на
                        # указанный
                        self.selected_language = self.languages[index]
                        self.settings['Language'] = self.selected_language
        elif event.type == pygame.KEYDOWN:
            # если была нажата кнопка Esc, то доп окно должно закрытся, а язык сохранится в файле
            if event.key == pygame.K_ESCAPE:
                tools.save_user_options(self.settings)
                return 'Close'

            # управление выбором языков с помощью стрелочек
            elif event.key == pygame.K_UP:
                ind = (self.languages.index(self.selected_language) - 1) % len(self.languages)
                self.selected_language = self.languages[
                    (self.languages.index(self.selected_language) - 1) % len(self.languages)]  # Листаем вверх
                self.selected_language = self.languages[ind]
                self.settings['Language'] = self.selected_language
            elif event.key == pygame.K_DOWN:
                ind = (self.languages.index(self.selected_language) + 1) % len(self.languages)
                self.selected_language = self.languages[
                    (self.languages.index(self.selected_language) + 1) % len(self.languages)]  # Листаем вниз
                self.selected_language = self.languages[ind]
                self.settings['Language'] = self.selected_language

    def is_inside_menu(self, mouse_pos, surface: pygame.Surface) -> bool:
        # метод проверки на то, что мышка находится в пределах доп экрана
        menu_rect = pygame.Rect(surface.get_width() * 0.2, surface.get_height() * 0.2, self.width, self.height)
        return menu_rect.collidepoint(mouse_pos)

    @staticmethod
    def hover(mos_pos: tuple[int, int], screen: pygame.Surface, virtual_surface: pygame.Surface) -> tuple[int, int]:
        # метод, который преобразует координаты мыши на экране в координаты мыши относительно виртуальной поверхности
        x_coeff = virtual_surface.get_width() / screen.get_width()
        y_coeff = virtual_surface.get_height() / screen.get_height()
        return int(mos_pos[0] * x_coeff), int(mos_pos[1] * y_coeff)
