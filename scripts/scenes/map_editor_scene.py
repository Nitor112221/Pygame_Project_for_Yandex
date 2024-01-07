import pygame
import scripts.tools as tools
from data.language import russian, english

# Инициализация Pygame
pygame.init()

# Определяем глобальные переменные для взаимодействия с доской
list_coor_board, list_rect_board = [], []  # Списки координат и прямоугольников ячеек
on_board_sprites = pygame.sprite.Group()  # Группа спрайтов для ячеек
circuit_sprites = pygame.sprite.Group()  # Группа спрайтов для выделителей

list_coor_b, list_rect_b = [], []  # Списки координат и прямоугольников блоков
list_sprites = []  # Список спрайтов всех блоков

block_selected = False
index_selected_sprite = 0


# Класс доски для создания уровня
class Board:
    # Инициализация основных переменных
    def __init__(self, width, hight, cell_size, top_shift, left_shift):
        self.width = width
        self.hight = hight
        self.top = top_shift
        self.left = left_shift
        self.size = cell_size
        self.board = [[0] * width for _ in range(hight)]

    # Метод изменения основных переменных
    def set_view(self, width, hight, left, top, cell_size):
        self.width = width
        self.hight = hight
        self.top = top
        self.left = left
        self.size = cell_size

    # Метод отрисовки ячеек доски
    def render(self, screen):
        global list_coor_board, list_rect_board
        list_coor_board, list_rect_board = [], []
        for row in range(self.width):
            for col in range(self.hight):
                coor_x = row * self.size + self.left
                coor_y = col * self.size + self.top
                rect_board = pygame.Rect((coor_x,
                                          coor_y,
                                          self.size,
                                          self.size))
                list_rect_board.append(rect_board)
                list_coor_board.append((coor_x, coor_y))
                pygame.draw.rect(screen, (80, 80, 80), rect_board, 1)


# Класс блоков, из которых будет строиться уровень
class Blocks:
    # Инициализация основных переменных
    def __init__(self, width_surface, width, hight, cell_size, top_shift, left_shift):
        self.width_surface = width_surface
        self.width = width
        self.hight = hight
        self.top = top_shift
        self.left = left_shift
        self.size = cell_size

    # Метод изменения основных переменных
    def set_view(self, width, hight, left, top, cell_size):
        self.width = width
        self.hight = hight
        self.top = top
        self.left = left
        self.size = cell_size

    # Метод отрисовки блоков для выбора
    def render(self, screen, image_list, group):
        list_coor = []
        list_rect = []
        for row in range(self.width):
            for col in range(len(image_list)):
                block = pygame.sprite.Sprite()
                block.image = image_list[col]
                block.image = pygame.transform.scale(block.image,
                                                     (self.size, self.size))
                block.rect = block.image.get_rect()
                group.add(block)
                block.rect.x = self.size * col + 10 * col + 10
                block.rect.y = screen.get_height() - self.size - 10
                list_coor.append((block.rect.x, block.rect.y))
                list_rect.append(block.rect)
        group.draw(screen)
        return list_coor, list_rect


# Главный класс опеределения спрайтов и создания экземпляров лоски и блоков
class Editor:
    def __init__(self, surface):
        # Во время инициализации создаются экземпляры клаасов и отрисовываются доска и блоки
        global list_coor_b, list_rect_b, list_sprites
        surface_w = surface.get_width()
        surface_h = surface.get_height()

        tiles_group = pygame.sprite.Group()  # Группа спрайтов для блоков

        # Загрузка спрайтов-блоков для создания уровня
        block_1 = tools.load_image('disappearing_block/disappearing_block_1.png')
        block_2 = tools.load_image('disappearing_block/disappearing_block_2.png')
        block_3 = tools.load_image('disappearing_block/disappearing_block_3.png')
        platform = tools.load_image('platform/platform.png')
        platform_h = tools.load_image('platform/platform_horizontal.png')
        platform_w = tools.load_image('platform/platform_vertical.png')
        spike_block = tools.load_image('spike/spike_classic.png')

        # Список прайтов всех изображений блоков
        list_sprites = []
        list_sprites.extend([block_1, block_2, block_3, platform, platform_h, platform_w, spike_block])

        # Определяем параметры для создания блоков
        cell_size_block = 50
        top_shift = 20
        left_shift = 20
        rows = 1
        cols = surface_w // cell_size_block

        # Отрисовываем блоки
        block = Blocks(surface_w, rows, cols, cell_size_block, top_shift, left_shift)
        # Получаем координаты и все прямоугольники блоков и рисуем блоки
        list_coor_b, list_rect_b = block.render(surface, list_sprites, tiles_group)

        # Определяем параметры для создания доски
        top_shift = 20
        left_shift = 20
        cell_size = 16
        rows = surface_w // cell_size - left_shift // cell_size - 1
        cols = surface_h // cell_size - (top_shift + 100) // cell_size - 1

        # Тут хранится вся доска в виде пробелов и соответстует размерам основной доски
        map_data = [[' ' for _ in range(cols)] for _ in range(rows)]

        # Отрисовываем доску
        board = Board(rows, cols, cell_size, top_shift, left_shift)
        board.render(surface)


# Класс сцены создания рдактора уровней
class EditorScene:
    # Инициализация основных переменных
    def __init__(self, width: int, height: int, settings: dict):
        self.width, self.height = round(width * 1), round(height * 1)
        self.settings = settings
        self.options = list(settings.items())
        self.options.pop(0)  # Используем ключи словаря settings как опции
        self.current_shift = 0

    # Метод отрисовки меню изменения настроек
    def draw(self, surface: pygame.Surface):
        background_scene = pygame.Surface((self.width, self.height))
        background_scene.fill(pygame.Color('black'))  # Заполнение поверхности белым цветом
        background_scene.set_alpha(50)
        surface.blit(background_scene, (0, 0))
        if self.settings['Language'] == 'English':
            lang = english.eng
        elif self.settings['Language'] == 'Русский':
            lang = russian.rus
        settings_scene = pygame.Surface((self.width, self.height))
        settings_scene.fill((255, 255, 255))
        settings_scene.set_colorkey((255, 255, 255))

        font = pygame.font.SysFont('Comic Sans MS', 36)
        interface_color = pygame.Color((255, 255, 255))

        # Отрисовка подсказки кнопки выхода (в последствии блок кода может быть уничножен)
        # Пока находится в режиме ожидания
        if self.settings['Language'] == 'Русский':
            text = font.render('Назад: Esc', True, interface_color)
        else:
            text = font.render('Back: Esc', True, interface_color)
        # surface.blit(text, (surface.get_width() * 0.01 + 10, surface.get_height() * 0.01 + 10))

        # Отрисовываем все элементы редактора
        surface.fill((0, 0, 0))
        Editor(surface)

    def handle_event(self, event, virtual_surface, screen):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                tools.save_user_options(self.settings)  # Сохранение настроек
                return 'Close'

        elif event.type == pygame.MOUSEWHEEL:
            self.current_shift += event.y * 15

    # Обработка взаимодействий редактора с создателем уровня
    def draw_element(self, surface):
        global block_selected, index_selected_sprite, circuit_sprites
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Если блок еще не был выбран:
                if not block_selected:
                    counter = 0
                    for rect in list_rect_b:
                        if rect.collidepoint(event.pos):
                            # Получаем индекс выбранного блока
                            index_selected_sprite = counter
                            block_selected = True

                            # Отрисовываем выделитель выбранного блока
                            circuit_sprites = pygame.sprite.Group()
                            circuit = pygame.sprite.Sprite()
                            circuit.image = pygame.Surface((rect.width // 4, rect.height // 4))
                            pygame.draw.rect(circuit.image, (0, 255, 0),
                                             (0, 0, rect.width // 4, rect.height // 4))
                            circuit.rect = circuit.image.get_rect()
                            circuit_sprites.add(circuit)
                            circuit.rect.x, circuit.rect.y = rect.x, rect.y

                        counter += 1

                elif block_selected:
                    for elem in list_rect_board:
                        if elem.collidepoint(event.pos):

                            # Отрисовываем выбранный блок на доске
                            arrow = pygame.sprite.Sprite()
                            image = list_sprites[index_selected_sprite]
                            scaled_image = pygame.transform.scale(image, (elem.width, elem.height))
                            arrow.image = scaled_image
                            arrow.rect = arrow.image.get_rect()
                            on_board_sprites.add(arrow)
                            arrow.rect.x, arrow.rect.y = elem.x, elem.y

                        else:
                            for rect in list_rect_b:
                                if rect.collidepoint(event.pos):
                                    block_selected = False

        on_board_sprites.draw(surface)
        circuit_sprites.draw(surface)
