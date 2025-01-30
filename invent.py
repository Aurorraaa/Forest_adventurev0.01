import sys
import pygame


class Inventory:
    def __init__(self):
        self.items = []
        self.inventory_bg = pygame.image.load("Data/invent.png").convert_alpha()
        self.bg_rect = self.inventory_bg.get_rect()

    def add_item(self, item_name, icon_path):
        self.items.append({
            "name" : item_name,
            "icon" : pygame.image.load(icon_path).convert_alpha()
        })

    def remove_item(self, item_name):
        for item in self.items:
            if item["name"] == item_name:
                self.items.remove(item)
                break

    def show_inventory(self, screen, clock):
        font = pygame.font.Font(None, 36)
        background_surf = screen.copy()
        overlay = pygame.Surface(screen.get_size())
        overlay.set_alpha(180)
        overlay.fill((50, 50, 50))
        self.bg_rect.center = (screen.get_width() // 2, screen.get_height() // 2)
        runin = True

        while runin:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e or event.key == pygame.K_ESCAPE:
                        runin = False

            screen.blit(background_surf, (0, 0))
            screen.blit(overlay, (0, 0))
            screen.blit(self.inventory_bg, self.bg_rect)
            title_surf = font.render("INVENTORY", True, (255, 255, 255))
            screen.blit(title_surf, (self.bg_rect.x + 20, self.bg_rect.y + 20))

            slot_positions = [
                (30, 30), (90, 30), (150, 30), (210, 30),
                (30, 80), (90, 140), (150, 140), (210, 140)
            ]

            for i, item in enumerate(self.items[:8]):
                slot_x, slot_y = slot_positions[i]
                # абсолютная позиция на экране:
                abs_x = self.bg_rect.x + slot_x
                abs_y = self.bg_rect.y + slot_y
                icon_surf = item["icon"]
                screen.blit(icon_surf, (abs_x, abs_y))

            pygame.display.flip()
            clock.tick(60)

        return