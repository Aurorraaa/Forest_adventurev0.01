from invent import Inventory
import json


class Blacksmith():
    def __init__(self, name):
        self.name = name
        self.inventory = Inventory()
        self.coins = float("inf")

    def load_items_from_json(self, json_path):
        try:
            with open(json_path, "r") as file:
                items = json.load(file)

            self.items_catalog = {item["id"]: item for item in items}
        except Exception as e:
            print(f"Ошибка загрузки предметов из JSON: {e}")

    def add_item_for_sale(self, item_id):
        item = self.items_catalog.get(item_id)
        if item:
            # Используем данные из каталога для добавления предмета в инвентарь
            self.inventory.add_item(item["name"], item["icon_path"], item.get("price", 100))
        else:
            print(f"Предмет с id '{item_id}' не найден в каталоге.")

    def buy_from_player(self, item, player):
        buy_price = item.get("sell_price", 0)
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
