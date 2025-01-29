import sys
import pygame
import pytmx

from menu import show_main_menu, show_settings_menu


class Map:
    def __init__(self, tmx_file):
        self.tmx_map = pytmx.load_pygame(tmx_file)

        self.lower_layers = ["ground", "grass", "paths"]
        self.upper_layers = ["ores", "props", "symbs", "houses", "landscape"]
        self.collision_layer_name = "collision"

        # Создаем словари для слоев
        self.precomputed_layers = {
            "lower": [],
            "upper": [],
            "collision": []
        }

        # Подготовка данных о тайлах
        for layer in self.tmx_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                layer_name = layer.name
                if layer_name in self.lower_layers:
                    target_list = self.precomputed_layers["lower"]
                elif layer_name in self.upper_layers:
                    target_list = self.precomputed_layers["upper"]
                else:
                    continue

                for x, y, gid in layer:
                    tile_image = self.tmx_map.get_tile_image_by_gid(gid)
                    if tile_image:
                        # Сохраняем данные о тайле
                        target_list.append({
                            "image": tile_image,
                            "rect": pygame.Rect(
                                x * self.tmx_map.tilewidth,
                                y * self.tmx_map.tileheight,
                                self.tmx_map.tilewidth,
                                self.tmx_map.tileheight
                            )
                        })
            elif isinstance(layer, pytmx.TiledObjectGroup):
                if layer.name == self.collision_layer_name:
                    for obj in layer:
                        self.precomputed_layers["collision"].append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

    def draw(self, screen, player, camera):
        view_rect = pygame.Rect(camera.offset.x, camera.offset.y, screen.get_width(), screen.get_height())

        # Рисуем нижние слои
        for tile in self.precomputed_layers["lower"]:
            if view_rect.colliderect(tile["rect"]):
                screen.blit(tile["image"], camera.apply(tile["rect"]))

        # Рисуем игрока
        screen.blit(player.image, camera.apply(player.rect))

        # Рисуем верхние слои
        for tile in self.precomputed_layers["upper"]:
            if view_rect.colliderect(tile["rect"]):
                screen.blit(tile["image"], camera.apply(tile["rect"]))

    def check_collision(self, rect):
        for obj_rect in self.precomputed_layers["collision"]:
            if rect.colliderect(obj_rect):
                return True
        return False


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, file):
        super().__init__()

        self.image = pygame.image.load(file).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        # self.rect.inflate_ip(-20, -20)

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

        self.idle_right_surfaces = [
            pygame.image.load(f"Data/gg_sprites/idle/{file}").convert_alpha()
            for file in self.idle_right_frames
        ]

        self.idle_left_surfaces = [
            pygame.image.load(f"Data/gg_sprites/idle_left/{file}").convert_alpha()
            for file in self.idle_left_frames
        ]

    def update(self, *args):
        original_rect = self.rect.copy()

        self.rect.x += self.dx
        if args[0].check_collision(self.rect):
            self.rect.x = original_rect.x

        self.rect.y += self.dy
        if args[0].check_collision(self.rect):
            self.rect.y = original_rect.y

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
        if self.Frame >= len(self.idle_left_surfaces):
            self.Frame = 0
        self.frame_index = int(self.Frame)
        if self.last_direction == "right":
            self.image = self.idle_right_surfaces[self.frame_index]
        elif self.last_direction == "left":
            self.image = self.idle_left_surfaces[self.frame_index]

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


def main_game(screen, clock, volume):
    WIDTH, HEIGHT = 800, 600
    FPS = 60
    pygame.display.set_caption("Forest Adventure")

    try:
        tmx_data = pytmx.load_pygame("Data/mapp/new_mapa.tmx")
    except Exception as e:
        print(f"Ошибка загрузки карты: {e}")
        return

    map_width = tmx_data.width * tmx_data.tilewidth
    map_height = tmx_data.height * tmx_data.tileheight

    spawn_x, spawn_y = 4650, 4625
    camera = Camera(WIDTH, HEIGHT, map_width, map_height)
    player = Object(spawn_x, spawn_y, "Data/gg_sprites/idle/image_0-0.png")

    tile_map = Map("Data/mapp/new_mapa.tmx")

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

        player.update(tile_map)
        camera.update(player.rect)
        pygame.mixer.music.set_volume(volume)

        # Можно использовать яркость как множитель для фона
        screen.fill((0, 0, 0))

        tile_map.draw(screen, player, camera)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
    sys.exit()


def main():
    pygame.init()
    SIZE = WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()

    volume = 0.5
    while True:
        choice = show_main_menu(screen, clock)
        if choice == "play":
            main_game(screen, clock, volume)
        elif choice == "settings":
            new_volume, command = show_settings_menu(screen, clock, volume)
            volume = new_volume
            if command == "back":
                continue

        elif choice == "quit":
            pygame.quit()
            sys.exit()


if __name__ == "__main__":
    main()
