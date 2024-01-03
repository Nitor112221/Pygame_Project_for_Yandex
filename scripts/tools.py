import pygame
import os
import sys

pygame.init()


def load_image(name: str, colorkey=None) -> pygame.Surface:  # функция загрузки изображения
    """
    Функция загрузки изображения
    :param name: str
    :param colorkey: int or None
    :return: pygame.Surface
    """
    fullname = os.path.join('data/images', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        elif colorkey == -2:
            colorkey = image.get_at((0, image.get_height()))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def tile_init():
    global tile_images, tile_width, tile_height
    tile_images = {
        'platform': load_image('platform/platform.png'),
        'platform_horizontal': load_image('platform/platform_horizontal.png'),
        'platform_vertical': load_image('platform/platform_vertical.png')
    }

    tile_width = tile_height = 8


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, *groups):
        super().__init__(*groups)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


default_options_file = 'data/default_options.txt'
user_options_file = 'data/options.txt'


def load_default_options():
    # Загрузка настроек по умолчанию из файла
    default_options = {}
    with open(default_options_file, 'r', encoding='UTF-8') as file:
        for line in file:
            key, value = line.strip().split()
            default_options[key] = value
    return default_options


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
    filename = "data/levels/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level, group):
    x, y = None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '1':
                Tile('platform', x, y, *group)
            elif level[y][x] == '2':
                Tile('platform_horizontal', x, y, *group)
            elif level[y][x] == '3':
                Tile('platform_vertical', x, y, *group)
    # вернем игрока, а также размер поля в клетках
    return x, y


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, *group):
        super().__init__(*group)
        self.rect = pygame.Rect(0, 0, 50, 50) .move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)