import pygame
from collections import deque
from constants import GRAVITY, PLAYER_SPEED, JUMP_POWER, WIDTH, HEIGHT
from bullet import Bullet
from utils import show_message

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 50)
        self.vel_y = 0
        self.on_ground = False
        self.history = deque()
        self.collected_stars = 0
        self.bullets = []
        self.shoot_cooldown = 0

    def move(self, keys, platforms):
        dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * PLAYER_SPEED
        self.rect.x += dx

        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        self.on_ground = False
        for p in platforms:
            if self.rect.colliderect(p.rect) and self.vel_y > 0:
                self.rect.bottom = p.rect.top
                self.vel_y = 0
                self.on_ground = True

        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = JUMP_POWER

        if self.shoot_cooldown <= 0:
            if keys[pygame.K_e]:
                self.bullets.append(Bullet(self.rect.right, self.rect.centery, 1))
                self.shoot_cooldown = 20
            elif keys[pygame.K_q]:
                self.bullets.append(Bullet(self.rect.left - 10, self.rect.centery, -1))
                self.shoot_cooldown = 20
        else:
            self.shoot_cooldown -= 1

        self.history.append((self.rect.x, self.rect.y))

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.top > HEIGHT:
            show_message("Вы упали! Попробуйте снова.")
            raise Exception('player_fell')

    def draw(self, surf):
        from constants import BLUE
        pygame.draw.rect(surf, BLUE, self.rect)
        for b in list(self.bullets):
            b.draw(surf)
