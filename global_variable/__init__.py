import pygame

current_level = ''
is_music_play = False
volume_sound_background = 0
statistics = {}


def increase_volume(settings: dict):
    global volume_sound_background
    volume_sound_background += 0.005
    volume_sound_background = min(volume_sound_background, 1)
    pygame.mixer.music.set_volume(volume_sound_background)
    if settings['Music'] == 'Off':
        volume_sound_background += -0.02
        volume_sound_background = max(0, volume_sound_background)
        pygame.mixer.music.set_volume(volume_sound_background)
