import pygame
import scripts.tools as tools

# Инициализация Pygame
pygame.init()


class SettingsScene:
    def __init__(self, width: int, height: int, settings: dict):
        self.width, self.height = round(width * 0.6), round(height * 0.6)
        self.settings = settings
        self.options = list(settings.items())
        self.options.pop(0)  # Используем ключи словаря settings как опции
        self.selected_option = None
        self.current_shift = 0

    def draw(self, surface: pygame.Surface):  # Метод отрисовки меню изменения настроек
        background_scene = pygame.Surface((self.width, self.height))
        background_scene.fill(pygame.Color('White'))  # Заполнение поверхности белым цветом
        background_scene.set_alpha(50)
        surface.blit(background_scene, (surface.get_width() * 0.2, surface.get_height() * 0.2))

        settings_scene = pygame.Surface((self.width, self.height))
        settings_scene.fill((255, 255, 255))
        settings_scene.set_colorkey((255, 255, 255))

        pygame.draw.rect(surface, (255, 255, 255),  # Рамка вокруг меню
                         (surface.get_width() * 0.2, surface.get_height() * 0.2, self.width, self.height), width=3,
                         border_radius=20)

        font = pygame.font.SysFont('Comic Sans MS', 36)
        text_color = pygame.Color((0, 0, 0))
        self.current_shift = max((-(len(self.options) - 12) * 50),
                                 min(0, self.current_shift))

        for i, option in enumerate(self.options):
            text = font.render(f'{option[0]}: {option[1]}', False, text_color)
            text_rect = text.get_rect(center=(settings_scene.get_width() * 0.5,
                                              settings_scene.get_height() * 0.125 + i * 50 + self.current_shift))
            settings_scene.blit(text, text_rect)

        # Отображение подчеркивания под выбранным вариантом
        if self.selected_option is not None:
            selected_text = font.render(f'{self.selected_option[0]}: {self.selected_option[1]}', False, text_color)
            selected_rect = selected_text.get_rect(center=(settings_scene.get_width() * 0.5,
                                                           settings_scene.get_height() * 0.125 + self.options.index(
                                                               self.selected_option) * 50 + 40 + self.current_shift))
            underline = pygame.Surface((selected_text.get_width(), 4))
            underline.fill(pygame.Color((0, 0, 0)))
            underline_pos = (selected_rect.x, selected_rect.bottom - 50)
            settings_scene.blit(underline, underline_pos)
        surface.blit(settings_scene, (surface.get_width() * 0.2, surface.get_height() * 0.2))

    def handle_event(self, event, surface: pygame.Surface, screen):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in (pygame.BUTTON_LEFT, pygame.BUTTON_RIGHT):
                mouse_pos = self.hover(pygame.mouse.get_pos(), screen, surface)
                # Используем координаты мыши относительно окна
                if self.is_inside_menu(mouse_pos, surface):
                    index = (mouse_pos[1] - round(surface.get_height() * 0.25 + self.current_shift)) // 50
                    if 0 <= index < len(self.options):
                        self.selected_option = self.options[index]
                        if index < abs(self.current_shift) // 50 or index >= (12 + abs(self.current_shift) // 50):
                            self.current_shift = -index * 50  # Автоматический сдвиг списка
                        print(f"Changed Option: {self.selected_option[0]} - {self.selected_option[1]}")
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                tools.save_user_options(self.settings)  # Сохранение настроек
                return 'Close'
            elif event.key == pygame.K_UP:
                ind = 0
                if self.selected_option is not None:
                    ind = (self.options.index(self.selected_option) - 1) % len(self.options)  # Листаем вверх
                self.selected_option = self.options[ind]
                if ind < abs(self.current_shift) // 50 or ind >= (12 + abs(self.current_shift) // 50):
                    self.current_shift = -ind * 50  # Автоматический сдвиг списка
            elif event.key == pygame.K_DOWN:
                ind = 0
                if self.selected_option is not None:
                    ind = (self.options.index(self.selected_option) + 1) % len(self.options)  # Листаем вниз
                self.selected_option = self.options[ind]
                if ind < abs(self.current_shift) // 50 or ind >= (12 + abs(self.current_shift) // 50):
                    self.current_shift = -ind * 50  # Автоматический сдвиг списка

        elif event.type == pygame.MOUSEWHEEL:
            self.current_shift += event.y * 15

    def move_list(self, direction):
        pass

    def is_inside_menu(self, mouse_pos, surface: pygame.Surface) -> bool:
        menu_rect = pygame.Rect(surface.get_width() * 0.2, surface.get_height() * 0.2, self.width, self.height)
        return menu_rect.collidepoint(mouse_pos)

    @staticmethod
    def hover(mos_pos: tuple[int, int], screen: pygame.Surface, virtual_surface: pygame.Surface) -> tuple[int, int]:
        x_coeff = virtual_surface.get_width() / screen.get_width()
        y_coeff = virtual_surface.get_height() / screen.get_height()
        return int(mos_pos[0] * x_coeff), int(mos_pos[1] * y_coeff)
