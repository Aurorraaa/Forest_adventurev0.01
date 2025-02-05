import pygame
import random
import json


class Ore:
    object_data = None

    def __init__(self, rect, ore_type, hp):
        self.rect = rect
        self.ore_type = ore_type
        self.hp = hp
        self.alive = True

        if Ore.object_data is None:
            try:
                with open("objects (2).json", encoding="utf-8") as f:
                    Ore.object_data = json.load(f)
            except FileNotFoundError:
                print("Файл objects (2).json не найден!")
                Ore.object_data = []
            except json.JSONDecodeError as e:
                print(f"Ошибка чтения JSON-файла: {e}")
                Ore.object_data = []

    def take_damage(self, damage):
        if self.alive:
            self.hp -= damage
            if self.hp <= 0:
                self.alive = False
                return self.drop_items()
            return None

    def drop_items(self):
        item_id_map = {
            "coal": "coal",
            "iron": "iron_ore",
            "demonic": "demonic_ore",
            "diamonds": "diamond"
        }

        item_id = item_id_map.get(self.ore_type)
        if not item_id:
            print(f"Ошибка: Неизвестный тип руды '{self.ore_type}")
            return []


        item_data = next((item for item in Ore.object_data if item["id"] == item_id), None)
        if not item_data:
            print(f"Ошибка: Не найдено описание предмета для id '{item_id}'")
            return []

        quantity = random.randint(3,5)

        return [{
            "id": item_data["id"],
            "name": item_data["name"],
            "icon_path": item_data["icon_path"],
            "quantity": quantity,
            "price": item_data.get("price", 0),
            "max_stack": item_data.get("max_stack", 1),
            "description": item_data.get("description", "")
        }]

    def draw(self, screen, camera):
        if self.alive:
            pygame.draw.rect(screen, (255, 255, 255), camera.apply(self.rect), 1)
