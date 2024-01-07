import pygame
import scripts.tools as tools
from data.language import russian, english

# Инициализация Pygame
pygame.init()


class Board:
    def __init__(self, width, hight, cell_size, top_shift, left_shift):
        self.width = width
        self.hight = hight
        self.top = top_shift
        self.left = left_shift
        self.size = cell_size

        self.board = [[0] * width for _ in range(hight)]

    def set_view(self, left, top, size):
        self.top = top
        self.left = left
        self.size = size

    def render(self, screen):
        for row in range(self.width):
            for col in range(self.hight):
                pygame.draw.rect(screen, (80, 80, 80), (row * self.size + self.left, col * self.size + self.top,
                                                   self.size, self.size), 1)


class Blocks:
    def __init__(self, width_surface, width, hight, cell_size, top_shift, left_shift):
        self.width_surface = width_surface
        self.width = width
        self.hight = hight
        self.top = top_shift
        self.left = left_shift
        self.size = cell_size

    def render(self, screen, image_list, group):
        list_coor = []
        list_rect = []
        for row in range(self.width):
            for col in range(len(image_list)):
                block = pygame.sprite.Sprite()
                block.image = image_list[col]
                block.image = pygame.transform.scale(block.image, (self.size, self.size))

                block.rect = block.image.get_rect()
                group.add(block)
                block.rect.x, block.rect.y = self.size * col + 10 * col + 10, screen.get_height() - self.size - 10
                list_coor.append((block.rect.x, block.rect.y))
                list_rect.append(block.rect)
        group.draw(screen)
        return list_coor, list_rect


list_coor_b, list_rect_b = [], []

class Editor:
    def __init__(self, surface):
        global list_coor_b, list_rect_b
        surface_w = surface.get_width()
        surface_h = surface.get_height()

        all_sprites = pygame.sprite.Group()
        tiles_group = pygame.sprite.Group()
        player_group = pygame.sprite.Group()

        # Загрузка спрайтов-блоков для создания уровня
        block_1 = tools.load_image('disappearing_block/disappearing_block_1.png')
        block_2 = tools.load_image('disappearing_block/disappearing_block_2.png')
        block_3 = tools.load_image('disappearing_block/disappearing_block_3.png')

        platform = tools.load_image('platform/platform.png')
        platform_h = tools.load_image('platform/platform_horizontal.png')
        platform_w = tools.load_image('platform/platform_vertical.png')

        spike_block = tools.load_image('spike/spike_classic.png')

        list_sprites = []
        list_sprites.extend([block_1, block_2, block_3, platform, platform_h, platform_w, spike_block])

        cell_size_block = 50
        top_shift = 20
        left_shift = 20
        rows = 1
        cols = surface_w // cell_size_block
        block = Blocks(surface_w, rows, cols, cell_size_block, top_shift, left_shift)

        # Получаем координаты и все прямоугольники блоков
        list_coor_b, list_rect_b = block.render(surface, list_sprites, tiles_group)

        # Определяем размеры клеток и сетки для редактора карт:
        top_shift = 20
        left_shift = 20
        cell_size = 32
        rows = surface_w // cell_size - left_shift // cell_size - 1
        cols = surface_h // cell_size - (top_shift + 100) // cell_size - 1
        map_data = [[' ' for _ in range(cols)] for _ in range(rows)]

        board = Board(rows, cols, cell_size, top_shift, left_shift)
        board.render(surface)


chek_button = False


class EditorScene:
    def __init__(self, width: int, height: int, settings: dict):
        self.width, self.height = round(width * 1), round(height * 1)
        self.settings = settings
        self.options = list(settings.items())
        self.options.pop(0)  # Используем ключи словаря settings как опции
        self.current_shift = 0

    def draw(self, surface: pygame.Surface):  # Метод отрисовки меню изменения настроек
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

        if self.settings['Language'] == 'Русский':
            text = font.render('Назад: Esc', True, interface_color)
        else:
            text = font.render('Back: Esc', True, interface_color)
        # surface.blit(text, (surface.get_width() * 0.01 + 10, surface.get_height() * 0.01 + 10))

        surface.fill((0, 0, 0))
        Editor(surface)

    def handle_event(self, event, virtual_surface, screen):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                tools.save_user_options(self.settings)  # Сохранение настроек
                return 'Close'

        elif event.type == pygame.MOUSEWHEEL:
            self.current_shift += event.y * 15

    def circuit(self, surface):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                counter = 0
                for rect in list_rect_b:
                    if rect.collidepoint(event.pos):
                        print(counter)
                    counter += 1
                counter = 0
