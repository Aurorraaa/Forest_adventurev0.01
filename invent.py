import sys
import pygame


class Inventory:
    def __init__(self):
        self.items = []
        self.inventory_bg = pygame.image.load("Data/invent.png").convert_alpha()
        self.bg_rect = self.inventory_bg.get_rect()
        self.slots = []
        self.slot_positions = [(16, 18), (68, 18), (118, 18), (168, 18), (220, 18), (270, 18), (320, 18), (370, 18),
                               (16, 68), (68, 68), (118, 68), (168, 68), (220, 68), (270, 68), (320, 68), (370, 68),
                               (16, 118), (68, 118), (118, 118), (168, 118), (220, 118), (270, 118), (320, 118),
                               (370, 118),
                               (16, 168), (68, 168), (118, 168), (168, 168), (220, 168), (270, 168), (320, 168),
                               (370, 168),
                               (16, 218), (68, 218), (118, 218), (168, 218), (220, 218), (270, 218), (320, 218),
                               (370, 218)
                               ]
        self.slot_width, self.slot_height = 48, 48
        for pos in self.slot_positions:
            self.x, self.y = pos
            r = pygame.Rect(self.x, self.y, self.slot_width, self.slot_height)
            self.slots.append({
                "rect": r,
                "item": None
            })

        self.dragging_item = None
        self.dragging_from = None
        self.drag_offset = (0, 0)
        self.drag_pos = (0, 0)

    def add_item(self, item_name, icon_path, price=0):
        self.icon_surf = pygame.image.load(icon_path).convert_alpha()
        self.new_item = {
            "name": item_name,
            "icon": self.icon_surf,
            "price" : price,
            "sell_price" : price // 2
        }
        for slot in self.slots:
            if slot["item"] is None:
                slot["item"] = self.new_item
                return

    def remove_item(self, item_name):
        for slot in self.slots:
            if slot["item"] is not None and slot["item"]["name"] == item_name:
                slot["item"] = None
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
                    if event.key in [pygame.K_e, pygame.K_ESCAPE]:
                        runin = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.handle_mouse_down(event.pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:  # ЛКМ
                        self.handle_mouse_up(event.pos)
                elif event.type == pygame.MOUSEMOTION:
                    self.handle_mouse_motion(event.pos)

            screen.blit(background_surf, (0, 0))
            screen.blit(overlay, (0, 0))
            screen.blit(self.inventory_bg, self.bg_rect)

            self.draw_slots(screen)

            if self.dragging_item is not None:
                self.icon = self.dragging_item["icon"]
                self.draw_x = self.drag_pos[0] - self.drag_offset[0]
                self.draw_y = self.drag_pos[1] - self.drag_offset[1]
                screen.blit(self.icon, (self.draw_x, self.draw_y))

            pygame.display.flip()
            clock.tick(60)
        return

    def draw_slots(self, screen):
        for slot in self.slots:
            # Абсолютная позиция слота:
            abs_x = self.bg_rect.x + slot["rect"].x
            abs_y = self.bg_rect.y + slot["rect"].y
            rect_abs = pygame.Rect(abs_x, abs_y, slot["rect"].width, slot["rect"].height)

            # Рисуем рамку слота (для наглядности)
            pygame.draw.rect(screen, (200, 200, 200), rect_abs, 2)

            # Если в слоте есть предмет и мы его не тащим
            if slot["item"] is not None:
                # Проверим, не является ли он тем, который сейчас тащим
                # (вдруг пользователь кликнул и убрал предмет из слота)
                if slot["item"] != self.dragging_item:
                    icon = slot["item"]["icon"]
                    icon_rect = icon.get_rect(center=rect_abs.center)
                    screen.blit(icon, icon_rect)

    def handle_mouse_down(self, mouse_pos):
        # Если уже что-то тащим - игнорируем
        if self.dragging_item is not None:
            return

        # Проверяем, попали ли мы в слот
        for i, slot in enumerate(self.slots):
            abs_x = self.bg_rect.x + slot["rect"].x
            abs_y = self.bg_rect.y + slot["rect"].y
            rect_abs = pygame.Rect(abs_x, abs_y, slot["rect"].width, slot["rect"].height)

            if rect_abs.collidepoint(mouse_pos):
                # Слот найден. Есть ли там предмет?
                if slot["item"] is not None:
                    # Берём этот предмет
                    self.dragging_item = slot["item"]
                    self.dragging_from = i
                    slot["item"] = None  # убрали из слота

                    # drag_offset, чтобы иконка не "прыгала"
                    icon_rect = self.dragging_item["icon"].get_rect(center=rect_abs.center)
                    dx = mouse_pos[0] - icon_rect.x
                    dy = mouse_pos[1] - icon_rect.y
                    self.drag_offset = (dx, dy)
                    self.drag_pos = mouse_pos
                break

    def handle_mouse_motion(self, mouse_pos):
        if self.dragging_item is not None:
            self.drag_pos = mouse_pos

    def handle_mouse_up(self, mouse_pos):
        if self.dragging_item is None:
            return

        # Проверяем, попали ли в другой слот
        dropped_in_slot = False
        for i, slot in enumerate(self.slots):
            abs_x = self.bg_rect.x + slot["rect"].x
            abs_y = self.bg_rect.y + slot["rect"].y
            rect_abs = pygame.Rect(abs_x, abs_y, slot["rect"].width, slot["rect"].height)

            if rect_abs.collidepoint(mouse_pos):
                # Если пустой слот - кладём туда
                if slot["item"] is None:
                    slot["item"] = self.dragging_item
                else:
                    # Слот занят - сделаем swap
                    old_item = slot["item"]
                    slot["item"] = self.dragging_item
                    # Предмет, который там был, возвращаем в исходный слот
                    self.slots[self.dragging_from]["item"] = old_item
                dropped_in_slot = True
                break

        if not dropped_in_slot:
            # не попали в слот - вернём предмет на место
            self.slots[self.dragging_from]["item"] = self.dragging_item

        # Завершаем перетаскивание
        self.dragging_item = None
        self.dragging_from = None
        self.drag_offset = (0, 0)
        self.drag_pos = (0, 0)



    def add_existing_item(self, item):
        for slot in self.slots:
            if slot["item"] is None:
                slot["item"] = item
                return
        print("Нет свободных слотов!")

    def remove_existing_item(self, item):
        for slot in self.slots:
            if slot["item"] == item:
                slot["item"] = None
                return
        print("Не нашли предмет в инвентаре.")

    def get_all_items(self):
        all_items = []
        for slot in self.slots:
            if slot["item"] is not None:
                all_items.append(slot["item"])
        return all_items

    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.handle_mouse_down(event.pos)
        elif event.type == pygame.MOUSEMOTION:
            self.handle_mouse_motion(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.handle_mouse_up(event.pos)