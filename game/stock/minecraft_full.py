#!/usr/bin/env python3
"""minecraft_full.py
Full playable Minecraft-inspired game prototype.
"""

import json
import random
from pathlib import Path
from typing import Dict, Any

from game.stock.minecraft.constants import BLOCKS, WORLD_SIZES, GAME_BALANCE
from game.stock.minecraft.world import World
from game.stock.minecraft.player import Player
from game.stock.minecraft.crafting import CraftingTable
from game.stock.minecraft.items import Inventory, Item


class MinecraftGame:
    def __init__(self, save_file: str = "minecraft_save.json"):
        self.save_file = Path(save_file)
        self.player = Player(1, 1, GAME_BALANCE["player_hp"])
        self.world = World(28, 28, "base28")
        self.inventory = Inventory()
        self.zone = "base28"
        self.running = True
        self.state = self.load_or_init()

    def load_or_init(self) -> Dict[str, Any]:
        if self.save_file.exists():
            with self.save_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
                self.player.x = data["player"]["x"]
                self.player.y = data["player"]["y"]
                self.player.hp = data["player"]["hp"]
                self.player.level = data["player"]["level"]
                self.player.experience = data["player"]["experience"]
                self.player.hunger = data["player"]["hunger"]
                self.zone = data["zone"]
                self.world = World(WORLD_SIZES[self.zone]["width"], WORLD_SIZES[self.zone]["height"], self.zone)
                return data
        return self.new_game()

    def new_game(self) -> Dict[str, Any]:
        self.inventory.add(Item("wood", "resource", emoji="🪵"))
        self.inventory.add(Item("wood", "resource", emoji="🪵"))
        self.inventory.add(Item("torch", "utility", emoji="🔥"))
        return {
            "player": {
                "x": self.player.x,
                "y": self.player.y,
                "hp": self.player.hp,
                "level": self.player.level,
                "experience": self.player.experience,
                "hunger": self.player.hunger,
            },
            "zone": self.zone,
            "inventory": self.inventory.to_dict(),
        }

    def save(self):
        self.state = {
            "player": {
                "x": self.player.x,
                "y": self.player.y,
                "hp": self.player.hp,
                "level": self.player.level,
                "experience": self.player.experience,
                "hunger": self.player.hunger,
            },
            "zone": self.zone,
            "inventory": self.inventory.to_dict(),
        }
        with self.save_file.open("w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=2)
        print(f"💾 Saved to {self.save_file}")

    def display_status(self):
        print(f"\n{'='*60}\n")
        print(f"📍 Zone: {self.zone.upper()} ({self.world.width}x{self.world.height})")
        print(f"👤 {self.player.status()}")
        print(f"{'='*60}\n")

    def show_inventory(self):
        print("\n📦 Inventory:")
        counts = {}
        for item in self.inventory.items:
            counts[item.name] = counts.get(item.name, 0) + 1
        for name, count in counts.items():
            print(f"  {count}x {name}")

    def mine_block(self):
        tile = self.world.grid[self.player.y][self.player.x]
        if tile not in BLOCKS or tile == "grass":
            print("❌ Nothing to mine here!")
            return
        info = BLOCKS[tile]
        if random.random() < GAME_BALANCE["drop_rate"] and info["drop"]:
            self.inventory.add(Item(info["drop"], "resource"))
            print(f"✓ Mined {tile} and got {info['drop']}")
        else:
            print(f"❌ Could not mine {tile}")

    def craft(self, recipe_name: str):
        recipe = CraftingTable.find_recipe(recipe_name)
        if not recipe:
            print(f"❌ Unknown recipe: {recipe_name}")
            return

        counts = {}
        for item in self.inventory.items:
            counts[item.name] = counts.get(item.name, 0) + 1

        if not recipe.can_craft(counts):
            print(f"❌ Not enough ingredients for {recipe_name}")
            return

        for item_name, qty in recipe.inputs.items():
            removed = 0
            for i in reversed(range(len(self.inventory.items))):
                if self.inventory.items[i].name == item_name and removed < qty:
                    self.inventory.items.pop(i)
                    removed += 1

        for _ in range(recipe.output_qty):
            self.inventory.add(Item(recipe.output, "crafted"))

        print(f"✓ Crafted {recipe.output_qty}x {recipe.output}")

    def move_player(self, direction: str):
        moves = {
            "north": (0, -1),
            "south": (0, 1),
            "east": (1, 0),
            "west": (-1, 0),
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0),
        }
        if direction not in moves:
            print("❌ Direction must be north/south/east/west")
            return

        dx, dy = moves[direction]
        new_x = self.player.x + dx
        new_y = self.player.y + dy

        if 0 <= new_x < self.world.width and 0 <= new_y < self.world.height:
            self.player.x = new_x
            self.player.y = new_y
            self.player.hunger = max(0, self.player.hunger - 1)
            print(f"✓ Moved to ({self.player.x}, {self.player.y})")
        else:
            print("❌ Border reached!")

    def render_map(self):
        print(self.world.render(self.player.x, self.player.y))

    def show_recipes(self):
        print("\n" + CraftingTable.list_recipes())

    def advance_zone(self, zone_name: str):
        if zone_name not in WORLD_SIZES:
            print(f"❌ zone {zone_name} not valid")
            return
        self.zone = zone_name
        size = WORLD_SIZES[zone_name]
        self.world = World(size["width"], size["height"], zone_name)
        self.player.x = 1
        self.player.y = 1
        self.player.level += 1
        print(f"✨ Advanced to {zone_name}")

    def show_help(self):
        print("""
╔════════════════════════════════════════╗
║     MINECRAFT INSPIRED GAME          ║
╚════════════════════════════════════════╝

Commands:
  move north|south|east|west
  mine
  inventory
  recipes
  craft wooden_pickaxe
  advance base28|base44x48|base64
  map
  status
  save
  quit
        """)

    def run(self):
        print("\n🎮 Welcome to the Minecraft-inspired prototype!")
        self.display_status()
        self.render_map()
        self.show_help()

        while self.running:
            try:
                cmd = input("\n> ").strip().lower()

                if not cmd:
                    continue

                if cmd in ["quit", "exit"]:
                    self.running = False
                    print("👋 Goodbye!")

                elif cmd == "status":
                    self.display_status()

                elif cmd == "map":
                    self.render_map()

                elif cmd == "inventory":
                    self.show_inventory()

                elif cmd == "recipes":
                    self.show_recipes()

                elif cmd == "mine":
                    self.mine_block()
                    self.render_map()

                elif cmd.startswith("move "):
                    direction = cmd.split()[1]
                    self.move_player(direction)
                    self.render_map()

                elif cmd.startswith("craft "):
                    recipe_name = cmd.split()[1]
                    self.craft(recipe_name)
                    self.show_inventory()

                elif cmd.startswith("advance "):
                    zone = cmd.split()[1]
                    self.advance_zone(zone)
                    self.render_map()

                elif cmd == "save":
                    self.save()

                elif cmd == "help":
                    self.show_help()

                else:
                    print("❓ Unknown command. Type 'help'.")
            except KeyboardInterrupt:
                print("\n\n⚠️ Interrupted.")
                self.running = False


if __name__ == "__main__":
    game = MinecraftGame("minecraft_save.json")
    game.run()
