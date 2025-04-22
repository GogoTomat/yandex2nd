import pygame
from constants import YELLOW


class Star:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.collected = False
    def check_collision(self, player):
        if not self.collected and self.rect.colliderect(player.rect):
            self.collected = True
            player.collected_stars += 1
    def draw(self, surf):
        if not self.collected:
            pygame.draw.circle(surf, YELLOW, self.rect.center, 10)
