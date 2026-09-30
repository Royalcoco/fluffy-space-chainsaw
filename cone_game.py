#!/usr/bin/env python3
"""
cone_game.py

Minimal playable exploration game with save/load system.
Supports progression through three zones: base28 -> base44x48 -> base64
"""

import json
import random
from pathlib import Path
from typing import Dict, Any, Tuple, List


class ConeGame:
    def __init__(self, save_file: str = "cone_save.json"):
        self.save_file = Path(save_file)
        self.state = self.load_or_init()
        self.running = True

    def load_or_init(self) -> Dict[str, Any]:
        """Load existing save or create new game state."""
        if self.save_file.exists():
            with self.save_file.open("r") as f:
                return json.load(f)
        else:
            return self.new_game()

    def new_game(self) -> Dict[str, Any]:
        """Initialize a new game state."""
        return {
            "version": 1,
            "timestamp": "2026-09-30",
            "player": {
                "name": "Hero",
                "x": 0,
                "y": 0,
                "map": "base28",
                "hp": 100,
                "max_hp": 100,
                "inventory": ["map", "torch"],
                "level": 1,
            },
            "world": {
                "current_zone": "base28",
                "grid": {"width": 28, "height": 28},
                "unlocked": ["base28"],
                "active_quest": "explore_base28",
            },
            "save": {
                "slot": "auto",
                "checkpoint": 0,
                "status": "new",
            },
            "zones": {
                "base28": {"width": 28, "height": 28, "discovered": False},
                "base44x48": {"width": 44, "height": 48, "discovered": False},
                "base64": {"width": 64, "height": 64, "discovered": False},
            },
        }

    def save(self):
        """Persist game state to JSON."""
        with self.save_file.open("w") as f:
            json.dump(self.state, f, indent=2)
        print(f"💾 Game saved to {self.save_file}")

    def render_map(self) -> str:
        """Render the current zone as ASCII."""
        zone = self.state["world"]["current_zone"]
        width = self.state["world"]["grid"]["width"]
        height = self.state["world"]["grid"]["height"]
        px, py = self.state["player"]["x"], self.state["player"]["y"]

        # Simple ASCII map
        lines = []
        lines.append(f"╔{'═' * (width + 2)}╗")
        for y in range(height):
            line = "║ "
            for x in range(width):
                if x == px and y == py:
                    line += "@"  # Player
                elif random.random() < 0.1:
                    line += "#"  # Wall
                else:
                    line += "."  # Floor
            line += " ║"
            lines.append(line)
        lines.append(f"╚{'═' * (width + 2)}╝")
        return "\n".join(lines)

    def display_status(self):
        """Show current game status."""
        p = self.state["player"]
        w = self.state["world"]
        print(f"\n{'='*50}")
        print(f"📍 Zone: {w['current_zone']} ({w['grid']['width']}x{w['grid']['height']})")
        print(f"👤 {p['name']} | HP: {p['hp']}/{p['max_hp']} | Level: {p['level']}")
        print(f"📦 Inventory: {', '.join(p['inventory'])}")
        print(f"🎯 Quest: {w['active_quest']}")
        print(f"{'='*50}\n")

    def move_player(self, dx: int, dy: int) -> bool:
        """Move player by delta, respecting zone bounds."""
        new_x = self.state["player"]["x"] + dx
        new_y = self.state["player"]["y"] + dy
        width = self.state["world"]["grid"]["width"]
        height = self.state["world"]["grid"]["height"]

        if 0 <= new_x < width and 0 <= new_y < height:
            self.state["player"]["x"] = new_x
            self.state["player"]["y"] = new_y
            return True
        else:
            print("❌ Out of bounds!")
            return False

    def advance_zone(self, zone_name: str) -> bool:
        """Progress to next zone."""
        unlocked = self.state["world"]["unlocked"]
        if zone_name in unlocked:
            self.state["world"]["current_zone"] = zone_name
            self.state["player"]["map"] = zone_name
            grid_sizes = {"base28": (28, 28), "base44x48": (44, 48), "base64": (64, 64)}
            w, h = grid_sizes.get(zone_name, (28, 28))
            self.state["world"]["grid"] = {"width": w, "height": h}
            self.state["player"]["x"] = 0
            self.state["player"]["y"] = 0
            self.state["player"]["level"] += 1
            print(f"✨ Advanced to {zone_name}!")
            return True
        else:
            print(f"❌ {zone_name} not yet unlocked")
            return False

    def unlock_zone(self, zone_name: str):
        """Unlock a new zone."""
        if zone_name not in self.state["world"]["unlocked"]:
            self.state["world"]["unlocked"].append(zone_name)
            print(f"🔓 Unlocked {zone_name}!")

    def checkpoint(self):
        """Create a save checkpoint."""
        self.state["save"]["checkpoint"] += 1
        self.save()
        print(f"🎯 Checkpoint {self.state['save']['checkpoint']} created!")

    def show_help(self):
        """Display command help."""
        print("""
╔════════════════════════════════════════╗
║       CONE GAME - COMMAND REFERENCE     ║
╚════════════════════════════════════════╝

Movement:
  w/a/s/d    Move up/left/down/right
  
Game Control:
  explore    Explore current zone (random event)
  zones      Show unlocked zones
  advance <zone>  Move to unlocked zone (base28/base44x48/base64)
  checkpoint Save game state
  map        Redraw current map
  status     Show player stats
  
Meta:
  help       Show this help
  save       Save game
  quit/exit  Exit game
        """)

    def explore(self):
        """Random exploration event."""
        events = [
            ("You found a treasure chest!", lambda: self.state["player"]["inventory"].append("gold")),
            ("An enemy appears!", lambda: self.damage_player(10)),
            ("You discovered a new area!", lambda: self.unlock_next_zone()),
            ("You healed yourself!", lambda: self.heal_player(25)),
        ]
        event, action = random.choice(events)
        print(f"🎲 {event}")
        action()

    def damage_player(self, amount: int):
        """Take damage."""
        self.state["player"]["hp"] = max(0, self.state["player"]["hp"] - amount)
        print(f"💔 You took {amount} damage! HP: {self.state['player']['hp']}")

    def heal_player(self, amount: int):
        """Heal player."""
        self.state["player"]["hp"] = min(
            self.state["player"]["max_hp"],
            self.state["player"]["hp"] + amount
        )
        print(f"💚 Healed {amount} HP! Current: {self.state['player']['hp']}")

    def unlock_next_zone(self):
        """Unlock next zone based on current progress."""
        current = self.state["world"]["current_zone"]
        progression = ["base28", "base44x48", "base64"]
        idx = progression.index(current)
        if idx < len(progression) - 1:
            next_zone = progression[idx + 1]
            self.unlock_zone(next_zone)

    def show_zones(self):
        """Display available zones."""
        print("\nAvailable Zones:")
        for zone in self.state["world"]["unlocked"]:
            info = self.state["zones"][zone]
            print(f"  • {zone} ({info['width']}x{info['height']})")

    def run(self):
        """Main game loop."""
        print("\n🎮 Welcome to CONE GAME!")
        print("An exploration game across three dimensional paliers.\n")
        self.display_status()
        self.show_help()

        while self.running:
            print()
            cmd = input("> ").strip().lower()

            if not cmd:
                continue

            if cmd == "quit" or cmd == "exit":
                print("\nSave before exit? (y/n)")
                if input().strip().lower() == "y":
                    self.save()
                self.running = False
                print("👋 Goodbye!")

            elif cmd == "map":
                print(self.render_map())

            elif cmd == "status":
                self.display_status()

            elif cmd == "help":
                self.show_help()

            elif cmd == "w":
                self.move_player(0, -1)
                print(self.render_map())

            elif cmd == "s":
                self.move_player(0, 1)
                print(self.render_map())

            elif cmd == "a":
                self.move_player(-1, 0)
                print(self.render_map())

            elif cmd == "d":
                self.move_player(1, 0)
                print(self.render_map())

            elif cmd == "explore":
                self.explore()

            elif cmd == "zones":
                self.show_zones()

            elif cmd.startswith("advance"):
                parts = cmd.split()
                if len(parts) > 1:
                    zone = parts[1]
                    self.advance_zone(zone)
                    print(self.render_map())
                else:
                    print("Usage: advance <zone>")

            elif cmd == "checkpoint":
                self.checkpoint()

            elif cmd == "save":
                self.save()

            else:
                print("❓ Unknown command. Type 'help' for options.")


if __name__ == "__main__":
    game = ConeGame("cone_save.json")
    game.run()
