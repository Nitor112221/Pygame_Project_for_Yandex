# загружаем нужные библиотеки и модули
import pygame
from scripts.scenes.menu import menu_scene
import scripts.tools as tools

# проводим инициализацию pygame
pygame.init()

default_options = tools.load_default_options()
settings = tools.load_user_options()
# Теперь user_options содержит значения из options.txt, и отсутствующие настройки добавлены из default_options
# Сохранение обновленных настроек в файл options.txt
tools.save_user_options(settings)

# создаём экран
screen = pygame.display.set_mode((800, 500), pygame.RESIZABLE)

# экран на котором всё будет рисоватся, а потом оно растянется
virtual_surface = pygame.Surface((1920, 1080), pygame.SRCALPHA)

# переменная в которой будет храниться текущая сцена
current_scene = None


def switch_scene(scene):
    global current_scene
    current_scene = scene


switch_scene(menu_scene)
while current_scene is not None:
    if current_scene == 'menu_scene':
        switch_scene(menu_scene)
    current_scene(screen, virtual_surface, switch_scene, settings)

pygame.quit()
