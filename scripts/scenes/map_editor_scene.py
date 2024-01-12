import pygame
import scripts.tools as tools
from data.language import russian, english


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
        self.sell_size = 40
        self.alpha = 128

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

        current_index = 0
        for key, value in self.tile_images.items():
            tile = pygame.sprite.Sprite(self.tile_group)
            scaled_image = pygame.transform.scale(value, (self.sell_size, self.sell_size))
            # Проверкак на неосязаемость блока

            if key[-1] == '-':
                scaled_image.set_alpha(self.alpha)

            tile.image = scaled_image
            tile.rect = tile.image.get_rect()
            tile.rect.x, tile.rect.y = current_index * self.sell_size + current_index * self.left + 10, \
                self.screen_height - self.sell_size - self.bottom
            current_index += 1

        self.tile_group.draw(self.screen)

    def chek_clicked(self, coords):
        current_index = 0
        for sprite in self.tile_group:
            if sprite.rect.collidepoint(coords):
                return sprite, current_index
            current_index += 1
        return None

    # Добавьте метод для изменения типа тайла
    def change_tile_type(self):
        pass
        # Здесь может быть логика изменения изображения в зависимости от нового типа


class Board:
    def __init__(self, surface):
        self.surface = surface
        self.width = surface.get_width()
        self.height = surface.get_height()

        self.color = pygame.Color(70, 70, 70, 255)
        self.top = 10
        self.left = 10
        self.cell_size = 16
        self.board = [['.'] * 48 for _ in range(24)]
        self.coordinate_cell = []

        filename = ''
        if tools.is_file_exists(filename):
            self.board = tools.load_level(filename)

        self.tile_images = {
            '1': tools.load_image('platform/platform.png'),
            '2': tools.load_image('platform/platform_horizontal.png'),
            '3': tools.load_image('platform/platform_vertical.png'),
            '4': tools.load_image('platform/platform.png'),
            '5': tools.load_image('platform/platform_horizontal.png'),
            '6': tools.load_image('platform/platform_vertical.png'),
            '7': tools.load_image('disappearing_block/disappearing_block_1.png', -2),
            '8': tools.load_image('disappearing_block/disappearing_block_2.png', -2),
            '9': tools.load_image('disappearing_block/disappearing_block_3.png', -2),
            '10': tools.load_image('spike/spike_classic.png')
        }

    def set_view(self, left, top, size):
        self.top = top
        self.left = left
        self.cell_size = size

    def draw(self):
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
                    image = self.tile_images[str(self.board[col][row] + 1)]
                    scale_image = pygame.transform.scale(image, (self.cell_size - 2, self.cell_size - 2))
                    surface.blit(scale_image, (0, 0))
                    self.surface.blit(surface, (row * self.cell_size + self.left + 1,
                                                col * self.cell_size + self.top + 1))

                coordinate.append((self.left + row * self.cell_size, self.top + col * self.cell_size))
            self.coordinate_cell.append(coordinate)
            coordinate = []

    def draw_rect(self, surface, color, coor_x, coor_y, size_x, size_y, gauge):
        pygame.draw.rect(surface,
                         color,
                         (coor_x,
                          coor_y,
                          size_x,
                          size_y), gauge)

    def chek_clicked_on_board(self, coor, current_tile, id_):
        for i in range(len(self.coordinate_cell)):
            for j in range(len(self.coordinate_cell[i])):
                if self.coordinate_cell[i][j][0] < coor[0] < \
                        (self.coordinate_cell[i][j][0] + self.cell_size) and \
                        self.coordinate_cell[i][j][1] < coor[1] < \
                        (self.coordinate_cell[i][j][1] + self.cell_size) and \
                        coor[1] < self.height - 58:

                    if current_tile is not None:
                        self.board[i][j] = id_

                    # print(self.coordinate_cell[i][j][0],
                    #       self.coordinate_cell[i][j][1])
                    # print(f'{(i, j)}')


class EditorScene:
    def __init__(self, screen, virtual_surface: pygame.Surface, switch_scene, settings):
        self.screen = screen
        self.virtual_surface = pygame.Surface((virtual_surface.get_width() * 0.5, virtual_surface.get_height() * 0.5))
        self.switch_scene = switch_scene
        self.settings = settings
        self.current_tile = None
        self.id_ = None
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.run()

    def run(self):
        running = True
        board = Board(self.screen)
        tile = Tile(self.screen)
        while running:

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                running = False
                self.switch_scene('menu_scene')
            if keys[pygame.K_LEFT]:
                board.left -= 10
            if keys[pygame.K_RIGHT]:
                board.left += 10
            if keys[pygame.K_DOWN]:
                board.top += 10
            if keys[pygame.K_UP]:
                board.top -= 10

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.switch_scene(None)

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Меняем выбранный тайл на новый, если нажали на него
                    return_click = tile.chek_clicked(event.pos)
                    if return_click is not None:
                        self.current_tile = return_click[0]
                        self.id_ = return_click[1]
                    board.chek_clicked_on_board(event.pos, self.current_tile, self.id_)

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                    # Если колесико вверх - увеличиваем размер сторон ячеек доски
                    board.cell_size += 1
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                    # Если колесико вниз - увеличиваем размер сторон ячеек доски до миниального размера = 8
                    if board.cell_size > 16:
                        board.cell_size -= 1

            self.render()
            board.draw()
            Tile(self.screen)
            pygame.display.flip()
            self.clock.tick(self.fps)

    def render(self):
        self.virtual_surface.fill((0, 0, 0))

        scaled_surface = pygame.transform.scale(self.virtual_surface, self.screen.get_size())
        self.screen.blit(scaled_surface, (0, 0))
