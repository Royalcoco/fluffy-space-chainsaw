#!/usr/bin/env python3
"""game/stock/minecraft/constants.py
Minecraft-inspired constants and balance settings.
"""

BLOCKS = {
    "grass": {"hardness": 1, "drop": "dirt", "emoji": "🌿"},
    "dirt": {"hardness": 1, "drop": "dirt", "emoji": "🟫"},
    "stone": {"hardness": 2, "drop": "stone", "emoji": "🪨"},
    "water": {"hardness": 0, "drop": None, "emoji": "💧"},
    "wood": {"hardness": 2, "drop": "wood", "emoji": "🪵"},
    "sand": {"hardness": 1, "drop": "sand", "emoji": "🏖️"},
    "ore": {"hardness": 3, "drop": "ore", "emoji": "⛏️"},
}

ITEMS = {
    "pickaxe": {"type": "tool", "power": 2, "emoji": "⛏️"},
    "axe": {"type": "tool", "power": 2, "emoji": "🪓"},
    "sword": {"type": "weapon", "damage": 10, "emoji": "⚔️"},
    "torch": {"type": "utility", "light": 5, "emoji": "🔥"},
    "bread": {"type": "food", "heal": 10, "emoji": "🍞"},
    "iron_ore": {"type": "resource", "emoji": "🪙"},
}

WORLD_SIZES = {
    "base28": {"width": 28, "height": 28},
    "base44x48": {"width": 44, "height": 48},
    "base64": {"width": 64, "height": 64},
}

GAME_BALANCE = {
    "mining": 1.0,
    "crafting": 1.0,
    "enemy_damage": 10,
    "player_hp": 100,
    "drop_rate": 0.7,
}
