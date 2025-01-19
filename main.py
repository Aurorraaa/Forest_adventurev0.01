import pygame
import pytmx


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, file):
        super().__init__()

        self.image = pygame.image.load(file).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

        self.dx = 0
        self.dy = 0

        self.go = False
        self.Frame = 0
        self.last_direction = "right"

        self.pers_right = [pygame.image.load(
            f"Data/gg_sprites/right/{f}").convert_alpha() for f in
                           ["0 (2).png", "1 (2).png", "2 (2).png", "3 (2).png", "4 (2).png", "5 (2).png", "0.png",
                            "1.png", "2.png", "3.png", "4.png", "5.png", "6.png", "7.png", "8.png", "9.png",
                            "10.png", "11.png", "12.png", "13.png", "14.png", "15.png", "16.png", "17.png"]]

        self.pers_left = [pygame.image.load(
            f"Data/gg_sprites/left/{f}").convert_alpha() for f in
                          ["image_0-23.png", "image_0-22.png", "image_0-21.png", "image_0-20.png", "image_0-19.png",
                           "image_0-18.png", "image_0-17.png", "image_0-16.png", "image_0-15.png", "image_0-14.png",
                           "image_0-13.png", "image_0-12.png", "image_0-11.png", "image_0-10.png", "image_0-9.png",
                           "image_0-8.png", "image_0-7.png", "image_0-6.png", "image_0-5.png", "image_0-4.png",
                           "image_0-3.png", "image_0-2.png", "image_0-1.png", "image_0-0.png"]]

        self.idle_right_frames = ["image_0-0.png", "image_0-1.png", "image_0-2.png", "image_0-3.png", "image_0-4.png",
                                  "image_0-5.png", "image_0-6.png", "image_0-7.png", "image_0-8.png", "image_0-9.png",
                                  "image_0-10.png", "image_0-11.png", "image_0-12.png", "image_0-13.png",
                                  "image_0-14.png",
                                  "image_0-15.png", "image_0-16.png", "image_0-17.png"]

        self.idle_left_frames = ["image_0-0.png", "image_0-1.png", "image_0-2.png", "image_0-3.png", "image_0-4.png",
                                 "image_0-5.png", "image_0-6.png", "image_0-7.png", "image_0-8.png", "image_0-9.png",
                                 "image_0-10.png", "image_0-11.png", "image_0-12.png", "image_0-13.png",
                                 "image_0-14.png",
                                 "image_0-15.png", "image_0-16.png", "image_0-17.png"]

    def update(self, *args):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.go:
            self.Frame += 0.4
            if self.dx != 0:
                if self.Frame >= len(self.pers_right):
                    self.Frame = 0

            if self.dx > 0:
                self.animate_right()
                self.last_direction = "right"
            elif self.dx < 0:
                self.animate_left()
                self.last_direction = "left"
        else:
            self.animate_idle()

    def animate_right(self):

        self.image = self.pers_right[int(self.Frame) % len(self.pers_right)]

    def animate_left(self):

        self.image = self.pers_left[int(self.Frame) % len(self.pers_left)]

    def animate_idle(self):

        self.Frame += 0.125
        if self.Frame >= len(self.idle_left_frames):
            self.Frame = 0
        if self.last_direction == "right":
            self.image = pygame.image.load(
                "Data/gg_sprites/idle/" + self.idle_right_frames[int(self.Frame)]).convert_alpha()
        elif self.last_direction == "left":
            self.image = pygame.image.load(
                "Data/gg_sprites/idle_left/" + self.idle_left_frames[int(self.Frame)]).convert_alpha()

    def start_animation(self):
        self.go = True

    def stop_animation(self):
        self.go = False


class Camera:
    def __init__(self, width, height, map_width, map_height):
        self.offset = pygame.Vector2(0, 0)
        self.width = width
        self.height = height
        self.map_width = map_width
        self.map_height = map_height

    def apply(self, rect):
        return rect.move(-self.offset)

    def apply_pos(self, pos):
        return pos[0] - self.offset.x, pos[1] - self.offset.y

    def update(self, target_rect):
        self.offset.x = target_rect.centerx - self.width // 2
        self.offset.y = target_rect.centery - self.height // 2

        self.offset.x = max(0, min(self.offset.x, self.map_width - self.width))
        self.offset.y = max(0, min(self.offset.y, self.map_height - self.height))


def render_map(tmx_data):
    tile_width = tmx_data.tilewidth
    tile_height = tmx_data.tileheight
    map_width = tmx_data.width * tile_width
    map_height = tmx_data.height * tile_height

    map_surface = pygame.Surface((map_width, map_height))
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    map_surface.blit(tile, (x * tile_width, y * tile_height))
    return map_surface


def main():
    pygame.init()
    SIZE = WIDTH, HEIGHT = 800, 600
    FPS = 60
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Forest Adventure")

    try:
        tmx_data = pytmx.load_pygame("Data/mapp/new_mapa.tmx")
        map_surface = render_map(tmx_data)
    except Exception as e:
        print(f"Ошибка загрузки карты: {e}")
        return
    map_width = tmx_data.width * tmx_data.tilewidth
    map_height = tmx_data.height * tmx_data.tileheight

    spawn_x, spawn_y = 4650, 4625
    camera = Camera(WIDTH, HEIGHT, map_width, map_height)
    player = Object(spawn_x, spawn_y, "Data/gg_sprites/idle/image_0-0.png")

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
        camera.update(player.rect)
        screen.fill((0, 0, 0))
        screen.blit(map_surface, camera.apply_pos((0, 0)))
        screen.blit(player.image, camera.apply(player.rect))
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == "__main__":
    main()
