import pygame
import os
import sys

pygame.init()
pygame.display.set_mode((800, 500), pygame.RESIZABLE)


def load_image(name: str, colorkey=None, reverse=False) -> pygame.Surface:  # функция загрузки изображения
    """
    Функция загрузки изображения
    :param name: str
    :param colorkey: int or None
    :param reverse bool
    :return: pygame.Surface
    """
    # Полный путь к изображению
    fullname = os.path.join('data\\images', name)

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


# импортируем после создания функции load_image, что бы не было ошибок
from logic.entity.Tile import Tile
from logic.entity.Tile_Info import tile_info


# загрузка статистики
def load_statistics():
    stats = dict()
    try:
        with open('data/Saves/statistics', 'r') as file:
            for line in file.readlines():
                key, value = line.strip().split()
                stats[key] = int(value)
    except Exception:
        print('Не удалось получить статистику')
    return stats


# сохранение статистики в файле:
def save_statistics(stats: dict[str, int]):
    with open('data/Saves/statistics', 'w', encoding='UTF-8') as file:
        for key, value in stats.items():
            file.write(f"{key} {value}\n")


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
            if level[y][x] == '@':
                player_coords = (x, y)
            elif level[y][x] == 'g':
                goblins.append((x, y))
            elif level[y][x] == '.':
                continue
            else:
                tile_info[level[y][x]][2](tile_info[level[y][x]][0], x, y, *group,
                                          is_touchable=tile_info[level[y][x]][1])

    tile = Tile(None, 0, 0, group[0])  # создание ориентировочного спрайта
    # оринтеровочный tile, нужен для правильной отрисовки камеры
    # вернем размеры поля и оринтеровочный Tile
    return x, y, tile, player_coords, goblins


def hover(mos_pos: tuple[int, int], screen: pygame.Surface, virtual_surface: pygame.Surface) -> tuple[int, int]:
    x_coeff = virtual_surface.get_width() / screen.get_width()
    y_coeff = virtual_surface.get_height() / screen.get_height()
    return int(mos_pos[0] * x_coeff), int(mos_pos[1] * y_coeff)
