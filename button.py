import pygame
from constants import GRAY, BLACK
from fonts import font_small


class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = GRAY
        self.activated = False

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect)
        ts = font_small.render(self.text, True, BLACK)
        surf.blit(ts, ts.get_rect(center=self.rect.center))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def update_state(self, player, ghost):
        self.activated = (
            self.rect.colliderect(player.rect) or
            (ghost and self.rect.colliderect(ghost.rect))
        )
