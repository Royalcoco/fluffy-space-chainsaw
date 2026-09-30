#!/usr/bin/env python3
"""game/stock/minecraft/player.py
Player movement and world control system.
"""

from typing import Tuple


class Player:
    def __init__(self, x: int = 1, y: int = 1, max_hp: int = 100):
        self.x = x
        self.y = y
        self.hp = max_hp
        self.max_hp = max_hp
        self.level = 1
        self.experience = 0
        self.hunger = 100

    def move(self, dx: int, dy: int, world_width: int, world_height: int) -> Tuple[bool, str]:
        """Move player in world, respecting bounds."""
        new_x = self.x + dx
        new_y = self.y + dy

        if new_x < 0 or new_x >= world_width:
            return False, "❌ Cannot move beyond world boundary!"
        if new_y < 0 or new_y >= world_height:
            return False, "❌ Cannot move beyond world boundary!"

        self.x = new_x
        self.y = new_y
        self.hunger = max(0, self.hunger - 1)
        return True, f"✓ Moved to ({self.x}, {self.y})"

    def take_damage(self, amount: int) -> bool:
        """Take damage. Returns True if still alive."""
        self.hp = max(0, self.hp - amount)
        return self.hp > 0

    def heal(self, amount: int):
        """Heal player."""
        self.hp = min(self.max_hp, self.hp + amount)

    def feed(self, amount: int):
        """Restore hunger."""
        self.hunger = min(100, self.hunger + amount)

    def gain_experience(self, amount: int):
        """Gain experience and level up if threshold reached."""
        self.experience += amount
        if self.experience >= 100:
            self.level += 1
            self.experience = 0
            self.max_hp += 10
            self.hp = self.max_hp
            return True
        return False

    def is_alive(self) -> bool:
        return self.hp > 0

    def status(self) -> str:
        return f"Level {self.level} | HP: {self.hp}/{self.max_hp} | Hunger: {self.hunger} | XP: {self.experience}/100"
