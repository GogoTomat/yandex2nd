import pygame
import sys
from constants import WIDTH, HEIGHT, WHITE
from utils import show_message, draw_timer, show_level_complete_screen
from levels import load_level
from ghost import Ghost

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Platformer")
clock = pygame.time.Clock()

# Меню выбора уровня
def start_menu(total_stars):
    from button import Button
    # Шрифты
    big_font = pygame.font.Font(None, 72)
    small_font = pygame.font.Font(None, 36)

    # Кнопки уровней
    b1 = Button(WIDTH//2 - 150, HEIGHT//2 - 40, 300, 60, "Level 1")
    b2 = Button(WIDTH//2 - 150, HEIGHT//2 + 40, 300, 60, "Level 2")

    while True:
        screen.fill(WHITE)
        title = big_font.render("Выбор уровня", True, (0, 0, 0))
        screen.blit(title, title.get_rect(center=(WIDTH//2, 100)))

        info = small_font.render(f"Всего монеток: {total_stars}", True, (0, 0, 0))
        screen.blit(info, info.get_rect(center=(WIDTH//2, 180)))

        b1.draw(screen)
        b2.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if b1.is_clicked(event.pos):
                    return 1
                if b2.is_clicked(event.pos):
                    return 2


def main():
    total_stars = 0

    while True:
        current_level = start_menu(total_stars)

        # Загружаем уровень и инициализируем
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

            # Запуск таймера при первом движении
            if not timer_started and (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_SPACE]):
                timer_started = True

            # Логика игрока
            player.move(keys, platforms)
            player.draw(screen)

            # Платформы
            for p in platforms:
                p.draw(screen)

            # Кнопка и дверь
            button.update_state(player, ghost)
            button.draw(screen)
            door.draw(screen)

            # Звезды
            for star in stars:
                star.check_collision(player)
                star.draw(screen)

            # Враги
            for enemy in enemies[:]:
                enemy.update()
                enemy.draw(screen)
                if player.rect.colliderect(enemy.rect):
                    show_message("Вы проиграли! Попробуйте снова.")
                    game_running = False

            # Пули
            for bullet in player.bullets[:]:
                bullet.update()
                if bullet.rect.x < 0 or bullet.rect.x > WIDTH:
                    player.bullets.remove(bullet)
                    continue
                for enemy in enemies[:]:
                    if bullet.rect.colliderect(enemy.rect):
                        enemies.remove(enemy)
                        player.bullets.remove(bullet)
                        break
                bullet.draw(screen)

            # Шипы
            for spike in spikes:
                spike.draw(screen)
                if player.rect.colliderect(spike.rect):
                    show_message("Вы наткнулись на шипы!")
                    game_running = False
                    break

            # Призрак
            if timer_started:
                if ghost is None:
                    time_left = ghost_delay - ghost_timer
                    if time_left > 0:
                        draw_timer(screen, time_left)
                    else:
                        ghost = Ghost(player.history)
                else:
                    ghost.update()
                    ghost.draw(screen)
                    if ghost.rect.colliderect(player.rect):
                        show_message("Вы проиграли! Попробуйте снова.")
                        game_running = False

            # Завершение уровня
            if door.is_open() and player.rect.colliderect(door.rect):
                action = show_level_complete_screen(player.collected_stars, len(stars))
                if action == 'restart':
                    break
                elif action == 'next':
                    total_stars += player.collected_stars
                    # Если больше уровней нет — выход
                    if current_level >= 2:
                        pygame.quit()
                        sys.exit()
                    break

            pygame.display.flip()
            clock.tick(60)
            if timer_started:
                ghost_timer += 1


if __name__ == "__main__":
    main()
