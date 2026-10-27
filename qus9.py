
class Inventory:
    def __init__(self):
        self.items = {}

    def add_item(self, name, quantity):
        self.items[name] = self.items.get(name, 0) + quantity

    def merge(self, other):
        result = Inventory()
        result.items = self.items.copy()

        for name, quantity in other.items.items():
            result.add_item(name, quantity)

        return result

    def display(self):
        for name in sorted(self.items):
            print(name, self.items[name])


n = int(input())
inventory1 = Inventory()

for _ in range(n):
    name, quantity = input().split()
    inventory1.add_item(name, int(quantity))

m = int(input())
inventory2 = Inventory()

for _ in range(m):
    name, quantity = input().split()
    inventory2.add_item(name, int(quantity))

merged = inventory1.merge(inventory2)
merged.display()
