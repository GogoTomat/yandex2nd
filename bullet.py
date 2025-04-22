import pygame
from constants import BLACK


class Bullet:
    def __init__(self, x, y, dir):
        self.rect = pygame.Rect(x, y, 10, 5)
        self.dir = dir
        self.speed = 10
    def update(self):
        self.rect.x += self.dir * self.speed
    def draw(self, surf):
        pygame.draw.rect(surf, BLACK, self.rect)
