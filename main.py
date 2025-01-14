import pygame
import pytmx

SIZE = WIDTH, HEIGHT = 800, 600


def main():
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Forest Adventure")

    # Загрузка карты
    try:
        tmx_data = pytmx.load_pygame("Data/map/map.tmx")
    except Exception as e:
        print(f"Ошибка загрузки карты: {e}")
        return

    tile_width = tmx_data.tilewidth
    tile_height = tmx_data.tileheight

    # Загружаем спрайт-лист для idle анимации
    try:
        idle_sheet = pygame.image.load("Data/gg_sprites/idle sheet-Sheet.png").convert_alpha()
        run_sheet = pygame.image.load("Data/gg_sprites/itch run-Sheet sheet.png").convert_alpha()
    except Exception as e:
        print(f"Ошибка загрузки спрайтов: {e}")
        return

    # Разделяем спрайт-лист на кадры для idle анимации
    idle_frame_width = idle_sheet.get_width() // 8
    idle_frame_height = idle_sheet.get_height()
    idle_frames = [
        idle_sheet.subsurface(pygame.Rect(i * idle_frame_width, 0, idle_frame_width, idle_frame_height))
        for i in range(8)
    ]

    # Разделяем спрайт-лист на кадры для анимации бега
    run_frame_width = run_sheet.get_width() // 8
    run_frame_height = run_sheet.get_height()
    run_frames = [
        run_sheet.subsurface(pygame.Rect(i * run_frame_width, 0, run_frame_width, run_frame_height))
        for i in range(8)
    ]

    # Загрузка стартовой позиции
    start_x, start_y = 0, 0
    for obj in tmx_data.objects:
        if obj.name == "start_place":
            start_x, start_y = obj.x, obj.y
            break

    player_pos = [start_x, start_y]
    player_frame = 0
    player_speed = 5
    flrunning = True
    player_direction = "idle"
    animation_timer = pygame.time.get_ticks()

    clock = pygame.time.Clock()

    while flrunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flrunning = False

        # Обработка клавиш для движения
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player_pos[0] -= player_speed
            player_direction = "run"
        elif keys[pygame.K_d]:
            player_pos[0] += player_speed
            player_direction = "run"
        elif keys[pygame.K_w]:
            player_pos[1] -= player_speed
            player_direction = "run"
        elif keys[pygame.K_s]:
            player_pos[1] += player_speed
            player_direction = "run"
        else:
            player_direction = "idle"

        # Отображаем фон и тайлы
        screen.fill((0, 0, 0))  # Очистка экрана перед отрисовкой
        for layer in tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        screen.blit(tile, (x * tile_width, y * tile_height))

        # Переключение кадров анимации
        current_time = pygame.time.get_ticks()
        if current_time - animation_timer > 100:  # Обновляем кадры каждые 100 мс
            animation_timer = current_time
            if player_direction == "run":
                player_frame = (player_frame + 1) % len(run_frames)
            else:
                player_frame = 0

        # Выбор текущего кадра
        if player_direction == "run":
            current_sprite = run_frames[player_frame]
        else:
            current_sprite = idle_frames[player_frame]

        # Отрисовка игрока
        screen.blit(current_sprite, player_pos)

        pygame.display.flip()
        clock.tick(60)  # Ограничение FPS

    pygame.quit()


if __name__ == "__main__":
    main()
