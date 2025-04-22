import pygame
from constants import RED


class Enemy:
    def __init__(self, x, y, w, h, move_range):
        self.rect = pygame.Rect(x, y, w, h)
        self.range = move_range
        self.dir = 1
        self.speed = 2
    def update(self):
        self.rect.x += self.dir * self.speed
        if self.rect.x >= self.range[1]: self.dir = -1
        if self.rect.x <= self.range[0]: self.dir = 1
    def draw(self, surf):
        pygame.draw.rect(surf, RED, self.rect)
