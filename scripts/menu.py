import pygame
import scripts.tools as tools

pygame.init()

font = pygame.font.SysFont('Comic Sans MS', 72)


class Menu:  # класс отвечающий за кнопки в меню
    def __init__(self):
        self.option_surflaces: list[pygame.Surface] = list()  # список с поверхностями текста
        self.option_callback = list()  # список с функциями которые принадлежат кнопкам
        self.current_option_index = 0  # текущий элемент

    def append_option(self, option: str, callback) -> None:
        self.option_surflaces.append(font.render(option, True, pygame.Color((255, 255, 255))))
        self.option_callback.append(callback)

    def swith(self, direction: int) -> None:
        self.current_option_index = (self.current_option_index + direction) % len(self.option_callback)

    def select(self):
        return self.option_callback[self.current_option_index]()

    def draw(self, surf: pygame.Surface, x: int, y: int, option_y_padding: int) -> None:
        for i, option in enumerate(self.option_surflaces):
            option_rect = option.get_rect()
            option_rect.topleft = (x, y + i * option_y_padding)
            if i == self.current_option_index:
                underline = pygame.Surface((option.get_width(), 4))
                underline.fill(pygame.Color((235, 235, 235)))
                surf.blit(underline, (option_rect.x, option_rect.bottom - option_y_padding // 5))
            surf.blit(option, option_rect)


def menu_scene(screen: pygame.Surface, virtual_surface: pygame.Surface, switch_scene) -> None:  # меню игры
    # создание кнопок меню
    menu = Menu()
    menu.append_option('Играть', lambda: print('нажата кнопка Играть'))  # действий пока нет
    menu.append_option('Настройки', lambda: print('нажата кнопка Настройки'))  # действий пока нет
    menu.append_option('Язык', lambda: print('нажата кнопка Язык'))  # действий пока нет
    menu.append_option('Выйти', lambda: 'Exit')  # выполняет выход из игры

    # загружаем задний фон
    background = tools.load_image('background.png')
    background = pygame.transform.scale(background, virtual_surface.get_size())

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                switch_scene(None)
            if event.type == pygame.KEYDOWN:
                key = pygame.key.get_pressed()
                if key[pygame.K_UP]:  # движение меню с помощью стрелочек
                    menu.swith(-1)
                elif key[pygame.K_DOWN]:
                    menu.swith(1)
                elif key[pygame.K_RETURN]:
                    if menu.select() == 'Exit':
                        running = False
                        switch_scene(None)

        # отрисовываем всё на сцене
        virtual_surface.fill((0, 0, 0))
        virtual_surface.blit(background, (0, 0))
        menu.draw(virtual_surface, 50, 600, 70)
        # отрисовываем сцену на экране
        scaled_surface = pygame.transform.scale(virtual_surface, screen.get_size())
        screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()
