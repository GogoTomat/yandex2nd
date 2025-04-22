import pygame
from constants import BROWN


class Door:
    def __init__(self, x, y, button):
        self.rect = pygame.Rect(x, y, 60, 100)
        self.button = button
    def is_open(self):
        return self.button.activated
    def draw(self, surf):
        if not self.is_open():
            pygame.draw.rect(surf, BROWN, self.rect)
