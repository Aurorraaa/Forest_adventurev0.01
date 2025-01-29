import pygame
import sys


def show_main_menu(screen, clock):
    """Отображает главное меню и возвращает 'play' или 'quit'."""
    font = pygame.font.Font(None, 72)  # Шрифт для заголовка
    small_font = pygame.font.Font(None, 40)  # Шрифт для кнопок
    background_image = pygame.image.load("Data/menu_back.png").convert()
    background_image = pygame.transform.scale(background_image, screen.get_size())
    play_button_image = pygame.image.load("Data/buttons/play01.png").convert_alpha()
    quit_button_image = pygame.image.load("Data/buttons/back01.png").convert_alpha()
    game_name = pygame.image.load("Data/yaname (1).png")
    menu_bg = pygame.Surface(screen.get_size())
    menu_bg.fill((50, 100, 50))

    # Прямоугольники кнопок (x, y, width, height)
    play_button_rect = play_button_image.get_rect(topleft=(370,450))
    quit_button_rect = quit_button_image.get_rect(topleft = (550, 450))
    name_rect = game_name.get_rect(topleft=(220, 0))
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
        screen.blit(background_image, (0, 0))

        # Заголовок
        screen.blit(game_name, name_rect)
        screen.blit(play_button_image, play_button_rect)
        screen.blit(quit_button_image, quit_button_rect)

        pygame.display.flip()
        clock.tick(60)
