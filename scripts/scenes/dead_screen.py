import pygame


class Button(pygame.sprite.Sprite):
    font = pygame.font.SysFont('Comic Sans MS', 15)

    def __init__(self, pos_x, pos_y, text):
        super().__init__()
        self.image = pygame.Surface((100, 20), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (70, 70, 70), self.image.get_rect(), 0, 20)
        text_surf = self.font.render(text, False, 'White')
        self.image.blit(text_surf, (self.image.get_width() // 2 - text_surf.get_width() // 2,
                                    self.image.get_height() // 2 - text_surf.get_height() // 2))
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.image.get_rect().move(pos_x, pos_y)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)


class DeadScreen:
    def __init__(self, surface: pygame.Surface):
        self.screen = pygame.Surface((surface.get_width() * 0.6, surface.get_height() * 0.6), pygame.SRCALPHA)
        self.surface = surface
        scene_surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        pygame.draw.rect(scene_surface, (60, 60, 60), self.screen.get_rect(), 0, 20)
        scene_surface.set_alpha(150)
        self.screen.blit(scene_surface, (0, 0))
        pygame.draw.rect(self.screen, (255, 255, 255), self.screen.get_rect(), width=1, border_radius=20)
        button_map = Button(self.screen.get_width() * 0.2 - 35, self.screen.get_height() * 0.2, 'Карта')
        button_menu = Button(self.screen.get_width() * 0.8 - 65, self.screen.get_height() * 0.2, 'Меню')
        button_repeat = Button(self.screen.get_width() * 0.5 - 40, self.screen.get_height() * 0.7, 'Повторить')
        button_menu.draw(self.screen)
        button_map.draw(self.screen)
        button_repeat.draw(self.screen)

    def draw(self):
        self.surface.blit(self.screen, (self.surface.get_width() * 0.2, self.surface.get_height() * 0.2))

    def update(self, mos_pos, switch_scene):
        pass
