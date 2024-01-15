import pygame

current_level = ''
is_music_play = False
volume_sound_background = 0


def increase_volume():
    global volume_sound_background
    volume_sound_background += 0.003
    volume_sound_background = min(volume_sound_background, 1)
    pygame.mixer.music.set_volume(volume_sound_background)
