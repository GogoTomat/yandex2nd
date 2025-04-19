import pygame
import sys
from collections import deque

pygame.init()

# Константы
WIDTH, HEIGHT = 1200, 600
GRAVITY = 0.5
PLAYER_SPEED = 5
JUMP_POWER = -10

# Цвета
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Platformer")
clock = pygame.time.Clock()

# Шрифт для текста
font = pygame.font.Font(None, 36)


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
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vel_y > 0:
                self.rect.bottom = platform.rect.top
                self.vel_y = 0
                self.on_ground = True

        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = JUMP_POWER

        self.history.append((self.rect.x, self.rect.y))

        if keys[pygame.K_q] and self.shoot_cooldown <= 0:
            direction = 1
            bullet = Bullet(self.rect.right, self.rect.centery, direction)
            self.bullets.append(bullet)
            self.shoot_cooldown = 20

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, self.rect)
        for bullet in self.bullets:
            bullet.draw(surface)


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

    def draw(self, surface):
        if self.active:
            pygame.draw.rect(surface, RED, self.rect, 2)


class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, surface):
        pygame.draw.rect(surface, GREEN, self.rect)


class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = GRAY
        self.activated = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def update_state(self, player, ghost):
        self.activated = self.rect.colliderect(player.rect) or (ghost and self.rect.colliderect(ghost.rect))


class Door:
    def __init__(self, x, y, button):
        self.rect = pygame.Rect(x, y, 60, 100)
        self.button = button

    def is_open(self):
        return self.button.activated

    def draw(self, surface):
        if not self.is_open():
            pygame.draw.rect(surface, BROWN, self.rect)


class Star:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.collected = False

    def check_collision(self, player):
        if self.rect.colliderect(player.rect) and not self.collected:
            self.collected = True
            player.collected_stars += 1

    def draw(self, surface):
        if not self.collected:
            pygame.draw.circle(surface, YELLOW, self.rect.center, 10)


class Enemy:
    def __init__(self, x, y, width, height, move_range):
        self.rect = pygame.Rect(x, y, width, height)
        self.move_range = move_range
        self.direction = 1
        self.speed = 2

    def update(self):
        self.rect.x += self.direction * self.speed
        if self.rect.x >= self.move_range[1]:
            self.direction = -1
        elif self.rect.x <= self.move_range[0]:
            self.direction = 1

    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect)


class Bullet:
    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x, y, 10, 5)
        self.direction = direction
        self.speed = 10

    def update(self):
        self.rect.x += self.direction * self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, BLACK, self.rect)


class Spike:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = RED

    def draw(self, surface):
        points = [
            (self.rect.centerx, self.rect.top),
            (self.rect.right, self.rect.bottom),
            (self.rect.left, self.rect.bottom)
        ]
        pygame.draw.polygon(surface, self.color, points)


def show_message(text):
    font = pygame.font.Font(None, 50)
    message = font.render(text, True, (0, 0, 0))
    screen.fill(WHITE)
    screen.blit(message, (WIDTH // 2 - 200, HEIGHT // 2 - 50))
    pygame.display.flip()
    pygame.time.delay(2000)


def load_level(level):
    if level == 1:
        return (
            Player(100, 500),
            [Platform(0, 580, WIDTH, 20), Platform(200, 450, 150, 20),
             Platform(400, 350, 150, 20), Platform(600, 250, 150, 20)],
            Button(800, 550, 40, 40, ""),
            Door(1100, 480, None),
            [Star(250, 430), Star(450, 330), Star(650, 230)],
            300,
            [Enemy(300, 530, 40, 40, (300, 500)), Enemy(700, 330, 40, 40, (700, 750))],
            [Spike(500, 550, 50, 30), Spike(550, 550, 50, 30)]
        )
    elif level == 2:
        return (
            Player(100, 500),
            [Platform(0, 580, WIDTH, 20), Platform(300, 400, 200, 20), Platform(600, 300, 150, 20)],
            Button(400, 500, 40, 40, ""),
            Door(700, 450, None),
            [Star(350, 380), Star(620, 280), Star(720, 200)],
            600,
            [Enemy(200, 530, 40, 40, (200, 400)), Enemy(600, 330, 40, 40, (600, 800))],
            [Spike(200, 550, 50, 30), Spike(400, 550, 50, 30)]
        )


def draw_timer(surface, time_left):
    timer_text = font.render(f"Ghost in: {time_left // 60}", True, BLACK)
    surface.blit(timer_text, (10, 10))


def show_level_complete_screen(collected_stars, total_stars):
    screen.fill(WHITE)
    message = font.render(f"Уровень пройден! Звезд собрано: {collected_stars}/{total_stars}", True, BLACK)
    screen.blit(message, (WIDTH // 2 - 200, HEIGHT // 2 - 100))

    restart_button = Button(WIDTH // 2 - 150, HEIGHT // 2, 200, 50, "Начать сначала")
    restart_button.draw(screen)

    next_level_button = Button(WIDTH // 2 - 150, HEIGHT // 2 + 70, 200, 50, "Следующий уровень")
    next_level_button.draw(screen)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.is_clicked(event.pos):
                    return "restart"
                if next_level_button.is_clicked(event.pos):
                    return "next"


current_level = 1
while True:
    player, platforms, button, door, stars, ghost_delay, enemies, spikes = load_level(current_level)
    door.button = button
    ghost = None
    ghost_timer = 0
    game_running = True
    timer_started = False

    while game_running:
        screen.fill(WHITE)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not timer_started and (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_SPACE]):
            timer_started = True

        player.move(keys, platforms)
        player.draw(screen)

        for platform in platforms:
            platform.draw(screen)

        button.update_state(player, ghost)
        button.draw(screen)

        door.draw(screen)

        for star in stars:
            star.check_collision(player)
            star.draw(screen)

        for enemy in enemies[:]:
            enemy.update()
            enemy.draw(screen)
            if player.rect.colliderect(enemy.rect):
                show_message("Вы проиграли! Попробуйте снова.")
                game_running = False

        for bullet in player.bullets[:]:
            bullet.update()
            bullet.draw(screen)
            if bullet.rect.x < 0 or bullet.rect.x > WIDTH:
                player.bullets.remove(bullet)
                continue
            for enemy in enemies[:]:
                if bullet.rect.colliderect(enemy.rect):
                    enemies.remove(enemy)
                    player.bullets.remove(bullet)
                    break

        for spike in spikes:
            spike.draw(screen)
            if player.rect.colliderect(spike.rect):
                show_message("Вы наткнулись на шипы!")
                game_running = False
                break

        if timer_started:
            if ghost is None:
                time_left = ghost_delay - ghost_timer
                if time_left > 0:
                    draw_timer(screen, time_left)
                else:
                    ghost = Ghost(player.history)

        if ghost:
            ghost.update()
            ghost.draw(screen)
            if ghost.rect.colliderect(player.rect):
                show_message("Вы проиграли! Попробуйте снова.")
                game_running = False

        if door.is_open() and player.rect.colliderect(door.rect):
            action = show_level_complete_screen(player.collected_stars, len(stars))
            if action == "restart":
                break
            elif action == "next":
                current_level += 1
                if current_level > 2:
                    pygame.quit()
                    sys.exit()
                break

        pygame.display.flip()
        clock.tick(60)
        if timer_started:
            ghost_timer += 1
        