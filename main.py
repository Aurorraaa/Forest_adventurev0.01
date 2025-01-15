import pygame
import pytmx

pygame.init()


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, file):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(file).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

        self.dx = 0
        self.dy = 0

        self.go = False
        self.Frame = 0

        self.pers_right = ["0 (2).png", "1 (2).png", "2 (2).png", "3 (2).png", "4 (2).png", "5 (2).png", "0.png",
                           "1.png", "2.png", "3.png", "4.png", "5.png", "6.png", "7.png", "8.png", "9.png",
                           "10.png", "11.png", "12.png", "13.png", "14.png", "15.png", "16.png", "17.png"]

        self.pers_left = ["image_0-23.png", "image_0-22.png", "image_0-21.png", "image_0-20.png", "image_0-19.png",
                          "image_0-18.png", "image_0-17.png", "image_0-16.png", "image_0-15.png", "image_0-14.png",
                          "image_0-13.png", "image_0-12.png", "image_0-11.png", "image_0-10.png", "image_0-9.png",
                          "image_0-8.png", "image_0-7.png", "image_0-6.png", "image_0-5.png", "image_0-4.png",
                          "image_0-3.png", "image_0-2.png", "image_0-1.png", "image_0-0.png"]

        self.idle_frames = ["image_0-0.png", "image_0-1.png", "image_0-2.png", "image_0-3.png", "image_0-4.png",
                            "image_0-5.png", "image_0-6.png", "image_0-7.png", "image_0-8.png", "image_0-9.png",
                            "image_0-10.png", "image_0-11.png", "image_0-12.png", "image_0-13.png", "image_0-14.png",
                            "image_0-15.png", "image_0-16.png", "image_0-17.png"]

    def update(self, *args):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.go:
            self.Frame += 0.4
            if self.dx != 0:
                if self.Frame >= len(self.pers_right):
                    self.Frame = 0

            if self.dx > 0:  # Движение вправо
                self.animate_right()
            elif self.dx < 0:  # Движение влево
                self.animate_left()
        else:
            self.animate_idle()

    def animate_right(self):
        """Анимация движения вправо"""
        self.image = pygame.image.load(
            "Data/gg_sprites/right/" + self.pers_right[int(self.Frame) % len(self.pers_right)]).convert_alpha()

    def animate_left(self):
        """Анимация движения влево"""
        self.image = pygame.image.load(
            "Data/gg_sprites/left/" + self.pers_left[int(self.Frame) % len(self.pers_left)]).convert_alpha()

    def animate_idle(self):
        """Анимация ожидания"""
        self.Frame += 0.125
        if self.Frame >= len(self.idle_frames):
            self.Frame = 0
        self.image = pygame.image.load(
            "Data/gg_sprites/idle/" + self.idle_frames[int(self.Frame)]).convert_alpha()

    def start_animation(self):
        self.go = True

    def stop_animation(self):
        self.go = False


SIZE = WIDTH, HEIGHT = 800, 600
FPS = 60
clock = pygame.time.Clock()


def main():
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
    player = Object(100, 400, "Data/gg_sprites/idle/image_0-0.png")
    flrunning = True

    while flrunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flrunning = False

        key = pygame.key.get_pressed()
        player.dx = 0
        player.dy = 0

        if key[pygame.K_d]:
            player.dx = 5
            player.start_animation()
        elif key[pygame.K_a]:
            player.dx = -5
            player.start_animation()
        elif key[pygame.K_w]:
            player.dy = -5
            player.start_animation()
        elif key[pygame.K_s]:
            player.dy = 5
            player.start_animation()
        else:
            player.stop_animation()
            player.animate_idle()

        player.update()
        screen.fill((0, 0, 0))
        screen.blit(player.image, player.rect)
        # # Отображаем фон и тайлы
        # screen.fill((0, 0, 0))  # Очистка экрана перед отрисовкой
        # for layer in tmx_data.visible_layers:
        #     if isinstance(layer, pytmx.TiledTileLayer):
        #         for x, y, gid in layer:
        #             tile = tmx_data.get_tile_image_by_gid(gid)
        #             if tile:
        #                 screen.blit(tile, (x * tile_width, y * tile_height))
        #

        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()


if __name__ == "__main__":
    main()
