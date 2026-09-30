#!/usr/bin/env python3
"""
cone_game_enhanced.py

Enhanced exploration game with:
- Item system (equipment, consumables, artifacts)
- Polished procedural map generator
- Tile types and biome support
- Loot drops and item discovery
- Inventory management
"""

import json
import random
from pathlib import Path
from typing import Dict, Any, List, Tuple
from enum import Enum


class ItemType(Enum):
    WEAPON = "weapon"
    ARMOR = "armor"
    CONSUMABLE = "consumable"
    ARTIFACT = "artifact"
    MISCELLANEOUS = "misc"


class Item:
    def __init__(self, name: str, item_type: ItemType, rarity: str = "common", value: int = 10):
        self.name = name
        self.item_type = item_type
        self.rarity = rarity  # common, rare, epic, legendary
        self.value = value

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "type": self.item_type.value,
            "rarity": self.rarity,
            "value": self.value,
        }

    def __repr__(self):
        return f"{self.name} ({self.rarity})"


class ItemDatabase:
    """Predefined item catalog."""

    WEAPONS = [
        Item("Wooden Sword", ItemType.WEAPON, "common", 15),
        Item("Iron Sword", ItemType.WEAPON, "common", 25),
        Item("Steel Blade", ItemType.WEAPON, "rare", 50),
        Item("Legendary Excalibur", ItemType.WEAPON, "legendary", 500),
    ]

    ARMOR = [
        Item("Leather Armor", ItemType.ARMOR, "common", 20),
        Item("Iron Plate", ItemType.ARMOR, "common", 30),
        Item("Mithril Suit", ItemType.ARMOR, "rare", 60),
        Item("Dragon Scale Armor", ItemType.ARMOR, "legendary", 400),
    ]

    CONSUMABLES = [
        Item("Health Potion", ItemType.CONSUMABLE, "common", 10),
        Item("Mana Potion", ItemType.CONSUMABLE, "common", 10),
        Item("Super Potion", ItemType.CONSUMABLE, "rare", 30),
        Item("Elixir of Life", ItemType.CONSUMABLE, "epic", 100),
    ]

    ARTIFACTS = [
        Item("Crystal of Power", ItemType.ARTIFACT, "rare", 75),
        Item("Amulet of Wisdom", ItemType.ARTIFACT, "rare", 75),
        Item("Ring of Fortune", ItemType.ARTIFACT, "epic", 150),
        Item("Crown of Kings", ItemType.ARTIFACT, "legendary", 300),
    ]

    @staticmethod
    def get_random_by_rarity(rarity: str = None) -> Item:
        """Get random item, optionally filtered by rarity."""
        all_items = ItemDatabase.WEAPONS + ItemDatabase.ARMOR + ItemDatabase.CONSUMABLES + ItemDatabase.ARTIFACTS
        if rarity:
            all_items = [i for i in all_items if i.rarity == rarity]
        return random.choice(all_items)

    @staticmethod
    def get_random_weapon() -> Item:
        return random.choice(ItemDatabase.WEAPONS)

    @staticmethod
    def get_random_armor() -> Item:
        return random.choice(ItemDatabase.ARMOR)

    @staticmethod
    def get_random_consumable() -> Item:
        return random.choice(ItemDatabase.CONSUMABLES)


class MapGenerator:
    """Procedural map generator with terrain variety."""

    TILE_TYPES = {
        ".": ("floor", "🟩"),
        "#": ("wall", "🟫"),
        "~": ("water", "🟦"),
        "T": ("tree", "🌲"),
        "S": ("start", "⭐"),
        "C": ("chest", "📦"),
        "E": ("enemy", "👹"),
        "X": ("exit", "🚪"),
    }

    def __init__(self, width: int, height: int, zone: str = "base28"):
        self.width = width
        self.height = height
        self.zone = zone
        self.tiles = self.generate()

    def generate(self) -> List[List[str]]:
        """Generate a procedural map with terrain variety."""
        tiles = [["." for _ in range(self.width)] for _ in range(self.height)]

        # Add walls as borders
        for x in range(self.width):
            tiles[0][x] = "#"
            tiles[self.height - 1][x] = "#"
        for y in range(self.height):
            tiles[y][0] = "#"
            tiles[y][self.width - 1] = "#"

        # Generate terrain based on zone
        if self.zone == "base28":
            self._generate_forest(tiles)
        elif self.zone == "base44x48":
            self._generate_ruins(tiles)
        elif self.zone == "base64":
            self._generate_cavern(tiles)

        # Place start marker
        tiles[1][1] = "S"

        # Place random chests
        for _ in range(random.randint(3, 6)):
            x, y = random.randint(2, self.width - 3), random.randint(2, self.height - 3)
            if tiles[y][x] == ".":
                tiles[y][x] = "C"

        # Place random enemies
        for _ in range(random.randint(2, 4)):
            x, y = random.randint(2, self.width - 3), random.randint(2, self.height - 3)
            if tiles[y][x] == ".":
                tiles[y][x] = "E"

        # Place exit
        exit_x, exit_y = self.width - 2, self.height - 2
        tiles[exit_y][exit_x] = "X"

        return tiles

    def _generate_forest(self, tiles: List[List[str]]):
        """Base28: Forest biome with trees."""
        for _ in range(int(self.width * self.height * 0.15)):
            x, y = random.randint(2, self.width - 3), random.randint(2, self.height - 3)
            if tiles[y][x] == ".":
                tiles[y][x] = "T"

    def _generate_ruins(self, tiles: List[List[str]]):
        """Base44x48: Ruins biome with more walls and water."""
        # Add ruins (wall patterns)
        for _ in range(int(self.width * self.height * 0.2)):
            x, y = random.randint(2, self.width - 3), random.randint(2, self.height - 3)
            if tiles[y][x] == ".":
                tiles[y][x] = "#"

        # Add water features
        for _ in range(int(self.width * self.height * 0.1)):
            x, y = random.randint(2, self.width - 3), random.randint(2, self.height - 3)
            if tiles[y][x] == ".":
                tiles[y][x] = "~"

    def _generate_cavern(self, tiles: List[List[str]]):
        """Base64: Cavern biome with complex walls and water."""
        # Dense cavern layout
        for _ in range(int(self.width * self.height * 0.3)):
            x, y = random.randint(2, self.width - 3), random.randint(2, self.height - 3)
            if tiles[y][x] == ".":
                tiles[y][x] = "#"

        # Water paths
        for _ in range(int(self.width * self.height * 0.15)):
            x, y = random.randint(2, self.width - 3), random.randint(2, self.height - 3)
            if tiles[y][x] == ".":
                tiles[y][x] = "~"

    def render(self, px: int, py: int) -> str:
        """Render map with player position."""
        lines = []
        lines.append(f"╔{'═' * (self.width * 2 + 1)}╗")

        for y in range(self.height):
            line = "║ "
            for x in range(self.width):
                if x == px and y == py:
                    line += "@ "
                else:
                    tile = self.tiles[y][x]
                    _, emoji = self.TILE_TYPES.get(tile, ("unknown", "❓"))
                    line += emoji
            line += " ║"
            lines.append(line)

        lines.append(f"╚{'═' * (self.width * 2 + 1)}╝")
        return "\n".join(lines)

    def get_tile(self, x: int, y: int) -> str:
        """Get tile at position."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return "#"


class Inventory:
    """Player inventory system."""

    def __init__(self):
        self.items: List[Item] = []

    def add_item(self, item: Item):
        """Add item to inventory."""
        self.items.append(item)

    def remove_item(self, index: int) -> Item:
        """Remove item by index."""
        return self.items.pop(index)

    def list_items(self) -> str:
        """Format inventory for display."""
        if not self.items:
            return "Empty"
        return "\n".join([f"  {i+1}. {item} ({item.item_type.value})" for i, item in enumerate(self.items)])

    def to_dict(self) -> List[Dict[str, Any]]:
        return [item.to_dict() for item in self.items]


class ConeGameEnhanced:
    """Enhanced game with items and polished maps."""

    def __init__(self, save_file: str = "cone_save_enhanced.json"):
        self.save_file = Path(save_file)
        self.state = self.load_or_init()
        self.inventory = self._load_inventory()
        self.map_generator = None
        self.running = True

    def load_or_init(self) -> Dict[str, Any]:
        """Load or create new game state."""
        if self.save_file.exists():
            with self.save_file.open("r") as f:
                return json.load(f)
        return self.new_game()

    def new_game(self) -> Dict[str, Any]:
        """Initialize new game."""
        return {
            "version": 2,
            "timestamp": "2026-09-30",
            "player": {
                "name": "Hero",
                "x": 1,
                "y": 1,
                "map": "base28",
                "hp": 100,
                "max_hp": 100,
                "level": 1,
                "experience": 0,
                "gold": 50,
            },
            "world": {
                "current_zone": "base28",
                "grid": {"width": 28, "height": 28},
                "unlocked": ["base28"],
                "active_quest": "explore_base28",
            },
            "inventory": [],
            "zones": {
                "base28": {"width": 28, "height": 28},
                "base44x48": {"width": 44, "height": 48},
                "base64": {"width": 64, "height": 64},
            },
        }

    def _load_inventory(self) -> Inventory:
        """Restore inventory from state."""
        inv = Inventory()
        for item_data in self.state.get("inventory", []):
            item = Item(
                item_data["name"],
                ItemType(item_data["type"]),
                item_data["rarity"],
                item_data["value"],
            )
            inv.add_item(item)
        return inv

    def save(self):
        """Persist state to JSON."""
        self.state["inventory"] = self.inventory.to_dict()
        with self.save_file.open("w") as f:
            json.dump(self.state, f, indent=2)
        print(f"💾 Game saved to {self.save_file}")

    def display_status(self):
        """Show player status."""
        p = self.state["player"]
        print(f"\n{'='*60}")
        print(f"📍 {self.state['world']['current_zone'].upper()} | Level {p['level']}")
        print(f"👤 {p['name']} | HP: {p['hp']}/{p['max_hp']} | XP: {p['experience']} | Gold: {p['gold']}")
        print(f"{'='*60}\n")

    def show_inventory(self):
        """Display inventory."""
        print("\n📦 INVENTORY:")
        print(self.inventory.list_items())
        print()

    def generate_and_show_map(self):
        """Generate and display map for current zone."""
        zone = self.state["world"]["current_zone"]
        width = self.state["world"]["grid"]["width"]
        height = self.state["world"]["grid"]["height"]

        self.map_generator = MapGenerator(width, height, zone)
        px, py = self.state["player"]["x"], self.state["player"]["y"]
        print(self.map_generator.render(px, py))

    def move_player(self, dx: int, dy: int):
        """Move player and check tile interactions."""
        new_x = self.state["player"]["x"] + dx
        new_y = self.state["player"]["y"] + dy
        width = self.state["world"]["grid"]["width"]
        height = self.state["world"]["grid"]["height"]

        if 0 <= new_x < width and 0 <= new_y < height:
            tile = self.map_generator.get_tile(new_x, new_y)

            if tile == "#":
                print("❌ You hit a wall!")
                return

            self.state["player"]["x"] = new_x
            self.state["player"]["y"] = new_y

            # Check for interactions
            if tile == "C":
                self._on_chest_found()
            elif tile == "E":
                self._on_enemy_encounter()
            elif tile == "X":
                print("🚪 You found the exit! Use 'zones' to advance.")

    def _on_chest_found(self):
        """Found a chest event."""
        item = ItemDatabase.get_random_by_rarity(random.choice(["common", "common", "rare", "epic"]))
        self.inventory.add_item(item)
        print(f"✨ Found a chest! Obtained: {item}")

    def _on_enemy_encounter(self):
        """Enemy encounter event."""
        damage = random.randint(5, 15)
        self.state["player"]["hp"] = max(0, self.state["player"]["hp"] - damage)
        xp_gain = random.randint(10, 25)
        self.state["player"]["experience"] += xp_gain
        print(f"👹 Enemy attack! Took {damage} damage. Gained {xp_gain} XP.")

    def advance_zone(self, zone_name: str):
        """Move to next zone."""
        unlocked = self.state["world"]["unlocked"]
        if zone_name in unlocked:
            self.state["world"]["current_zone"] = zone_name
            self.state["player"]["map"] = zone_name
            self.state["player"]["x"] = 1
            self.state["player"]["y"] = 1
            self.state["player"]["level"] += 1
            print(f"✨ Advanced to {zone_name}!")
            self.generate_and_show_map()
        else:
            print(f"❌ {zone_name} not unlocked yet!")

    def unlock_next_zone(self):
        """Unlock next zone."""
        progression = ["base28", "base44x48", "base64"]
        current_idx = progression.index(self.state["world"]["current_zone"])
        if current_idx < len(progression) - 1:
            next_zone = progression[current_idx + 1]
            if next_zone not in self.state["world"]["unlocked"]:
                self.state["world"]["unlocked"].append(next_zone)
                print(f"🔓 Unlocked {next_zone}!")

    def show_zones(self):
        """Display zones."""
        print("\n🗺️  ZONES:")
        for zone in self.state["world"]["unlocked"]:
            info = self.state["world"]["grid"]
            print(f"  • {zone}")

    def show_help(self):
        """Display help."""
        print("""
╔════════════════════════════════════════╗
║    CONE GAME ENHANCED - COMMANDS        ║
╚════════════════════════════════════════╝

Movement:
  w/a/s/d       Move up/left/down/right
  map           Show map

Inventory & Items:
  inventory     Show inventory
  
Exploration:
  zones         Show unlocked zones
  advance <zone>  Move to zone (base28/base44x48/base64)
  
Game:
  status        Show stats
  checkpoint    Save game
  save          Save game
  help          Show this help
  quit/exit     Exit game
        """)

    def run(self):
        """Main game loop."""
        print("\n🎮 CONE GAME ENHANCED - Exploration & Items")
        print("A game across three dimensional zones with procedural maps.\n")

        self.display_status()
        self.generate_and_show_map()
        self.show_help()

        while self.running:
            cmd = input("> ").strip().lower()

            if not cmd:
                continue

            if cmd in ["quit", "exit"]:
                if input("Save? (y/n): ").strip().lower() == "y":
                    self.save()
                self.running = False
                print("👋 Goodbye!")

            elif cmd == "map":
                self.generate_and_show_map()

            elif cmd == "status":
                self.display_status()

            elif cmd == "inventory":
                self.show_inventory()

            elif cmd == "help":
                self.show_help()

            elif cmd in ["w", "a", "s", "d"]:
                moves = {"w": (0, -1), "a": (-1, 0), "s": (0, 1), "d": (1, 0)}
                dx, dy = moves[cmd]
                self.move_player(dx, dy)
                self.generate_and_show_map()

            elif cmd == "zones":
                self.show_zones()

            elif cmd.startswith("advance"):
                parts = cmd.split()
                if len(parts) > 1:
                    self.advance_zone(parts[1])
                else:
                    print("Usage: advance <zone>")

            elif cmd == "checkpoint":
                self.save()
                print("🎯 Checkpoint saved!")

            elif cmd == "save":
                self.save()

            else:
                print("❓ Unknown command. Type 'help' for options.")


if __name__ == "__main__":
    game = ConeGameEnhanced("cone_save_enhanced.json")
    game.run()
