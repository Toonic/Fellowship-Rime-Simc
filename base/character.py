"""Module for the Character class."""

from abc import ABC, abstractmethod
from typing import Dict, List, TYPE_CHECKING

# from enum import Enum


if TYPE_CHECKING:
    from spell import BaseSpell
    from spell import BaseBuff


class BaseCharacter(ABC):
    """Abstract base class for all characters."""

    def __init__(self, main_stat, crit, expertise, haste, spirit):
        self.main_stat = main_stat
        self.main_stat = main_stat * self.main_stat_per_point
        self.crit_points = crit
        self.crit = (crit * self.critPerPoint) + 5  # % chance (e.g., 5 for 5%)
        self.expertise_points = expertise
        self.expertise = (  # % increase to damage
            expertise * self.expertisePerPoint
        )
        self.haste_points = haste
        # % increase to cast speed
        self.haste = haste * self.hastePerPoint
        self.spirit = spirit * self.spiritPerPoint
        self.spirit_points = spirit
        # This will hold the character's available spells.
        self.spells: Dict[str, BaseSpell] = {}
        # This will hold the character's rotation.
        # TODO: Change this to an object reference of SimFell Action?
        self.rotation: List[str] = []
        # All the talents.
        self.talents: List[str] = []
        # Buffs
        self.buffs: Dict[str, BaseBuff] = {}
        self.configure_spell_book()
        self.simulation = None

        # External Character Stat Buffs
        self.main_stat_multiplier = 0
        self.main_stat_additional = 0
        self.haste_multiplier = 0
        self.haste_additional = 0

    def set_simulation(self, simulation) -> None:
        """Sets the simulation for the character."""
        self.simulation = simulation

    def get_main_stat(self) -> float:
        """Returns the character's main stat."""
        return (self.main_stat + self.main_stat_additional) * (
            1 + self.main_stat_multiplier
        )

    def get_haste(self) -> float:
        """Returns the character's haste."""
        return (self.haste + self.haste_additional) * (
            1 + self.haste_multiplier
        )

    @abstractmethod
    def configure_spell_book(self) -> None:
        """Adds a spells to the character's spell book."""

    def add_talent(self, talent: str) -> None:
        """Adds a talent to the character's available talents."""
