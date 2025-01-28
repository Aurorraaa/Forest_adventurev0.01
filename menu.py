import pygame
import sys


def show_main_menu(screen, clock):
    """Отображает главное меню и возвращает 'play' или 'quit'."""
    font = pygame.font.Font(None, 72)  # Шрифт для заголовка
    small_font = pygame.font.Font(None, 40)  # Шрифт для кнопок

    # Фон (вы можете заменить на загрузку картинки или другой цвет)
    menu_bg = pygame.Surface(screen.get_size())
    menu_bg.fill((50, 100, 50))

    # Прямоугольники кнопок (x, y, width, height)
    play_button_rect = pygame.Rect(300, 200, 200, 60)
    quit_button_rect = pygame.Rect(300, 300, 200, 60)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Закрытие окна -> выходим из игры
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Проверяем, попал ли клик по кнопкам
                if play_button_rect.collidepoint(event.pos):
                    return "play"
                elif quit_button_rect.collidepoint(event.pos):
                    return "quit"

        # Отрисовываем меню
        screen.blit(menu_bg, (0, 0))

        # Заголовок
        title_surf = font.render("Forest Adventure", True, (255, 255, 255))
        screen.blit(
            title_surf,
            (screen.get_width() // 2 - title_surf.get_width() // 2, 80)
        )

        # Кнопка "Play"
        pygame.draw.rect(screen, (100, 200, 100), play_button_rect)
        play_text = small_font.render("Play", True, (0, 0, 0))
        screen.blit(
            play_text,
            (
                play_button_rect.centerx - play_text.get_width() // 2,
                play_button_rect.centery - play_text.get_height() // 2
            )
        )

        # Кнопка "Quit"
        pygame.draw.rect(screen, (200, 100, 100), quit_button_rect)
        quit_text = small_font.render("Quit", True, (0, 0, 0))
        screen.blit(
            quit_text,
            (
                quit_button_rect.centerx - quit_text.get_width() // 2,
                quit_button_rect.centery - quit_text.get_height() // 2
            )
        )

        pygame.display.flip()
        clock.tick(60)
