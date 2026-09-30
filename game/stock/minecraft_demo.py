#!/usr/bin/env python3
"""game/stock/minecraft_demo.py
Small demo script using the Minecraft-inspired module.
"""

from game.stock.minecraft import World, Inventory, Item, ItemType

if __name__ == "__main__":
    world = World(12, 12, "base28")
    print(world.render(1, 1))
    inv = Inventory()
    inv.add(Item("pickaxe", "tool", power=2, emoji="⛏️"))
    inv.add(Item("torch", "utility", emoji="🔥"))
    print("\nInventory:")
    for entry in inv.list_items():
        print(entry)
