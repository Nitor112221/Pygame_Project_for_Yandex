import pygame
import os
import sys
import time

pygame.init()


def load_image(name: str, colorkey=None, reverse=False) -> pygame.Surface:  # функция загрузки изображения
    """
    Функция загрузки изображения
    :param name: str
    :param colorkey: int or None
    :param reverse bool
    :return: pygame.Surface
    """
    # Полный путь к изображению
    fullname = os.path.join('data/images', name)

    # Проверка существования файла
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    # Загрузка изображения
    image = pygame.image.load(fullname).convert_alpha()

    # Применение цветового ключа для прозрачности, если указано
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:  # цвет для прозрачности левого верхнего угла
            colorkey = image.get_at((0, 0))
        elif colorkey == -2:  # цвет для прозрачности левого нижнего угла
            colorkey = image.get_at((0, image.get_height() - 1))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    if reverse:
        return pygame.transform.flip(image, True, False)

    return image


# функция инициализации тайлов, для последующей работы с ними
def tile_init():
    global tile_images, tile_width, tile_height
    # словарь для работы с изображениями тайлов
    tile_images = {
        'platform': load_image('platform/platform.png'),
        'platform_horizontal': load_image('platform/platform_horizontal.png'),
        'platform_vertical': load_image('platform/platform_vertical.png'),
        'disappearing_block1': load_image('disappearing_block/disappearing_block_1.png', -2),
        'disappearing_block2': load_image('disappearing_block/disappearing_block_2.png', -2),
        'disappearing_block3': load_image('disappearing_block/disappearing_block_3.png', -2),
        'spike': load_image('spike/spike_classic.png'),
        'dirt': load_image('dirt/dirt.png'),
        'dirtu': load_image('dirt/dirt_up.png'),
        'dirth': load_image('dirt/dirt_down.png'),
        'dirtl': load_image('dirt/dirt_left.png'),
        'dirtr': load_image('dirt/dirt_right.png'),
        'dirtq': load_image('dirt/dirt_up_left.png'),
        'dirtw': load_image('dirt/dirt_down_left.png'),
        'dirte': load_image('dirt/dirt_up_right.png'),
        'dirtt': load_image('dirt/dirt_down_right.png')
    }

    tile_width = tile_height = 8  # размеры 1 тайла


# класс описывающий тайл и его логику
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, *groups, is_touchable=True):
        self.tile_type = tile_type
        self.is_touchable = is_touchable
        super().__init__(*groups)
        if tile_type is not None:
            self.image = tile_images[tile_type].copy()
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)
            if 'disappearing_block' in tile_type:  # если блок падающий, то добавляем ему доп параметры
                self.disappearing_time = None
                self.original_image = tile_images[tile_type].copy()  # Исходное изображение блока
                if '1' in tile_type:
                    self.dotted_line = load_image('disappearing_block/dotted_line_1.png')
                elif '2' in tile_type:
                    self.dotted_line = load_image('disappearing_block/dotted_line_2.png')
                elif '3' in tile_type:
                    self.dotted_line = load_image('disappearing_block/dotted_line_3.png')
        else:  # создание ориентировочного тайла, нужного для ориентации камеры
            self.image = tile_images['platform'].copy()
            self.rect = pygame.Rect(0, 0, 0, 0).move(
                tile_width * pos_x, tile_height * pos_y)

    def update(self, player):
        # метод, который добавляет разным блокам уникальное поведение (пока что есть только исчезающие блоки)
        if 'disappearing_block' in self.tile_type:
            if player.rect.move(0, 2).colliderect(self.rect) and not self.disappearing_time:
                # если игрок наступил на блок, и таймер ещё не идёт запускаем таймер
                self.disappearing_time = time.time() + 0.6
            if self.disappearing_time is not None and time.time() >= self.disappearing_time:
                # проверяем на то вышло ли время исчезновения
                self.image = self.dotted_line.copy()
                self.is_touchable = False
            if self.disappearing_time is not None and time.time() >= self.disappearing_time + 3:
                # Восстанавливаем изображение блока
                self.image = self.original_image.copy()
                self.is_touchable = True
                self.disappearing_time = None


default_options_file = 'data/default_options.txt'  # путь к настройкам по умолчанию
user_options_file = 'data/options.txt'  # путь к текущим настройкам игры


def load_default_options():
    # Загрузка настроек по умолчанию из файла
    default_options = {}
    with open(default_options_file, 'r', encoding='UTF-8') as file:
        for line in file:
            key, value = line.strip().split()
            default_options[key] = value
    return default_options


def load_font(font_name):
    font_path = 'data/fonts/'
    return font_path + font_name


def is_file_exists(filename, file_path):
    file_path = file_path + filename
    if os.path.exists(file_path):
        return True
    return False


def load_user_options():
    default_options = load_default_options()
    # Загрузка пользовательских настроек из файла, с добавлением отсутствующих значений из default_options
    user_options = default_options.copy()
    try:
        with open(user_options_file, 'r', encoding='UTF-8') as file:
            for line in file:
                key, value = line.strip().split()
                user_options[key] = value
    except FileNotFoundError:
        pass  # Если файл не найден, используются только значения по умолчанию

    # Добавление отсутствующих настроек из default_options
    for key, value in user_options.items():
        if key not in user_options:
            user_options[key] = value

    return user_options


def save_user_options(user_options):
    # Сохранение пользовательских настроек в файл
    with open(user_options_file, 'w', encoding='UTF-8') as file:
        for key, value in user_options.items():
            file.write(f"{key} {value}\n")


def load_level(filename):
    try:
        filename = "data/levels/" + filename
        # читаем уровень, убирая символы перевода строки
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]

        # и подсчитываем максимальную длину
        max_width = max(map(len, level_map))

        # дополняем каждую строку пустыми клетками ('.')
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))
    except ValueError:  # max() arg is an empty sequence
        pass


def generate_level(level, group):
    x, y = None, None  # размеры карты
    player_coords = None
    goblins = []
    for y in range(len(level)):
        for x in range(len(level[y])):
            # определяем типы клеток, их координаты и создаём на их основе тайлы
            if level[y][x] == '1':
                Tile('platform', x, y, *group)
            elif level[y][x] == '2':
                Tile('platform_horizontal', x, y, *group)
            elif level[y][x] == '3':
                Tile('platform_vertical', x, y, *group)
            elif level[y][x] == '4':
                Tile('platform', x, y, *group, is_touchable=False)
            elif level[y][x] == '5':
                Tile('platform_horizontal', x, y, *group, is_touchable=False)
            elif level[y][x] == '6':
                Tile('platform_vertical', x, y, *group, is_touchable=False)
            elif level[y][x] == '7':
                Tile('disappearing_block1', x, y, *group)
            elif level[y][x] == '8':
                Tile('disappearing_block2', x, y, *group)
            elif level[y][x] == '9':
                Tile('disappearing_block3', x, y, *group)
            elif level[y][x] == 's':
                Tile('spike', x, y, *group, is_touchable=False)
            elif level[y][x] == 'd':
                Tile('dirt', x, y, *group)
            elif level[y][x] == 'D':
                Tile('dirt', x, y, *group, is_touchable=False)
            elif level[y][x] == 'u':
                Tile('dirtu', x, y, *group)
            elif level[y][x] == 'U':
                Tile('dirtu', x, y, *group, is_touchable=False)
            elif level[y][x] == 'h':
                Tile('dirth', x, y, *group)
            elif level[y][x] == 'H':
                Tile('dirth', x, y, *group, is_touchable=False)
            elif level[y][x] == 'l':
                Tile('dirtl', x, y, *group)
            elif level[y][x] == 'L':
                Tile('dirtl', x, y, *group, is_touchable=False)
            elif level[y][x] == 'r':
                Tile('dirtr', x, y, *group)
            elif level[y][x] == 'R':
                Tile('dirtr', x, y, *group, is_touchable=False)
            elif level[y][x] == 'q':
                Tile('dirtq', x, y, *group)
            elif level[y][x] == 'Q':
                Tile('dirtq', x, y, *group, is_touchable=False)
            elif level[y][x] == 'w':
                Tile('dirtw', x, y, *group)
            elif level[y][x] == 'W':
                Tile('dirtw', x, y, *group, is_touchable=False)
            elif level[y][x] == 'e':
                Tile('dirte', x, y, *group)
            elif level[y][x] == 'E':
                Tile('dirte', x, y, *group, is_touchable=False)
            elif level[y][x] == 't':
                Tile('dirtt', x, y, *group)
            elif level[y][x] == 'T':
                Tile('dirtt', x, y, *group, is_touchable=False)
            elif level[y][x] == '@':
                player_coords = (x, y)
            elif level[y][x] == 'g':
                goblins.append((x, y))

    tile = Tile(None, 0, 0, group[0])  # создание ориентировочного спрайта
    # оринтеровочный tile, нужен для правильной отрисовки камеры
    # вернем размеры поля и оринтеровочный Tile
    return x, y, tile, player_coords, goblins


def hover(mos_pos: tuple[int, int], screen: pygame.Surface, virtual_surface: pygame.Surface) -> tuple[int, int]:
    x_coeff = virtual_surface.get_width() / screen.get_width()
    y_coeff = virtual_surface.get_height() / screen.get_height()
    return int(mos_pos[0] * x_coeff), int(mos_pos[1] * y_coeff)
