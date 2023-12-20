# загружаем нужные библиотеки и модули
import pygame
from scripts.menu import menu_scene

# проводим инициализацию pygame
pygame.init()

# создаём экран
info = pygame.display.Info()

# получение ширины и высоты монитора
screen_width = 800
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

# экран на котором всё будет рисоватся, а потом оно растянется
virtual_surface = pygame.Surface((screen_width, screen_height))

# переменная в которой будет храниться текущая сцена
current_scene = None


def switch_scene(scene):
    global current_scene
    current_scene = scene


switch_scene(menu_scene)
while current_scene is not None:
    current_scene(screen, virtual_surface, switch_scene)

pygame.quit()
