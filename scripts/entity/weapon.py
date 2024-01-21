# файл в котором будет логика получения урона
import pygame

# словарь с характеристикой оружий по следующей структуре: название оружия:
# ((размеры поражаемой зоны rect в картеже),
# (координаты левого верхнего угла поражаемой зоны относительно владельца оружия, картеж),
# (кадр анимации, начиная с которой игрок получает урон число)),
# (урон наносимый оружием)
weapon_stats = {'hummer': ((30, 35), (30, 13), 4, 40),
                'sword': ((16, 16), (28, 16), 2, 10)}


class Weapon:
    def __init__(self, owner, type_weapon):
        self.owner = owner
        self.weapon = weapon_stats[type_weapon]
        self.rect = pygame.Rect(owner.rect.x + self.weapon[1][0], owner.rect.y + self.weapon[1][1],
                                self.weapon[0][0], self.weapon[0][1])

    def update(self):
        self.rect.x = self.owner.rect.x + self.weapon[[1][0]]
        self.rect.y = self.owner.rect.y + self.weapon[[1][1]]

    def collide(self, target):
        if self.owner.frame_ind >= self.weapon[2]:
            if target.rect.colliderect(self.rect):
                target.get_damage(self.weapon[3])
