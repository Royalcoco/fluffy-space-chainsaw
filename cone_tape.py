#!/usr/bin/env python3
"""
cone_tape.py

Converted from a guessed binary tape to a real game save/load model.

This script models the repository's exploration-game progression:
base28 -> base44x48 -> base64

It keeps a JSON save file and supports checkpoint save/load transitions.
"""

import json
from pathlib import Path
from typing import Dict, Any


DEFAULT_SAVE = {
    "version": 1,
    "timestamp": "2026-09-30T10:03:22Z",
    "player": {
        "name": "hero",
        "x": 0,
        "y": 0,
        "map": "base28",
        "hp": 100,
        "inventory": ["map", "torch"],
    },
    "world": {
        "current_zone": "base28",
        "grid": {"width": 28, "height": 28},
        "unlocked": ["base28"],
        "active_quest": "explore_first_room",
    },
    "save": {
        "slot": "auto",
        "checkpoint": 1,
        "status": "ready",
    },
    "transition": {
        "back": ["base28 -> menu", "menu -> previous_checkpoint"],
        "forward": ["base28 -> base44x48", "base44x48 -> base64"],
    },
}


class ConeGameSave:
    def __init__(self, save_path: str = "cone_save.json"):
        self.save_path = Path(save_path)
        self.state = self.load() if self.save_path.exists() else DEFAULT_SAVE.copy()

    def save(self) -> Dict[str, Any]:
        """Persist the current game state to disk."""
        self.state["timestamp"] = "2026-09-30T10:03:22Z"
        with self.save_path.open("w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=2)
            f.write("\n")
        return self.state

    def load(self) -> Dict[str, Any]:
        """Load the current game state from disk if available."""
        with self.save_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        self.state = data
        return self.state

    def checkpoint(self, slot: str = "auto") -> Dict[str, Any]:
        """Create a checkpoint in the save file."""
        self.state["save"] = {
            "slot": slot,
            "checkpoint": self.state["save"].get("checkpoint", 1) + 1,
            "status": "saved",
        }
        return self.save()

    def resume(self) -> Dict[str, Any]:
        """Resume from the latest checkpoint."""
        self.state["save"]["status"] = "resumed"
        return self.state

    def advance_zone(self, to_zone: str) -> Dict[str, Any]:
        """Progress through the game zones: base28 -> base44x48 -> base64."""
        current = self.state["world"]["current_zone"]
        if to_zone not in {"base28", "base44x48", "base64"}:
            raise ValueError(f"Unsupported zone: {to_zone}")
        self.state["world"]["current_zone"] = to_zone
        self.state["player"]["map"] = to_zone
        self.state["world"]["grid"] = {
            "width": 28 if to_zone == "base28" else 44 if to_zone == "base44x48" else 64,
            "height": 28 if to_zone == "base28" else 48 if to_zone == "base44x48" else 64,
        }
        if to_zone not in self.state["world"]["unlocked"]:
            self.state["world"]["unlocked"].append(to_zone)
        return self.save()

    def run_tape(self, tape: str = "101 011 :/011, 011:/101 110/:/EXIT") -> str:
        """
        Interpret a guessed binary tape as checkpoint save/load operations.
        This is intentionally simple and meant to match the earlier tape idea.
        """
        # The tape format is treated as a sequence of checkpoint markers.
        # `:/011` means save at checkpoint 011
        # `110:/` means load from checkpoint 110
        # Here we'll parse the discrete checkpoint references and reflect them in state.
        sample = tape.replace(",", " ")
        tokens = sample.split()
        for token in tokens:
            if token.startswith(":/"):
                target = token[2:]
                self.state["save"] = {
                    "slot": target,
                    "checkpoint": int(target, 2) if target.startswith("0") or target.isdigit() else 1,
                    "status": "saved",
                }
            elif token.endswith(":/"):
                source = token[:-2]
                self.state["save"]["status"] = "loaded"
                self.state["save"]["slot"] = source
        return json.dumps(self.state, indent=2)


if __name__ == "__main__":
    game = ConeGameSave("cone_save.json")
    print("=== SAVE/LOAD STATE ===")
    print(json.dumps(game.state, indent=2))
    print("\n=== SAVE CHECKPOINT ===")
    print(json.dumps(game.checkpoint("auto"), indent=2))
    print("\n=== ADVANCE TO NEXT ZONE ===")
    print(json.dumps(game.advance_zone("base44x48"), indent=2))
    print("\n=== TAPE INTERPRETATION ===")
    print(game.run_tape())
