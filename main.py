# загружаем нужные библиотеки и модули
import pygame
from logic.scenes.menu import menu_scene
from logic.scenes.WorldMap_scene import world_map_scene
from logic.scenes.game_scene import game_scene

import global_variable
import logic.tools as tools

# проводим инициализацию pygame
pygame.init()

default_options = tools.load_default_options()
settings = tools.load_user_options()
# Теперь settings содержит значения из options.txt, и отсутствующие настройки добавлены из default_options.txt
# Сохранение обновленных настроек в файл options.txt
tools.save_user_options(settings)

# создаём экран
screen = pygame.display.set_mode((800, 500), pygame.RESIZABLE)
pygame.display.set_caption('Зов Героя: Королевский изгнанник')
pygame.mouse.set_visible(False)

# экран на котором всё будет рисоватся, а потом оно растянется
virtual_surface = pygame.Surface((1920, 1080), pygame.SRCALPHA)

# переменная в которой будет храниться текущая сцена
current_scene = None

# Загрузка изображения иконки
icon = tools.load_image('icon.png')

# Установка иконки для окна
pygame.display.set_icon(icon)

# инициализация музыки в меню
pygame.mixer.music.load('data/music_and_sound/background_music_for_menu.mp3')
pygame.mixer.music.play(-1)
global_variable.is_music_play = True
pygame.mixer.music.set_volume(global_variable.volume_sound_background)


# функция переключения сцен
def switch_scene(scene):
    global current_scene
    current_scene = scene


switch_scene(menu_scene)
while current_scene is not None:
    if current_scene == 'menu_scene':
        if global_variable.is_music_play is False:
            pygame.mixer.music.play(-1)
            global_variable.is_music_play = True
        switch_scene(menu_scene)
    elif current_scene == 'world_map':
        if global_variable.is_music_play is False:
            pygame.mixer.music.play(-1)
            global_variable.is_music_play = True
        switch_scene(world_map_scene)
    elif current_scene == 'game_scene':
        pygame.mixer.music.stop()
        switch_scene(game_scene)

    # запуск текущей сцены
    current_scene(screen, virtual_surface, switch_scene, settings)

pygame.quit()
