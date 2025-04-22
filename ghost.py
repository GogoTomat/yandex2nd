import pygame


class Ghost:
    def __init__(self, history):
        self.history = list(history)
        self.index = 0
        self.rect = pygame.Rect(0, 0, 40, 50)
        self.active = True

    def update(self):
        if self.index < len(self.history):
            self.rect.topleft = self.history[self.index]
            self.index += 1
        else:
            self.active = False

    def draw(self, surf):
        if self.active:
            pygame.draw.rect(surf, (255,0,0), self.rect, 2)
