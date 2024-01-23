import sys
import time
import pygame
from scripts.scenes.map_editor.tile import Tile
from scripts.scenes.map_editor.board import Board
from scripts.scenes.map_editor.button import Button
from scripts.scenes.map_editor.text import Text
from scripts.scenes.map_editor.cursor import Cursor
from scripts.scenes.map_editor.convert_index import ConvertTile
from scripts.scenes.map_editor.notification import Notification


# Главный класс сцены редактора уровней
class EditorScene:
    def __init__(self, screen, virtual_surface: pygame.Surface, switch_scene, settings):
        # основные характеристики сцены
        self.switch_scene = switch_scene
        self.settings = settings
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.virtual_surface = pygame.Surface((virtual_surface.get_width() * 0.5, virtual_surface.get_height() * 0.5))
        self.FPS = 90
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(False)
        self.prewiew_cursor = True

        # Текущий выбранный тайл для отрисовки
        self.current_tile = None
        # Индексы текущих выбранных тайла и курсора для отрисовки
        self.current_index_tile = None
        self.current_index_cursor = None
        # Последнии координаты мыши, поля и переменная нахождения мыши в области поля
        self.last_coordinate = (0, 0)
        self.last_coor_board = (0, 0)
        self.focus_board = None
        # Имя файла, для сохранения уровня
        self.filename = 'level_2'
        # Инстансы классов доски, тайла, кнопки
        self.notification = Notification(self.screen)
        self.convert_tile = ConvertTile()
        self.board = Board(screen, self.filename, self.last_coordinate)
        self.tile = Tile(screen)
        self.button = Button(screen)
        self.cursor = Cursor(screen)
        self.text1 = Text(screen, 5, 5, 'minecraft_seven_2.ttf')
        self.text2 = Text(screen, 5, 30, 'minecraft_seven_2.ttf')
        self.list_text = [self.text1, self.text2]

        # Запускаем обработку пользовательских действий
        self.run()

    def focused_board(self) -> None:
        """
        Функция переопределения состояния фокусировки относительно доски
        :return: None
        """
        self.focus_board = self.board.chek_clicked_on_board(self.last_coordinate)

    def select_tile(self, index) -> None:
        """
        Функция переопределения текущего тайла
        :return: None
        """
        index = index
        sprite = self.tile.return_sprite(index)
        self.current_tile = sprite
        self.current_index_tile = index
        self.tile.selected_tile = True

    def update_cursor(self, index=None, value_visible=True) -> None:
        """
        Функция переопределения состояния курсора
        :return: None
        """
        pygame.mouse.set_visible(value_visible)
        self.current_index_cursor = index

    def check_prewiew_cursor(self) -> None:
        """
        Функция проверки и переопределения отображения курсора
        :return: None
        """
        # Проверка на нахождения курсора в пространстве доски и смена его индекса в положительном случае
        if self.focus_board:
            if self.prewiew_cursor:
                self.update_cursor(0, False)
        else:
            self.current_index_cursor = None
            # Проверка на нахождения курсора в пространстве тайлов и смена его индекса в положительном случае
            if self.last_coordinate[1] >= self.screen.get_height() - (self.tile.cell_size + self.tile.bottom):
                if self.tile.last_left_coorx + self.tile.cell_size + self.tile.left \
                        < self.screen.get_width():
                    if self.prewiew_cursor:
                        self.update_cursor(0, False)

    def run(self) -> None:
        """
        Функция главного цикла всех событий
        :return: None
        """
        # Определение клавиш для разных операционных систем
        if sys.platform.startswith('win'):
            # Для Windows
            key_to_press = pygame.K_RETURN
        elif sys.platform.startswith('darwin'):
            # Для MacOS
            key_to_press = pygame.K_RETURN
        else:
            # Для других операционных систем
            key_to_press = pygame.K_RETURN

        running = True
        while running:
            self.check_prewiew_cursor()

            # Обрабатываем нажатия на различные клавиши (является ли нажатой в любой кадр игры)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                if self.last_coordinate is not None:
                    if self.last_coordinate[1] < self.screen.get_height() - (self.tile.cell_size + self.tile.bottom):
                        self.board.left += 10
                    else:
                        if self.tile.last_right_coorx - self.tile.left > 0:
                            self.tile.shift_x -= 10
                self.focused_board()
            if keys[pygame.K_RIGHT]:
                if self.last_coordinate is not None:
                    if self.last_coordinate[1] < self.screen.get_height() - (self.tile.cell_size + self.tile.bottom):
                        self.board.left -= 10
                    else:
                        if self.tile.last_left_coorx + self.tile.cell_size + self.tile.left \
                                < self.screen.get_width():
                            self.tile.shift_x += 10
                self.focused_board()
            if keys[pygame.K_DOWN]:
                self.board.top -= 10
                self.focused_board()
            if keys[pygame.K_UP]:
                self.board.top += 10
                self.focused_board()

            # Проверяем, были ли нажаты Ctrl + Z
            if keys[pygame.K_z] and (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]):
                # Если нажали на кнопку отмены действия и действия были накоплены - отменяем его (удаляем блок)
                self.board.back_render()
                # Делаем отмену отрисовки немного замедленной, чтобы действия были управляемые
                time.sleep(0.1)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.switch_scene(None)
                elif event.type == pygame.MOUSEMOTION:
                    self.last_coordinate = event.pos
                    self.board.last_coordinate = self.last_coordinate
                    self.focus_board = self.board.chek_clicked_on_board(self.last_coordinate)

                # Обработка нажатий на клавиатуру (была ли нажата любой в кадр игры)
                if event.type == pygame.KEYDOWN:
                    if event.key == key_to_press:
                        self.save_board_file(self.filename)
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                        self.switch_scene('menu_scene')
                    elif event.key == pygame.K_BACKSPACE:
                        self.board.clear_board()
                    elif event.key == pygame.K_TAB:
                        self.current_tile = None
                        self.tile.selected_tile = False
                    elif event.key == pygame.K_d and event.mod & pygame.KMOD_CTRL:
                        if self.prewiew_cursor:
                            self.prewiew_cursor = False
                        else:
                            self.prewiew_cursor = True

                    elif event.key == pygame.K_1:
                        index = 0
                        self.select_tile(index)
                    elif event.key == pygame.K_2:
                        index = 1
                        self.select_tile(index)
                    elif event.key == pygame.K_3:
                        index = 2
                        self.select_tile(index)
                    elif event.key == pygame.K_4:
                        index = 3
                        self.select_tile(index)
                    elif event.key == pygame.K_5:
                        index = 4
                        self.select_tile(index)
                    elif event.key == pygame.K_6:
                        index = 5
                        self.select_tile(index)
                    elif event.key == pygame.K_7:
                        index = 6
                        self.select_tile(index)
                    elif event.key == pygame.K_8:
                        index = 7
                        self.select_tile(index)
                    elif event.key == pygame.K_9:
                        index = 8
                        self.select_tile(index)
                    elif event.key == pygame.K_0:
                        index = 9
                        self.select_tile(index)

                self.last_coor_board = self.board.last_coor_board

                # Обработка нажатий на мышь
                mouse_pressed = pygame.mouse.get_pressed()
                try:
                    if mouse_pressed[0]:  # соответствует левой кнопке мыши
                        # Меняем выбранный тайл на новый, если нажали на него
                        return_click_on_tile = self.tile.chek_clicked(event.pos)
                        if return_click_on_tile is not None:
                            self.current_tile = return_click_on_tile[0]
                            self.current_index_tile = return_click_on_tile[1]
                            self.tile.selected_tile = True
                        self.board.chek_clicked_on_board(event.pos, self.current_tile, self.current_index_tile)

                        # Если нажали на кнопку отмены действия и действия были накоплены - отменяем его
                        return_click_on_btn = self.button.chek_clicked(event.pos)
                        if return_click_on_btn is not None:
                            self.board.back_render()
                    elif mouse_pressed[2]:  # соответствует правой кнопке мыши
                        self.board.action_lbm = True
                        self.board.delete_tile(event.pos)
                    else:
                        self.board.action_lbm = False

                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                        if event.pos[1] < self.screen.get_height() - (self.tile.cell_size + self.tile.bottom):
                            # Если колесико вверх - увеличиваем размер сторон ячеек доски
                            self.board.cell_size += 1
                            self.focused_board()
                        else:
                            # Проверка на нахождения в видимой зоне
                            if self.tile.last_left_coorx + self.tile.cell_size + self.tile.left \
                                    < self.screen.get_width():
                                self.tile.shift_x += 10
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                        if event.pos[1] < self.screen.get_height() - (self.tile.cell_size + self.tile.bottom):
                            # Если колесико вниз - увеличиваем размер сторон ячеек доски до миниального размера = 8
                            if self.board.cell_size > 8:
                                self.board.cell_size -= 1
                            self.focused_board()
                        else:
                            # Проверка на нахождения в видимой зоне
                            if self.tile.last_right_coorx - self.tile.left > 0:
                                self.tile.shift_x -= 10

                # Делаем защиту от уязвимости (сборки координат при нажатии кнопок на клавиатуре)
                except AttributeError:
                    pass

            # Отрисовываем все объекты редактора
            self.render()

    # Метод отрисовки сцены
    def render(self) -> None:
        """
        Функция отрисовки всех элементов на экране
        :return: None
        """
        self.virtual_surface.fill((0, 0, 0))
        scaled_surface = pygame.transform.scale(self.virtual_surface, self.screen.get_size())
        self.screen.blit(scaled_surface, (0, 0))

        self.board.render(self.current_tile)
        self.tile.render(self.current_index_tile)
        self.button.render()

        for text_index in range(len(self.list_text)):
            if text_index != 1:
                self.list_text[text_index].render(self.last_coor_board, self.focus_board)
            else:
                self.list_text[text_index].render(self.board.coor_first_cell, True)

        if pygame.mouse.get_focused():
            if self.prewiew_cursor:
                if self.current_index_cursor is None:
                    pygame.mouse.set_visible(True)
                else:
                    self.cursor.prewiew(self.current_index_cursor, self.last_coordinate)
            else:
                self.update_cursor()

        self.notification.render()

        pygame.display.flip()

    # Метод сохранения уровня в файл в виде символов
    def save_board_file(self, filename) -> None:
        """
        Функция сохранения уровня в файл
        :return: None
        """
        file_path = 'data/levels/' + filename
        board = self.board.board

        # Очищаем содержимое файла для загрузки а него новой карты уровня
        with open(file_path, 'w') as file_level:
            file_level.write('')

        with open(file_path, mode='a', encoding='utf8') as file_level:
            for row in board:
                file_level.write(f'''{''.join(map(lambda x: str(x), row))}\n''')
