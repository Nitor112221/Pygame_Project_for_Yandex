import pygame

# Инициализация Pygame
pygame.init()


class LanguegeScene:
    def __init__(self, width: int, height: int):
        self.width, self.height = round(width * 0.6), round(height * 0.6)
        self.languages = ["English", "Русский"]  # Список поддерживаемых языков
        self.selected_language = None

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
            underline_pos = (selected_rect.x, selected_rect.bottom - 5)
            surface.blit(underline, underline_pos)

    def handle_event(self, event, surface: pygame.Surface):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()  # Используем координаты мыши относительно окна
            if self.is_inside_menu(mouse_pos, surface):
                index = (mouse_pos[1] - round(surface.get_height() * 0.2)) // 50
                if 0 <= index < len(self.languages):
                    self.selected_language = self.languages[index]
                    print(f"Selected Language: {self.selected_language}")
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return 'Close'

    def is_inside_menu(self, mouse_pos, surface: pygame.Surface) -> bool:
        menu_rect = pygame.Rect(surface.get_width() * 0.2, surface.get_height() * 0.2, self.width, self.height)
        return menu_rect.collidepoint(mouse_pos)
