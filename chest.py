import pygame
import json
import random as rnd
from invent import ChestInventory, Inventory


class Chest:
    def __init__(self, rect):
        self.rect = rect
        self.inventory = ChestInventory()
        self.is_populated = False

    def populate_random_items(self, possible_item_ids, json_path):
        if self.is_populated:
            return

        try:
            with open(json_path, "r", encoding="utf-8") as file:
                items = json.load(file)
            items_catalog = {item["id"]: item for item in items}
        except Exception as e:
            print(f"Ошибка загрузки предметов из JSON: {e}")
            return

        num_items = rnd.randint(2, 4)
        available_ids = possible_item_ids.copy()
        if len(available_ids) < num_items:
            num_items = len(available_ids)
        selected_ids = rnd.sample(available_ids, num_items)

        for item_id in selected_ids:
            if item_id in items_catalog:
                item = items_catalog[item_id]
                self.inventory.add_item(
                    item["name"],
                    item["icon_path"],
                    item.get("price", 0),
                    item.get("description", ""),
                    item.get("damage", 0),
                    item.get("max_stack", 1),
                    1
                )
            else:
                print(f"Предмет с id '{item_id}' не найден в JSON.")
        self.is_populated = True

    def open_chest(self, player_inventory, screen, clock):
        player_inventory.bg_rect.topleft = (50, 300)
        self.inventory.bg_rect.topleft = (50, 50)
        running = True
        while running:
            screen.fill((50, 50, 50))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_e):
                        running = False

                self.handle_drag_event(self.inventory, player_inventory, event)
                self.handle_drag_event(player_inventory, self.inventory, event)

            screen.blit(player_inventory.inventory_bg, player_inventory.bg_rect.topleft)
            screen.blit(self.inventory.inventory_bg, self.inventory.bg_rect.topleft)

            player_inventory.draw_slots(screen)
            self.inventory.draw_slots(screen)

            mouse_pos = pygame.mouse.get_pos()
            player_inventory.show_tooltip(screen, mouse_pos)
            self.inventory.show_tooltip(screen, mouse_pos)

            if Inventory.dragging_item is not None:
                self.icon = Inventory.dragging_item["icon"]
                self.x, self.y = Inventory.drag_pos[0] - Inventory.drag_offset[0], Inventory.drag_pos[1] - \
                                 Inventory.drag_offset[1]
                screen.blit(self.icon, (self.x, self.y))
            pygame.display.flip()
            clock.tick(60)

    def handle_drag_event(self, source_inventory, target_inventory, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            for i, slot in enumerate(source_inventory.slots):
                rect_abs = pygame.Rect(
                    source_inventory.bg_rect.x + slot["rect"].x,
                    source_inventory.bg_rect.y + slot["rect"].y,
                    slot["rect"].width,
                    slot["rect"].height
                )
                if rect_abs.collidepoint(event.pos) and slot["item"] is not None:
                    Inventory.dragging_item = slot["item"]
                    Inventory.dragging_from = (source_inventory, i)
                    slot["item"] = None
                    icon_rect = Inventory.dragging_item["icon"].get_rect(center=rect_abs.center)
                    Inventory.drag_offset = (event.pos[0] - icon_rect.x, event.pos[1] - icon_rect.y)
                    Inventory.drag_pos = event.pos
                    break

        elif event.type == pygame.MOUSEMOTION:
            if Inventory.dragging_item is not None:
                Inventory.drag_pos = event.pos

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if Inventory.dragging_item is not None:
                dropped = False

                for i, slot in enumerate(target_inventory.slots):
                    rect_abs = pygame.Rect(
                        target_inventory.bg_rect.x + slot["rect"].x,
                        target_inventory.bg_rect.y + slot["rect"].y,
                        slot["rect"].width,
                        slot["rect"].height
                    )
                    if rect_abs.collidepoint(event.pos):
                        if (slot["item"] is not None and slot["item"]["name"] == Inventory.dragging_item["name"]):
                            free_space = slot["item"]["max_stack"] - slot["item"]["current_stack"]
                            if free_space > 0:
                                to_add = min(Inventory.dragging_item["current_stack"], free_space)
                                slot["item"]["current_stack"] += to_add
                                Inventory.dragging_item["current_stack"] -= to_add
                                if Inventory.dragging_item["current_stack"] == 0:
                                    Inventory.dragging_item = None
                                dropped = True
                                break
                            else:
                                # Если нет свободного места, можно сделать "swap"
                                old_item = slot["item"]
                                slot["item"] = Inventory.dragging_item
                                src_inv, src_index = Inventory.dragging_from
                                src_inv.slots[src_index]["item"] = old_item
                                dropped = True
                                break

                        if slot["item"] is None and Inventory.dragging_item is not None:
                            slot["item"] = Inventory.dragging_item
                            dropped = True
                            break

                        if not dropped:
                            old_item = slot["item"]
                            slot["item"] = Inventory.dragging_item
                            src_inv, src_index = Inventory.dragging_from
                            src_inv.slots[src_index]["item"] = old_item
                            dropped = True
                            break

                if not dropped:
                    src_inv, src_index = Inventory.dragging_from
                    src_inv.slots[src_index]["item"] = Inventory.dragging_item

                Inventory.dragging_item = None
                Inventory.dragging_from = None
                Inventory.drag_offset = (0, 0)
                Inventory.drag_pos = (0, 0)
