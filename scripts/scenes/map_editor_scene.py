import pygame
import scripts.tools as tools
from data.language import russian, english


class Tile:
    def __init__(self, screen, all_sprites):
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
            '1': tools.load_image('platform/platform.png'),
            '2': tools.load_image('platform/platform_horizontal.png'),
            '3': tools.load_image('platform/platform_vertical.png'),
            '4-': tools.load_image('platform/platform.png'),
            '5-': tools.load_image('platform/platform_horizontal.png'),
            '6-': tools.load_image('platform/platform_vertical.png'),
            '7': tools.load_image('disappearing_block/disappearing_block_1.png', -2),
            '8': tools.load_image('disappearing_block/disappearing_block_2.png', -2),
            '9': tools.load_image('disappearing_block/disappearing_block_3.png', -2),
            's': tools.load_image('spike/spike_classic.png')
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

    def chek_clicked_on_board(self, coords):
        current_index = 0
        for sprite in self.tile_group:
            if sprite.rect.collidepoint(coords):
                return sprite
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

    def chek_clicked_on_board(self, coor, current_tile, group_tile_on_board):
        for i in range(len(self.coordinate_cell)):
            for j in range(len(self.coordinate_cell[i])):
                if self.coordinate_cell[i][j][0] < coor[0] < \
                        (self.coordinate_cell[i][j][0] + self.cell_size) and \
                        self.coordinate_cell[i][j][1] < coor[1] < \
                        (self.coordinate_cell[i][j][1] + self.cell_size) and \
                        coor[1] < self.height - 58:

                    if current_tile is not None:
                        scale_image = pygame.transform.scale(current_tile.image, (self.cell_size, self.cell_size))

                        clone_current_tile = pygame.sprite.Sprite()
                        clone_current_tile.image = scale_image
                        clone_current_tile.rect = clone_current_tile.image.get_rect()
                        clone_current_tile.rect.x = self.coordinate_cell[i][j][0]
                        clone_current_tile.rect.y = self.coordinate_cell[i][j][1]
                        group_tile_on_board.add(clone_current_tile)

                    print(self.coordinate_cell[i][j][0],
                          self.coordinate_cell[i][j][1])
                    print(f'{(i, j)}')


class EditorScene:
    def __init__(self, screen, virtual_surface: pygame.Surface, switch_scene, settings):
        self.screen = screen
        self.virtual_surface = pygame.Surface((virtual_surface.get_width() * 0.5, virtual_surface.get_height() * 0.5))
        self.switch_scene = switch_scene
        self.settings = settings
        self.current_tile = None

        self.group_tile_on_board = pygame.sprite.Group()

        # self.map_screen = pygame.Surface((virtual_surface.get_width() * 0.8, virtual_surface.get_height() * 0.6))

        self.all_sprites = pygame.sprite.Group()
        self.scroll_x = 0
        self.scroll_y = 0
        self.scroll_x_speed = 0
        self.scroll_y_speed = 0

        self.zoom = 2

        self.dragging = False
        self.start_pos = (0, 0)

        self.fps = 60
        self.clock = pygame.time.Clock()
        self.run()

    def transport_position_group_sprite(self, value='+', measurement='x'):
        for sprite in self.group_tile_on_board:
            if measurement == 'x':
                if value == '-':
                    sprite.rect.move(-10, 0)
                elif value == '+':
                    sprite.rect.move(10, 0)
            if measurement == 'y':
                if value == '-':
                    sprite.rect.move(0, -10)
                elif value == '+':
                    sprite.rect.move(0, 10)

    def run(self):
        running = True
        board = Board(self.screen)
        tile = Tile(self.screen, self.all_sprites)
        # (mouse_pos[0] + self.scroll_x) / self.zoom,
        # (mouse_pos[1] + self.scroll_y) / self.zoom,
        while running:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                running = False
                self.switch_scene('menu_scene')
            if keys[pygame.K_LEFT]:
                self.scroll_x_speed -= 10
                board.left -= 10
                self.transport_position_group_sprite()
            if keys[pygame.K_RIGHT]:
                self.scroll_x_speed += 10
                board.left += 10
                self.transport_position_group_sprite('-', 'x')
            if keys[pygame.K_DOWN]:
                self.scroll_y_speed += 10
                board.top += 10
                self.transport_position_group_sprite('+', 'y')
            if keys[pygame.K_UP]:
                self.scroll_y_speed -= 10
                board.top -= 10
                self.transport_position_group_sprite('-', 'y')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.switch_scene(None)
                elif event.type == pygame.MOUSEWHEEL:
                    self.zoom += event.y * 0.2
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Меняем выбранный тайл на новый, если нажали на него
                    return_click = tile.chek_clicked_on_board(event.pos)
                    if return_click is not None:
                        self.current_tile = return_click
                    board.chek_clicked_on_board(event.pos, self.current_tile, self.group_tile_on_board)

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    self.remove_tile()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                    self.change_current_tile_type()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                    self.change_current_tile_type(forward=True)
                    # Если колесико вверх - увеличиваем размер сторон ячеек доски
                    board.cell_size += 1
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                    self.change_current_tile_type(forward=False)
                    # Если колесико вниз - увеличиваем размер сторон ячеек доски до миниального размера = 8
                    if board.cell_size > 8:
                        board.cell_size -= 1
                elif event.type == pygame.KEYUP:  # заканчиваем движение
                    if event.key == pygame.K_LEFT:
                        self.scroll_x_speed += 10
                    if event.key == pygame.K_RIGHT:
                        self.scroll_x_speed -= 10
                    if event.key == pygame.K_DOWN:
                        self.scroll_y_speed -= 10
                    if event.key == pygame.K_UP:
                        self.scroll_y_speed += 10

            self.mouse_interaction()
            self.update()
            self.render()
            board.draw()
            self.group_tile_on_board.draw(self.screen)
            Tile(self.screen, self.all_sprites)

            pygame.display.flip()
            self.clock.tick(self.fps)

    def mouse_interaction(self):
        mouse_pos = pygame.mouse.get_pos()
        self.scroll_x += self.scroll_x_speed * self.zoom
        self.scroll_y += self.scroll_y_speed * self.zoom

        if self.dragging:
            # Обновляем смещение при перемещении мышью
            current_pos = pygame.mouse.get_pos()
            self.scroll_x += self.start_pos[0] - current_pos[0]
            self.scroll_y += self.start_pos[1] - current_pos[1]
            self.start_pos = current_pos

        # Ограничиваем смещение, чтобы не выходить за пределы карты
        max_scroll_x = (self.virtual_surface.get_width() * self.zoom - self.screen.get_width()) // 2
        max_scroll_y = (self.virtual_surface.get_height() * self.zoom - self.screen.get_height()) // 2

        self.scroll_x = max(-max_scroll_x, min(max_scroll_x, self.scroll_x))
        self.scroll_y = max(-max_scroll_y, min(max_scroll_y, self.scroll_y))

    def update(self):
        pass

    def render(self):
        self.virtual_surface.fill((0, 0, 0))
        self.zoom = max(2, min(self.zoom, 3.5))

        scaled_surface = pygame.transform.scale(self.virtual_surface, self.screen.get_size())
        self.screen.blit(scaled_surface, (0, 0))

    def add_tile(self):
        mouse_pos = pygame.mouse.get_pos()

    def remove_tile(self):
        pass
        # mouse_pos = pygame.mouse.get_pos()
        #  clicked_sprites = [s for s in self.tile_group if s.rect.collidepoint(mouse_pos)]
        # for sprite in clicked_sprites:
        #     sprite.kill()

    def change_current_tile_type(self, forward=True):
        # Метод для смены текущего типа тайла
        # forward=True - перейти к следующему типу, forward=False - перейти к предыдущему типу
        # Вам нужно реализовать логику смены типов тайлов в зависимости от ваших требований
        pass
