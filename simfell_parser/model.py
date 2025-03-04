"""Models for the SimFell file."""

from typing import Any, List, Optional
from pydantic import BaseModel

from simfell_parser.enums import Gem, TierSet, Tier


class Condition(BaseModel):
    """Class for a condition in a SimFell file."""

    left: str
    operator: str
    right: Any


class Action(BaseModel):
    """Class for an action in a SimFell file."""

    name: str
    conditions: List[Condition]

    def __str__(self):
        return f"{self.name} ({', '.join(self.conditions)})"


class GemTier(BaseModel):
    """Class for a gem tier in a SimFell configuration."""

    tier: Tier
    gem: Gem


class Equipment(BaseModel):
    """Class for an equipment in a SimFell configuration."""

    name: str
    ilvl: int
    tier: Tier
    tier_set: Optional[TierSet]
    intellect: int
    stamina: int
    expertise: Optional[int]
    crit: Optional[int]
    haste: Optional[int]
    spirit: Optional[int]
    gem_bonus: Optional[int]
    gem: Optional[GemTier]


class Gear(BaseModel):
    """Class for a gear in a SimFell configuration."""

    helmet: Optional[Equipment]
    shoulder: Optional[Equipment]


class SimFellConfiguration(BaseModel):
    """Class for a SimFell configuration."""

    name: str
    hero: str
    intellect: int
    crit: float
    expertise: float
    haste: float
    spirit: float
    talents: str
    trinket1: Optional[str]
    trinket2: Optional[str]

    duration: int
    enemies: int
    run_count: int

    actions: List[Action]
    gear: Gear

    @property
    def parsed_json(self) -> str:
        """Convert the configuration to a JSON string."""

        return self.model_dump_json(indent=2)
