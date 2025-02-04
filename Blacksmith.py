from invent import Inventory
import json


class Blacksmith():
    def __init__(self, name):
        self.name = name
        self.inventory = Inventory()
        self.coins = float("inf")

    def load_items_from_json(self, json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as file:
                items = json.load(file)

            self.items_catalog = {item["id"]: item for item in items}
        except FileNotFoundError:
            print(f"Файл {json_path} не найден!")
            self.items_catalog = {}
        except json.JSONDecodeError as e:
            print(f"Ошибка чтения JSON-файла: {e}")
            self.items_catalog = {}
        except Exception as e:
            print(f"Неизвестная ошибка при загрузке JSON: {e}")
            self.items_catalog = {}

    def add_item_for_sale(self, item_id):
        item = self.items_catalog.get(item_id)
        if item:
            self.inventory.add_item(
                item["name"],
                item["icon_path"],
                item.get("price", 100),
                description=item.get("description", ""),
                damage=item.get("damage", 0),
                max_stack = item.get("max_stack", 1),
                quantity = item.get("current_stack", 1)
            )
        else:
            print(f"Предмет с id '{item_id}' не найден в каталоге.")

    def buy_from_player(self, item, player):
        buy_price = item.get("price", 0)
        if self.coins >= buy_price:
            self.coins -= buy_price
            player.coins += buy_price
            self.inventory.add_existing_item(item)
            player.inventory.remove_existing_item(item)

    def sell_to_player(self, item, player):
        sell_price = item.get("price", 0)
        if player.coins >= sell_price:
            # игрок платит торговцу
            player.coins -= sell_price
            self.coins += sell_price
            # передаём предмет игроку
            self.inventory.remove_existing_item(item)
            player.inventory.add_existing_item(item)
        else:
            print("Hедостаточно монет!")
