import pygame
import scripts.tools as tools

pygame.init()

font = pygame.font.SysFont('Comic Sans MS', 72)  # шрифт для текста меню


class Menu:  # класс отвечающий за кнопки в меню
    def __init__(self):
        self.option_surflaces: list[pygame.Surface] = list()  # список с поверхностями текста
        self.option_callback = list()  # список с функциями которые принадлежат кнопкам
        self.current_option_index = 0  # текущий элемент

    def append_option(self, option: str, callback) -> None:  # метод для дабавление разделов в menu
        self.option_surflaces.append(font.render(option, True, pygame.Color((255, 255, 255))))
        self.option_callback.append(callback)

    def switch(self, direction: int) -> None:  # переключение текущего элемента
        self.current_option_index = (self.current_option_index + direction) % len(self.option_callback)

    def select(self):  # вызывает функцию, привязанную к выбранному элеметну и возвращает результат вызова функции
        return self.option_callback[self.current_option_index]()

    # метод для преобразования текущих координат мыши в относительные для расчёта пересечений
    @staticmethod
    def hover(mos_pos: tuple[int, int], screen: pygame.Surface, virtual_surface: pygame.Surface) -> tuple[int, int]:
        x_coeff = virtual_surface.get_width() / screen.get_width()
        y_coeff = virtual_surface.get_height() / screen.get_height()
        return int(mos_pos[0] * x_coeff), int(mos_pos[1] * y_coeff)

    def draw(self, surface: pygame.Surface, x: int, y: int, option_y_padding: int, screen: pygame.Surface) -> None:
        # метод отрисовки всех элементов
        for i, option in enumerate(self.option_surflaces):  # проходимся по всем повехностям
            # создаём прямоугольник описывающий текст
            option_rect = option.get_rect()
            option_rect.topleft = (x, y + i * option_y_padding)
            if option_rect.collidepoint(self.hover(pygame.mouse.get_pos(), screen, surface)):
                # проверяем на пересечение с мышкой и меняем текущий выбранный элемент на тот, на который указывает мышь
                self.current_option_index = i
            if i == self.current_option_index:  # если текущий элемент выбранн, создаём подчёркивание для него
                underline = pygame.Surface((option.get_width(), 4))
                underline.fill(pygame.Color((235, 235, 235)))
                underline_pos = (option_rect.x, option_rect.bottom - option_y_padding // 5)
            surface.blit(option, option_rect)  # отрисовываем текст
        surface.blit(underline, underline_pos)   # отрисовываем подчёркивание

    def check_mouse_event(self, x, y, option_y_padding, screen, surf):
        # метод находящий элемент на который указывает мышь
        for i, option in enumerate(self.option_surflaces):
            option_rect = option.get_rect()
            option_rect.topleft = (x, y + i * option_y_padding)
            if option_rect.collidepoint(self.hover(pygame.mouse.get_pos(), screen, surf)):
                return self.select()


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
                # изменение выбранного элеметна меню с помощью стрелочек
                if key[pygame.K_UP]:
                    menu.switch(-1)
                elif key[pygame.K_DOWN]:
                    menu.switch(1)
                elif key[pygame.K_RETURN]:
                    if menu.select() == 'Exit':  # если функция вернула Exit - закрываем игру
                        running = False
                        switch_scene(None)
            if event.type == pygame.MOUSEBUTTONDOWN:  # обработка нажатий мыши
                if menu.check_mouse_event(50, 600, 70, screen, virtual_surface) == 'Exit':
                    running = False
                    switch_scene(None)
        # отрисовываем всё на сцене
        virtual_surface.fill((0, 0, 0))
        virtual_surface.blit(background, (0, 0))
        menu.draw(virtual_surface, 50, 600, 70, screen)
        # отрисовываем сцену на экране
        scaled_surface = pygame.transform.scale(virtual_surface, screen.get_size())
        screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()
