import pygame
import os
import sys


def load_image(name: str, colorkey=None) -> pygame.Surface:  # функция загрузки изображения
    """
    Функция загрузки изображения
    :param name: str
    :param colorkey: int or None
    :return: pygame.Surface
    """
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image
