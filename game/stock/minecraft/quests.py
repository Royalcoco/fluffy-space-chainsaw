#!/usr/bin/env python3
"""game/stock/minecraft/quests.py
Quest tracking for the Minecraft-inspired game.
"""

from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Quest:
    title: str
    description: str
    kind: str
    target: int
    progress: int = 0

    def add_progress(self, amount: int = 1):
        self.progress += amount

    def is_complete(self) -> bool:
        return self.progress >= self.target

    def remaining(self) -> int:
        return max(0, self.target - self.progress)


class QuestTracker:
    def __init__(self):
        self.quests: List[Quest] = [
            Quest("Gather wood", "Collect enough wood to build tools.", "gather", 8),
            Quest("Craft a torch", "Create a torch for the cave.", "craft", 2),
            Quest("Defeat enemies", "Defeat 3 enemies in the world.", "kill", 3),
            Quest("Reach the next zone", "Advance to the next biome.", "zone", 1),
        ]

    def update(self, kind: str, amount: int = 1):
        for quest in self.quests:
            if quest.kind == kind and not quest.is_complete():
                quest.add_progress(amount)

    def list(self) -> str:
        lines = ["\nQuests:"]
        for quest in self.quests:
            done = "✓" if quest.is_complete() else "•"
            lines.append(f"  {done} {quest.title}: {quest.progress}/{quest.target} - {quest.description}")
        return "\n".join(lines)

    def completed(self) -> List[str]:
        return [q.title for q in self.quests if q.is_complete()]
