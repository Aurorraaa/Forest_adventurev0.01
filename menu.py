import pygame
import sys


def show_main_menu(screen, clock):
    """Отображает главное меню и возвращает 'play' или 'quit'."""
    font = pygame.font.Font(None, 72)  # Шрифт для заголовка
    small_font = pygame.font.Font(None, 40)  # Шрифт для кнопок
    background_image = pygame.image.load("Data/menu_back.png").convert()
    background_image = pygame.transform.scale(background_image, screen.get_size())
    play_button_images = {"normal": pygame.image.load("Data/buttons/play/play01.png").convert_alpha(),
                          "hover": pygame.image.load("Data/buttons/play/play02.png").convert_alpha(),
                          "pressed": pygame.image.load("Data/buttons/play/play03.png").convert_alpha()}

    quit_button_images = {"normal": pygame.image.load("Data/buttons/back/back01.png").convert_alpha(),
                          "hover": pygame.image.load("Data/buttons/back/back02.png").convert_alpha(),
                          "pressed": pygame.image.load("Data/buttons/back/back03.png").convert_alpha()}
    game_name = pygame.image.load("Data/yaname (1).png")
    menu_bg = pygame.Surface(screen.get_size())
    menu_bg.fill((50, 100, 50))

    play_button_rect = play_button_images["normal"].get_rect(topleft=(370, 450))
    quit_button_rect = quit_button_images["normal"].get_rect(topleft=(550, 450))
    name_rect = game_name.get_rect(topleft=(220, 0))

    play_button_state = "normal"
    quit_button_state = "normal"

    def update_button_state_on_hover(mouse_pos):
        nonlocal play_button_state, quit_button_state
        if play_button_rect.collidepoint(mouse_pos):
            if play_button_state != "pressed":
                play_button_state = "hover"
        else:
            if play_button_state != "pressed":
                play_button_state = "normal"

        if quit_button_rect.collidepoint(mouse_pos):
            if quit_button_state != "pressed":
                quit_button_state = "hover"
        else:
            if quit_button_state != "pressed":
                quit_button_state = "normal"

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                update_button_state_on_hover(event.pos)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if play_button_rect.collidepoint(event.pos):
                        play_button_state = "pressed"
                    if quit_button_rect.collidepoint(event.pos):
                        quit_button_state = "pressed"

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if play_button_state == "pressed":
                        if play_button_rect.collidepoint(event.pos):
                            return "play"
                        else:
                            play_button_state = "normal"

                    if quit_button_state == "pressed":
                        if quit_button_rect.collidepoint(event.pos):
                            return "quit"
                        else:
                            quit_button_state = "normal"

                    update_button_state_on_hover(mouse_pos)
        screen.blit(background_image, (0, 0))

        current_play_image = play_button_images[play_button_state]
        current_quit_image = quit_button_images[quit_button_state]
        screen.blit(current_play_image, play_button_rect)
        screen.blit(current_quit_image, quit_button_rect)

        pygame.display.flip()
        clock.tick(60)
