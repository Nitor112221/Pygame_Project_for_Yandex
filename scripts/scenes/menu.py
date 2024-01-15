import pygame

import global_variable
import scripts.tools as tools
from scripts.scenes.language_menu import LanguageScene
from scripts.scenes.control_menu import ControlScene
from scripts.scenes.game_scene import game_scene
from scripts.scenes.WorldMap_scene import world_map_scene

from data.language import russian, english

pygame.init()

font = pygame.font.SysFont('Comic Sans MS', 72)  # шрифт для текста меню


class ButtonMusic(pygame.sprite.Sprite):
    def __init__(self, pos_x: int, pos_y: int, settings: dict):
        super().__init__()
        self.music = [tools.load_image('music/music_off.png'),
                      tools.load_image('music/music_on.png')]
        self.image = self.music[1] if settings['Music'] == 'On' else self.music[0]
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.settings = settings

    def update(self, mos_pos: tuple[int, int]):
        if self.rect.collidepoint(mos_pos):
            self.settings['Music'] = 'On' if self.settings['Music'] == 'Off' else 'Off'
            self.image = self.music[1] if self.settings['Music'] == 'On' else self.music[0]
            tools.save_user_options(self.settings)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))


class Menu:  # класс отвечающий за кнопки в меню
    def __init__(self):
        self.option_surflaces: list[str] = list()  # список с поверхностями текста
        self.option_callback = list()  # список с функциями которые принадлежат кнопкам
        self.current_option_index = 0  # текущий элемент
        self.is_action_menu = True  # говорит активно ли сейчас меню, что бы блокировать его в некоторые моменты

    def append_option(self, option: str, callback) -> None:  # метод для дабавление разделов в menu
        self.option_surflaces.append(option)
        self.option_callback.append(callback)

    def switch(self, direction: int) -> None:  # переключение текущего элемента
        if self.is_action_menu:
            self.current_option_index = (self.current_option_index + direction) % len(self.option_callback)

    def select(self):  # вызывает функцию, привязанную к выбранному элеметну и возвращает результат вызова функции
        if self.is_action_menu:
            return self.option_callback[self.current_option_index]()

    # метод для преобразования текущих координат мыши в относительные для расчёта пересечений
    @staticmethod
    def hover(mos_pos: tuple[int, int], screen: pygame.Surface, virtual_surface: pygame.Surface) -> tuple[int, int]:
        x_coeff = virtual_surface.get_width() / screen.get_width()
        y_coeff = virtual_surface.get_height() / screen.get_height()
        return int(mos_pos[0] * x_coeff), int(mos_pos[1] * y_coeff)

    def draw(self, surface: pygame.Surface, option_y_padding: int, screen: pygame.Surface, settings: dict) -> None:
        # метод отрисовки всех элементов
        # координаты расположения меню относительно виртуальнйо поверхности
        x, y = surface.get_width() * 0.025, surface.get_height() * 0.555
        if settings['Language'] == 'English':
            lang = english.eng
        elif settings['Language'] == 'Русский':
            lang = russian.rus

        for i, option in enumerate(self.option_surflaces):  # проходимся по всем повехностям
            # создаём прямоугольник описывающий текст2
            option = font.render(lang[option], True, pygame.Color((255, 255, 255)))
            option_rect = option.get_rect()
            option_rect.topleft = (x, y + i * option_y_padding)
            if self.is_action_menu:
                if option_rect.collidepoint(self.hover(pygame.mouse.get_pos(), screen, surface)):
                    # проверяем на пересечение с мышкой
                    # и меняем текущий выбранный элемент на тот, на который указывает мышь
                    self.current_option_index = i
            if i == self.current_option_index:  # если текущий элемент выбранн, создаём подчёркивание для него
                underline = pygame.Surface((option.get_width(), 4))
                underline.fill(pygame.Color((235, 235, 235)))
                underline_pos = (option_rect.x, option_rect.bottom - option_y_padding // 5)
            surface.blit(option, option_rect)  # отрисовываем текст
        surface.blit(underline, underline_pos)  # отрисовываем подчёркивание

    def check_mouse_event(self, option_y_padding, screen, surf, settings: dict):
        # метод находящий элемент на который указывает мышь
        x, y = surf.get_width() * 0.025, surf.get_height() * 0.555
        if settings['Language'] == 'English':
            lang = english.eng
        elif settings['Language'] == 'Русский':
            lang = russian.rus

        for i, option in enumerate(self.option_surflaces):  # проходимся по всем повехностям
            # создаём прямоугольник описывающий текст2
            option = font.render(lang[option], True, pygame.Color((255, 255, 255)))
            option_rect = option.get_rect()
            option_rect.topleft = (x, y + i * option_y_padding)
            if self.is_action_menu:
                if option_rect.collidepoint(self.hover(pygame.mouse.get_pos(), screen, surf)):
                    return self.option_callback[i]()


def menu_scene(screen: pygame.Surface, virtual_surface: pygame.Surface, switch_scene, settings: dict) -> None:
    # меню игры
    extra_scene = None  # переменная хранящая текущую доп сцену (с выбором языка или гайдом по управлению)
    menu = Menu()  # создание меню
    running = True
    music_btn = ButtonMusic(int(virtual_surface.get_width() - virtual_surface.get_width() * 0.03 - 32),
                            int(virtual_surface.get_height() * 0.06 - 16),
                            settings)

    def open_language_scene() -> None:  # функция открывающая окно выбора языка и блокирующая меню
        nonlocal extra_scene, menu, virtual_surface
        extra_scene = LanguageScene(*virtual_surface.get_size(), settings)  # создание меню выбора языков
        menu.is_action_menu = False  # блокировка меню

    def open_control_scene() -> None:  # функция открывающая окно гайда по игре и блокирующая меню
        nonlocal extra_scene, menu, virtual_surface
        extra_scene = ControlScene(*virtual_surface.get_size(), settings)
        menu.is_action_menu = False

    def open_game_scene() -> None:  # функция запуска основной игры
        nonlocal running
        running = False
        switch_scene(world_map_scene)

    # создание кнопок меню
    menu.append_option('Play', open_game_scene)  # запускает игру
    menu.append_option('Control', open_control_scene)  # открывает окно изменения настроек
    menu.append_option('Language', open_language_scene)  # открывает окно выбора языка
    menu.append_option('Exit', lambda: 'Exit')  # выполняет выход из игры

    # загружаем задний фон
    background = tools.load_image('background.png')
    background = pygame.transform.scale(background, virtual_surface.get_size())

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
                if menu.check_mouse_event(100, screen, virtual_surface, settings) == 'Exit':
                    # если метод вернул Exit - закрываем игру
                    running = False
                    switch_scene(None)
                music_btn.update(tools.hover(pygame.mouse.get_pos(), screen, virtual_surface))
            if extra_scene is not None:
                if extra_scene.handle_event(event, virtual_surface, screen) == 'Close':
                    # если метод вернул Close - закрываем доп окно и востанавливаем функционал меню
                    extra_scene = None
                    menu.is_action_menu = True

        # отрисовываем всё на сцене
        virtual_surface.fill((0, 0, 0))
        virtual_surface.blit(background, (0, 0))
        menu.draw(virtual_surface, 100, screen, settings)
        if extra_scene is not None:
            extra_scene.draw(virtual_surface)

        music_btn.draw(virtual_surface)

        # отрисовываем сцену на экране
        scaled_surface = pygame.transform.scale(virtual_surface, screen.get_size())
        screen.blit(scaled_surface, (0, 0))
        global_variable.increase_volume(settings)
        pygame.display.flip()
