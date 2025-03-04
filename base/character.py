"""Module for the Character class."""

from abc import ABC, abstractmethod
from typing import Dict, List, TYPE_CHECKING, Optional

# from enum import Enum


if TYPE_CHECKING:
    from spell import BaseSpell
    from spell import BaseBuff
    from rework_sim import Simulation


class BaseCharacter(ABC):
    """Abstract base class for all characters."""

    # TODO: Figure out Stat DR.
    percent_per_point = 0.21

    def __init__(self, main_stat, crit, expertise, haste, spirit):
        # Main Stat Conversion - Points to % including DR.
        self._main_stat = main_stat
        # Crit has a base of 5%.
        self._crit = (crit * self.percent_per_point) + 5
        self._expertise = expertise * self.percent_per_point
        self._haste = haste * self.percent_per_point
        self._spirit = spirit * self.percent_per_point

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
        self.simulation: Optional["Simulation"] = None

        # External Character Stat Buffs - EG: Gems, Gear, Buffs.
        self.damage_multiplier = 0

        self.main_stat_multiplier = 0
        self.main_stat_additional = 0
        self.crit_multiplier = 0
        self.crit_additional = 0
        self.expertise_multiplier = 0
        self.expertise_additional = 0
        self.haste_multiplier = 0
        self.haste_additional = 0
        self.spirit_multiplier = 0
        self.spirit_additional = 0

    def set_simulation(self, simulation: "Simulation") -> None:
        """Sets the simulation for the character."""
        self.simulation = simulation

    def get_main_stat(self) -> float:
        """Returns the character's main stat."""
        return (self._main_stat + self.main_stat_additional) * (
            1 + self.main_stat_multiplier
        )

    def get_crit(self) -> float:
        """Returns the character's crit as a percentage."""
        return (self._crit + self.crit_additional) * (1 + self.crit_multiplier)

    def get_haste(self) -> float:
        """Returns the character's haste as a percentage."""
        return (self._haste + self.haste_additional) * (
            1 + self.haste_multiplier
        )

    def get_expertise(self) -> float:
        """Returns the character's expertise as a percentage."""
        return (self._expertise + self.expertise_additional) * (
            1 + self.expertise_multiplier
        )

    def get_spirit(self) -> float:
        """Returns the character's spirit as a percentage."""
        return (self._spirit + self.spirit_additional) * (
            1 + self.spirit_multiplier
        )

    def get_damage_multiplier(self) -> float:
        """Returns the character's damage multiplyer."""
        return 1 + self.damage_multiplier

    @abstractmethod
    def configure_spell_book(self) -> None:
        """Adds a spells to the character's spell book."""

    def add_talent(self, talent: str) -> None:
        """Adds a talent to the character's available talents."""
