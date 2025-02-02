import pygame
import json
import random as rnd
from invent import Inventory


class Chest:
    def __init__(self, rect):
        self.rect = rect  # Область сундука на карте
        self.inventory = Inventory()  # Каждый сундук имеет свой инвентарь
        self.is_populated = False  # Флаг, чтобы заполнение происходило один раз

    def populate_random_items(self, possible_item_ids, json_path):
        """
        Заполняет инвентарь сундука случайными предметами.
        possible_item_ids — список идентификаторов (например, ["wood", "coal_ore", ...]),
        json_path — путь к JSON-файлу с описанием предметов.
        """
        if self.is_populated:
            return  # Если сундук уже заполнен, повторное заполнение не нужно

        try:
            with open(json_path, "r") as file:
                items = json.load(file)
            # Создаём словарь для быстрого доступа: id -> данные предмета
            items_catalog = {item["id"]: item for item in items}
        except Exception as e:
            print(f"Ошибка загрузки предметов из JSON: {e}")
            return

        # Выбираем случайное количество предметов: 3 или 4
        num_items = rnd.randint(3, 4)
        available_ids = possible_item_ids.copy()
        if len(available_ids) < num_items:
            num_items = len(available_ids)
        selected_ids = rnd.sample(available_ids, num_items)

        for item_id in selected_ids:
            if item_id in items_catalog:
                item = items_catalog[item_id]
                # Добавляем предмет в инвентарь сундука
                # В метод add_item передаются: название, путь к иконке, цена
                self.inventory.add_item(item["name"], item["icon_path"], item.get("price", 0))
            else:
                print(f"Предмет с id '{item_id}' не найден в JSON.")
        self.is_populated = True

    def open_chest(self, player_inventory, screen, clock):
        """
        Открывает окно взаимодействия с сундуком.
        Отображаются две панели:
          левая – инвентарь сундука,
          правая – инвентарь игрока.
        Для закрытия нажмите ESC или E.
        """
        # Задаём области для двух панелей
        chest_panel_rect = pygame.Rect(50, 50, 300, 300)
        player_panel_rect = pygame.Rect(400, 50, 300, 300)
        self.inventory.bg_rect = chest_panel_rect
        player_inventory.bg_rect = player_panel_rect

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_e):
                        running = False

                # Обработка событий drag & drop для обоих инвентарей
                self.inventory.process_event(event)
                player_inventory.process_event(event)

            screen.fill((50, 50, 50))
            pygame.draw.rect(screen, (200, 200, 200), chest_panel_rect, 2)
            pygame.draw.rect(screen, (200, 200, 200), player_panel_rect, 2)
            self.inventory.draw_slots(screen)
            player_inventory.draw_slots(screen)
            pygame.display.flip()
            clock.tick(60)