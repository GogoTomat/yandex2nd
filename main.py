import pygame
import sys
from collections import deque

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
GRAVITY = 0.5
PLAYER_SPEED = 5
JUMP_POWER = -10
GHOST_DELAY = 300  # Время перед появлением клона (5 секунд при 60 FPS)

# Цвета
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BROWN = (139, 69, 19)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Platformer")
clock = pygame.time.Clock()

# Класс игрока
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 50)
        self.vel_y = 0
        self.on_ground = False
        self.history = deque(maxlen=GHOST_DELAY)
    
    def move(self, keys, platforms):
        dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * PLAYER_SPEED
        self.rect.x += dx
        
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vel_y > 0:
                self.rect.bottom = platform.rect.top
                self.vel_y = 0
                self.on_ground = True
                
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = JUMP_POWER
        
        self.history.append((self.rect.x, self.rect.y))
    
    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, self.rect)

class Ghost:
    def __init__(self, history):
        self.history = list(history)
        self.index = 0
        self.rect = pygame.Rect(0, 0, 40, 50)
        self.active = True
    
    def update(self):
        if self.active and self.index < len(self.history):
            self.rect.topleft = self.history[self.index]
            self.index += 1
        else:
            self.active = False
    
    def draw(self, surface):
        if self.active:
            pygame.draw.rect(surface, RED, self.rect, 2)

class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
    
    def draw(self, surface):
        pygame.draw.rect(surface, GREEN, self.rect)

class Button:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.activated = False
    
    def check_collision(self, entity):
        if self.rect.colliderect(entity.rect):
            self.activated = True
        else:
            self.activated = False
    
    def draw(self, surface):
        color = GREEN if self.activated else (100, 100, 100)
        pygame.draw.rect(surface, color, self.rect)

class Door:
    def __init__(self, x, y, button):
        self.rect = pygame.Rect(x, y, 60, 100)
        self.button = button
    
    def is_open(self):
        return self.button.activated
    
    def draw(self, surface):
        if not self.is_open():
            pygame.draw.rect(surface, BROWN, self.rect)

def load_level(level):
    if level == 1:
        return (
            Player(100, 500),
            [Platform(0, 580, WIDTH, 20), Platform(200, 450, 150, 20), Platform(400, 350, 150, 20), Platform(600, 250, 150, 20)],
            Button(500, 550),
            Door(700, 480, None)
        )
    elif level == 2:
        return (
            Player(100, 500),
            [Platform(0, 580, WIDTH, 20), Platform(300, 400, 200, 20), Platform(600, 300, 150, 20)],
            Button(400, 500),
            Door(700, 450, None)
        )

current_level = 1
while True:
    player, platforms, button, door = load_level(current_level)
    door.button = button
    ghost = None
    ghost_timer = 0
    game_running = True
    
    while game_running:
        screen.fill(WHITE)
        keys = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        player.move(keys, platforms)
        player.draw(screen)
        
        for platform in platforms:
            platform.draw(screen)
        
        button.check_collision(player)
        if ghost:
            button.check_collision(ghost)
        button.draw(screen)
        
        door.draw(screen)
        
        if ghost is None and ghost_timer >= GHOST_DELAY:
            ghost = Ghost(player.history)
        if ghost:
            ghost.update()
            ghost.draw(screen)
        
        if ghost and ghost.rect.colliderect(player.rect):
            print("Игра окончена! Вы столкнулись с клоном.")
            game_running = False
        
        if door.is_open() and player.rect.colliderect(door.rect):
            print(f"Уровень {current_level} пройден!")
            current_level += 1
            if current_level > 2:
                print("Игра завершена!")
                pygame.quit()
                sys.exit()
            break
        
        pygame.display.flip()
        clock.tick(60)
        ghost_timer += 1