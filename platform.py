import pygame
from constants import GREEN


class Platform:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
    def draw(self, surf):
        pygame.draw.rect(surf, GREEN, self.rect)
