import pygame
import scripts.tools as tools
from scripts.scenes.map_editor.convert_index import ConvertTile


# Главный класс, отвечающий за доску для создания и отрисовки уровня
class Board:
    def __init__(self, surface, filename, last_coordinate):
        self.surface = surface
        self.width = surface.get_width()
        self.height = surface.get_height()
        self.convert_tile = ConvertTile()

        self.color = pygame.Color(70, 70, 70, 255)
        self.color_rect = pygame.Color(0, 0, 0, 255)
        self.top = 10
        self.left = 10
        self.cell_size = 16
        self.board = [['.'] * 48 for _ in range(24)]
        self.coordinate_cell = []
        self.last_coordinate = last_coordinate
        self.coor_first_cell = [0, 0]
        self.last_coor_board = [0, 0]
        self.stack_action = []  # тут храним стек всех добавленных координат на начало сцены
        self.action_lbm = False

        if tools.is_file_exists(filename, 'data/levels/'):
            self.board = tools.load_level(filename)
            new_board = [['.'] * len(self.board[_]) for _ in range(len(self.board))]
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    new_board[i][j] = self.board[i][j]
            self.board = new_board

    def set_view(self, left, top, size):
        self.top = top
        self.left = left
        self.cell_size = size

    def render(self, current_tile=None):
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
                if col == 0 and row == 0:
                    self.coor_first_cell = [row * self.cell_size + self.left, col * self.cell_size + self.top]

                if self.board[col][row] != '.':
                    surface = pygame.Surface((self.cell_size - 2, self.cell_size - 2))
                    try:
                        image = self.convert_tile.tile_images[
                            str(self.convert_tile.return_index(self.board[col][row]) + 1)
                        ][0]
                    except KeyError:
                        image = self.convert_tile.tile_images[
                            f'{self.convert_tile.return_index(self.board[col][row]) + 1}-'
                        ][0]
                        image.set_alpha(180)

                    scale_image = pygame.transform.scale(image, (self.cell_size - 2, self.cell_size - 2))
                    surface.blit(scale_image, (0, 0))
                    self.surface.blit(surface, (row * self.cell_size + self.left + 1,
                                                col * self.cell_size + self.top + 1))

                coordinate.append((self.left + row * self.cell_size, self.top + col * self.cell_size))
            self.coordinate_cell.append(coordinate)
            coordinate = []

        if self.action_lbm:
            self.color_rect = pygame.Color(255, 255, 255, 255)
        elif current_tile is None:
            self.color_rect = pygame.Color(255, 0, 0, 255)
        else:
            self.color_rect = pygame.Color(0, 214, 27, 255)
        for i in range(len(self.coordinate_cell)):
            for j in range(len(self.coordinate_cell[i])):
                try:
                    if self.coordinate_cell[i][j][0] < self.last_coordinate[0] < \
                            (self.coordinate_cell[i][j][0] + self.cell_size) and \
                            self.coordinate_cell[i][j][1] < self.last_coordinate[1] < \
                            (self.coordinate_cell[i][j][1] + self.cell_size) and \
                            self.last_coordinate[1] < self.height - 58:
                        self.draw_rect(self.surface,
                                       self.color_rect,
                                       self.coordinate_cell[i][j][0],
                                       self.coordinate_cell[i][j][1],
                                       self.cell_size,
                                       self.cell_size,
                                       2)

                        self.last_coor_board = (i, j)

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

    def chek_clicked_on_board(self, coor, current_tile=None, current_index_tile=None):
        for i in range(len(self.coordinate_cell)):
            for j in range(len(self.coordinate_cell[i])):
                # Если вызвали метод для отрисовки тайла
                if current_tile is not None and current_index_tile is not None:
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
                                self.board[i][j] = self.convert_tile.return_symbol(current_index_tile)

                # Если нужно просто проверить нахождении мыши внутри доски
                else:
                    if self.coordinate_cell[i][j][0] <= coor[0] <= \
                            (self.coordinate_cell[i][j][0] + self.cell_size) and \
                            self.coordinate_cell[i][j][1] <= coor[1] <= \
                            (self.coordinate_cell[i][j][1] + self.cell_size) and \
                            coor[1] <= self.height - 58:
                        return True

                    # Важные строки для определения кординат :)
                    # Обычно, использовались в отладке, возможно пригодятся при дальнейшем развитии проекта

                    # print(self.coordinate_cell[i][j][0],
                    #       self.coordinate_cell[i][j][1])
                    # print(f'{(i, j)}')
