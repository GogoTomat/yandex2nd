import pygame
import sys

from constants import WIDTH, HEIGHT, WHITE, BLACK
from fonts import font_small, font_large

def show_message(text):
    msg = font_large.render(text, True, BLACK)
    screen = pygame.display.get_surface()
    screen.fill(WHITE)
    screen.blit(msg, msg.get_rect(center=(WIDTH//2, HEIGHT//2)))
    pygame.display.flip()
    pygame.time.delay(2000)

def draw_timer(surface, time_left):
    txt = font_small.render(f"Ghost in: {time_left//60}", True, BLACK)
    surface.blit(txt, (10, 10))

def show_level_complete_screen(collected, total):
    screen = pygame.display.get_surface()
    screen.fill(WHITE)
    txt = font_small.render(f"Уровень пройден! Звезд собрано: {collected}/{total}", True, BLACK)
    screen.blit(txt, (WIDTH//2 - 200, HEIGHT//2 - 50))

    from button import Button

    restart = Button(WIDTH//2 - 150, HEIGHT//2 + 10, 200, 50, "Начать сначала")
    next_lvl = Button(WIDTH//2 - 150, HEIGHT//2 + 80, 200, 50, "Следующий уровень")
    restart.draw(screen)
    next_lvl.draw(screen)
    pygame.display.flip()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if restart.is_clicked(e.pos):
                    return 'restart'
                if next_lvl.is_clicked(e.pos):
                    return 'next'
