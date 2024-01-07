import pygame
import scripts.tools as tools


def mini_game_scene():
    def __init__(self, width: int, height: int, settings: dict):
        self.width, self.height = round(width * 0.6), round(height * 0.6)
        self.languages = ["English", "Русский"]  # Список поддерживаемых языков
        self.settings = settings
        self.selected_language = settings['Language']