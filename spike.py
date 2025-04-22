import pygame
from constants import RED


class Spike:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
    def draw(self, surf):
        pts = [(self.rect.centerx, self.rect.top), (self.rect.right, self.rect.bottom), (self.rect.left, self.rect.bottom)]
        pygame.draw.polygon(surf, RED, pts)
