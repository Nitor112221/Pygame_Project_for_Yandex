import sys
import time
import pygame
import scripts.tools as tools
# from data.language import russian, english


# Главный класс, отвечающий за тайлы для рисования
class Tile:
    def __init__(self, screen):
        super().__init__()
        self.tile_group = pygame.sprite.Group()
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        self.color = pygame.Color(70, 70, 70, 255)
        self.bottom = 10
        self.left = 10
        self.cell_size = 40
        self.alpha = 128
        self.current_index = 0
        self.shift_x = 0
        self.last_left_coorx = 0

        self.tile_images = {
            '1.': tools.load_image('platform/platform.png'),
            '2.': tools.load_image('platform/platform_horizontal.png'),
            '3.': tools.load_image('platform/platform_vertical.png'),
            '4.-': tools.load_image('platform/platform.png'),
            '5.-': tools.load_image('platform/platform_horizontal.png'),
            '6.-': tools.load_image('platform/platform_vertical.png'),
            '7.': tools.load_image('disappearing_block/disappearing_block_1.png', -2),
            '8.': tools.load_image('disappearing_block/disappearing_block_2.png', -2),
            '9.': tools.load_image('disappearing_block/disappearing_block_3.png', -2),
            '10.': tools.load_image('spike/spike_classic.png')
        }

    # Метод отрисовки всех тайлов на экране
    def render(self):
        # Необхлодимо очистить группу, чтобы внести спрайы с новыми координатами и отрисовать их
        self.tile_group = pygame.sprite.Group()
        current_index = 0
        for key, value in self.tile_images.items():
            tile = pygame.sprite.Sprite(self.tile_group)
            scaled_image = pygame.transform.scale(value, (self.cell_size, self.cell_size))

            if key[-1] == '-':
                scaled_image.set_alpha(self.alpha)

            tile.image = scaled_image
            tile.rect = tile.image.get_rect()
            tile.rect.x, tile.rect.y = current_index * self.cell_size + current_index * self.left + 10 + self.shift_x, \
                self.screen_height - self.cell_size - self.bottom
            if current_index == 0:
                self.last_left_coorx = tile.rect.x
            current_index += 1

        self.tile_group.draw(self.screen)

    # Метод для проверки нажатия на тайл
    def chek_clicked(self, coords):
        current_index_tile = 0
        for sprite in self.tile_group:
            if sprite.rect.collidepoint(coords):
                self.current_index = current_index_tile
                color = pygame.Color((255, 0, 0, 255))
                pygame.draw.rect(self.screen,
                                 color,
                                 (sprite.rect[0],
                                  sprite.rect[1],
                                  sprite.rect[2],
                                  sprite.rect[3]), 2)
                return sprite, current_index_tile
            current_index_tile += 1
        return None

    # Метод возврата тайла по текущему индексу для дальнейших действий
    def return_sprite(self, index):
        count = 0
        for sprite in self.tile_group:
            if index == count:
                return sprite
            count += 1


# Главный класс, отвечающий за доску для создания и отрисовки уровня
class Board:
    def __init__(self, surface, filename, last_coordinate):
        self.surface = surface
        self.width = surface.get_width()
        self.height = surface.get_height()

        self.color = pygame.Color(70, 70, 70, 255)
        self.top = 10
        self.left = 10
        self.cell_size = 16
        self.board = [['.'] * 48 for _ in range(24)]
        self.coordinate_cell = []
        self.last_coordinate = last_coordinate
        self.stack_action = []  # тут храним стек всех добавленных координат на начало сцены

        if tools.is_file_exists(filename):
            self.board = tools.load_level(filename)
            new_board = [['.'] * len(self.board[_]) for _ in range(len(self.board))]
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    new_board[i][j] = self.board[i][j]
            self.board = new_board

        self.tile_images = {
            '1': tools.load_image('platform/platform.png'),
            '2': tools.load_image('platform/platform_horizontal.png'),
            '3': tools.load_image('platform/platform_vertical.png'),
            '4-': tools.load_image('platform/platform.png'),
            '5-': tools.load_image('platform/platform_horizontal.png'),
            '6-': tools.load_image('platform/platform_vertical.png'),
            '7': tools.load_image('disappearing_block/disappearing_block_1.png', -2),
            '8': tools.load_image('disappearing_block/disappearing_block_2.png', -2),
            '9': tools.load_image('disappearing_block/disappearing_block_3.png', -2),
            '10': tools.load_image('spike/spike_classic.png')
        }

    def set_view(self, left, top, size):
        self.top = top
        self.left = left
        self.cell_size = size

    def render(self):
        coordinate = []
        self.coordinate_cell = []
        for col in range(len(self.board)):
            for row in range(len(self.board[col])):
                self.draw_rect(self.surface,
                               self.color,
                               row * self.cell_size + self.left,
                               col * self.cell_size + self.top,
                               self.cell_size,
                               self.cell_size,
                               1)

                if self.board[col][row] != '.':
                    surface = pygame.Surface((self.cell_size - 2, self.cell_size - 2))
                    try:
                        image = self.tile_images[str(int(self.board[col][row]) + 1)]
                    except KeyError:
                        image = self.tile_images[f'{str(int(self.board[col][row]) + 1)}-']
                        image.set_alpha(180)

                    scale_image = pygame.transform.scale(image, (self.cell_size - 2, self.cell_size - 2))
                    surface.blit(scale_image, (0, 0))
                    self.surface.blit(surface, (row * self.cell_size + self.left + 1,
                                                col * self.cell_size + self.top + 1))

                coordinate.append((self.left + row * self.cell_size, self.top + col * self.cell_size))
            self.coordinate_cell.append(coordinate)
            coordinate = []

        color = pygame.Color(255, 0, 0, 255)
        for i in range(len(self.coordinate_cell)):
            for j in range(len(self.coordinate_cell[i])):
                try:
                    if self.coordinate_cell[i][j][0] < self.last_coordinate[0] < \
                            (self.coordinate_cell[i][j][0] + self.cell_size) and \
                            self.coordinate_cell[i][j][1] < self.last_coordinate[1] < \
                            (self.coordinate_cell[i][j][1] + self.cell_size) and \
                            self.last_coordinate[1] < self.height - 58:
                        self.draw_rect(self.surface,
                                       color,
                                       self.coordinate_cell[i][j][0],
                                       self.coordinate_cell[i][j][1],
                                       self.cell_size,
                                       self.cell_size,
                                       2)
                except TypeError:
                    pass

    def back_render(self):
        if len(self.stack_action) != 0:
            cur_elem_stack = self.stack_action[-1]
            color = pygame.Color((0, 0, 0))
            self.draw_rect(self.surface,
                           color,
                           cur_elem_stack[0][0],
                           cur_elem_stack[0][1],
                           self.cell_size,
                           self.cell_size,
                           1)
            self.board[cur_elem_stack[1][0]][cur_elem_stack[1][1]] = '.'
            del self.stack_action[-1]

    def clear_board(self):
        for col in range(len(self.board)):
            for row in range(len(self.board[col])):
                self.board[col][row] = '.'
        self.render()

    def delete_tile(self, coor):
        for col in range(len(self.coordinate_cell)):
            for row in range(len(self.coordinate_cell[col])):
                if self.coordinate_cell[col][row][0] < coor[0] < \
                        (self.coordinate_cell[col][row][0] + self.cell_size) and \
                        self.coordinate_cell[col][row][1] < coor[1] < \
                        (self.coordinate_cell[col][row][1] + self.cell_size) and \
                        coor[1] < self.height - 58:
                    self.board[col][row] = '.'
        self.render()

    def draw_rect(self, surface, color, coor_x, coor_y, size_x, size_y, gauge=0):
        pygame.draw.rect(surface,
                         color,
                         (coor_x,
                          coor_y,
                          size_x,
                          size_y), gauge)

    def chek_clicked_on_board(self, coor, current_tile, current_index_tile):
        for i in range(len(self.coordinate_cell)):
            for j in range(len(self.coordinate_cell[i])):
                if self.coordinate_cell[i][j][0] < coor[0] < \
                        (self.coordinate_cell[i][j][0] + self.cell_size) and \
                        self.coordinate_cell[i][j][1] < coor[1] < \
                        (self.coordinate_cell[i][j][1] + self.cell_size) and \
                        coor[1] < self.height - 58:

                    # Добавляем координаты последнего добавленного спрайта
                    push_eleme_to_stack = [(self.coordinate_cell[i][j][0],
                                             self.coordinate_cell[i][j][1]), (i, j)]
                    if push_eleme_to_stack not in self.stack_action and current_tile is not None:
                        self.stack_action.append(push_eleme_to_stack)

                    if current_tile is not None:
                        self.board[i][j] = current_index_tile

                    # print(self.coordinate_cell[i][j][0],
                    #       self.coordinate_cell[i][j][1])
                    # print(f'{(i, j)}')


# Главный класс, отвечающий за кнопки взаимодействия с пользователем
class Button:
    def __init__(self, screen):
        self.screen = screen
        self.width_screen = screen.get_width()
        self.height_screen = screen.get_height()
        self.width = 30
        self.height = 30
        self.right = 10
        self.bottom = 10
        self.coor_x = self.width_screen - self.width - self.right
        self.coor_y = self.height_screen - self.height - self.bottom
        self.group = pygame.sprite.Group()

        self.tile_images = {
            1: tools.load_image('menu_buttons/editor_back.png')
        }

    def render(self):
        for key, value in self.tile_images.items():
            btn = pygame.sprite.Sprite(self.group)
            scaled_image = pygame.transform.scale(value, (self.width, self.height))
            btn.image = scaled_image
            btn.rect = btn.image.get_rect()
            btn.rect.x, btn.rect.y = self.coor_x, self.coor_y
        self.group.draw(self.screen)

    def chek_clicked(self, coords):
        for sprite in self.group:
            if sprite.rect.collidepoint(coords):
                return sprite
        return None


# Главный класс сцены редактора уровней
class EditorScene:
    def __init__(self, screen, virtual_surface: pygame.Surface, switch_scene, settings):
        # основные характеристики сцены
        self.switch_scene = switch_scene
        self.settings = settings
        self.screen = screen
        self.virtual_surface = pygame.Surface((virtual_surface.get_width() * 0.5, virtual_surface.get_height() * 0.5))
        self.FPS = 60
        self.clock = pygame.time.Clock()

        # Текущий выбранный тайл для отрисовки
        self.current_tile = None
        # Индекс текущего выбранного тайла для отрисовки
        self.current_index_tile = None
        # Последнии координаты мыши
        self.last_coordinate = None
        # Имя файла, для сохранения уровня
        self.filename = 'level_2'
        # Инстансы классов доски, тайла, кнопки
        self.board = Board(self.screen, self.filename, self.last_coordinate)
        self.tile = Tile(self.screen)
        self.button = Button(self.screen)

        # Запускаем обработку пользовательских действий
        self.run()

    def run(self):
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

            # Обрабатываем нажатия на различные клавиши (является ли нажатой в любой кадр игры)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                running = False
                self.switch_scene('menu_scene')
            if keys[pygame.K_LEFT]:
                if self.last_coordinate is not None:
                    if self.last_coordinate[1] < self.screen.get_height() - self.tile.cell_size + self.tile.bottom:
                        self.board.left += 10
                    else:
                        self.tile.shift_x -= 10
            if keys[pygame.K_RIGHT]:
                if self.last_coordinate is not None:
                    if self.last_coordinate[1] < self.screen.get_height() - self.tile.cell_size + self.tile.bottom:
                        self.board.left -= 10
                    else:
                        self.tile.shift_x += 10
            if keys[pygame.K_DOWN]:
                self.board.top -= 10
            if keys[pygame.K_UP]:
                self.board.top += 10
                # Проверяем, были ли нажаты Ctrl + Z
            if keys[pygame.K_z] and (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]):
                # Если нажали на кнопку отмены действия и действия были накоплены - отменяем его (удаляем блок)
                self.board.back_render()
                # Делаем отмену отрисовки немного замедленной, чтобы действия были управляемые
                time.sleep(0.1)

            for event in pygame.event.get():
                # Обработка нажатий на клавиатуру (была ли нажата любой в кадр игры)
                if event.type == pygame.QUIT:
                    running = False
                    self.switch_scene(None)
                elif event.type == pygame.MOUSEMOTION:
                    self.last_coordinate = event.pos
                    self.board.last_coordinate = self.last_coordinate
                elif event.type == pygame.KEYDOWN:
                    if event.key == key_to_press:
                        self.save_board_file(self.filename)
                    elif event.key == pygame.K_BACKSPACE:
                        self.board.clear_board()
                    elif event.key == pygame.K_TAB:
                        self.current_tile = None

                # elif event.key == pygame.K_1:
                #    self.current_tile = 0
                #     self.current_index_tile = self.tile.return_sprite(self.current_tile)
                # elif event.key == pygame.K_2:
                #     self.current_tile = 1
                #     self.current_index_tile = self.tile.return_sprite(self.current_tile)
                # elif event.key == pygame.K_3:
                #     self.current_tile = 2
                #     self.current_index_tile = self.tile.return_sprite(self.current_tile)
                # elif event.key == pygame.K_4:
                #     self.current_tile = 3
                #     self.current_index_tile = self.tile.return_sprite(self.current_tile)
                # elif event.key == pygame.K_5:
                #     self.current_tile = 4
                #     self.current_index_tile = self.tile.return_sprite(self.current_tile)
                # elif event.key == pygame.K_6:
                #     self.current_tile = 5
                #     self.current_index_tile = self.tile.return_sprite(self.current_tile)
                # elif event.key == pygame.K_7:
                #     self.current_tile = 6
                #     self.current_index_tile = self.tile.return_sprite(self.current_tile)
                # elif event.key == pygame.K_8:
                #     self.current_tile = 7
                #     self.current_index_tile = self.tile.return_sprite(self.current_tile)
                # elif event.key == pygame.K_9:
                #     self.current_tile = 8
                #     self.current_index_tile = self.tile.return_sprite(self.current_tile)
                # elif event.key == pygame.K_0:
                #     self.current_tile = 9
                #     self.current_index_tile = self.tile.return_sprite(self.current_tile)

                # Обработка нажатий на мышь
                mouse_pressed = pygame.mouse.get_pressed()
                try:
                    if mouse_pressed[0]:  # соответствует левой кнопке мыши
                        # Меняем выбранный тайл на новый, если нажали на него
                        return_click_on_tile = self.tile.chek_clicked(event.pos)
                        if return_click_on_tile is not None:
                            self.current_tile = return_click_on_tile[0]
                            self.current_index_tile = return_click_on_tile[1]
                        self.board.chek_clicked_on_board(event.pos, self.current_tile, self.current_index_tile)

                        # Если нажали на кнопку отмены действия и действия были накоплены - отменяем его
                        return_click_on_btn = self.button.chek_clicked(event.pos)
                        if return_click_on_btn is not None:
                            self.board.back_render()

                    elif mouse_pressed[2]:  # соответствует правой кнопке мыши
                        self.board.delete_tile(event.pos)

                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                        if event.pos[1] < self.screen.get_height() - (self.tile.cell_size + self.tile.bottom):
                            # Если колесико вверх - увеличиваем размер сторон ячеек доски
                            self.board.cell_size += 1
                        else:
                            # Проверка на нахождения в видимой зоне
                            if self.tile.last_left_coorx + self.tile.cell_size + self.tile.left \
                                    < self.screen.get_width():
                                self.tile.shift_x += 10

                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                        if event.pos[1] < self.screen.get_height() - self.tile.cell_size + self.tile.bottom:
                            # Если колесико вниз - увеличиваем размер сторон ячеек доски до миниального размера = 8
                            if self.board.cell_size > 8:
                                self.board.cell_size -= 1
                        else:
                            # Проверка на нахождения в видимой зоне
                            if self.tile.last_left_coorx - self.tile.left > 0:
                                self.tile.shift_x -= 10

                # Делаем защиту от уязвимости (сборки координат при нажатии кнопок на клавиатуре)
                except AttributeError:
                    pass

            # Отрисовываем все объекты редактора
            self.render()
            self.board.render()
            self.tile.render()
            self.button.render()
            pygame.display.flip()
            self.clock.tick(self.FPS)

    # Метод отрисовки сцены
    def render(self):
        self.virtual_surface.fill((0, 0, 0))
        scaled_surface = pygame.transform.scale(self.virtual_surface, self.screen.get_size())
        self.screen.blit(scaled_surface, (0, 0))

    # Метод сохранения уровня в файл в виде символов
    def save_board_file(self, filename):
        file_path = 'data/levels/' + filename
        board = self.board.board

        # Очищаем содержимое файла для загрузки а него новой карты уровня
        with open(file_path, 'w') as file_level:
            file_level.write('')

        with open(file_path, mode='a', encoding='utf8') as file_level:
            for row in board:
                file_level.write(f'''{''.join(map(lambda x: str(x), row))}\n''')
