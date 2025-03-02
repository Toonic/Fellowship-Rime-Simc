"""Module for the BaseSimulation class."""

from abc import ABC, abstractmethod

from base import BaseCharacter, BaseSpell


class BaseSimulation(ABC):
    """Abstract base class for all simulations."""

    def __init__(
        self,
        character: BaseCharacter,
        duration: int,
        enemy_count: int = 1,
        do_debug: bool = True,
        is_deterministic: bool = False,
    ):
        self.character = character
        self.time = 0
        self.duration = duration
        self.total_damage = 0
        self.do_debug = do_debug
        self.gcd = 0
        self.debuffs = []
        self.buffs = []
        self.enemy_count = enemy_count
        self.is_deterministic = is_deterministic

        self.damage_table = {}

        if is_deterministic:
            self.character.crit = 0
            self.character.spirit = 0

    def _fill_damage_table(self, key: str, damage: float) -> None:
        """Fill the damage table with the given key and damage."""

        self.damage_table[key] = self.damage_table.get(key, 0) + damage

    @abstractmethod
    def do_damage(
        self,
        spell: BaseSpell,
        damage: float,
        anima_gained: float,
        orb_cost: int,
        is_cast: bool = True,
    ) -> None:
        """Does damage to the enemy (dummy)"""

    @abstractmethod
    def apply_damage_multipliers(
        self, spell: BaseSpell, damage: float
    ) -> float:
        """Apply damage multipliers based on active buffs and talents."""

    @abstractmethod
    def update_spell_cooldowns(self, spell: BaseSpell) -> None:
        """Update cooldowns for specific spells."""

    @abstractmethod
    def determine_aoe_count(self, spell: BaseSpell) -> int:
        """Determine the number of targets affected by AoE spells."""

    @abstractmethod
    def apply_critical_hit(self, spell: BaseSpell, damage: float) -> float:
        """Calculate and apply critical hit damage."""

    @abstractmethod
    def apply_aoe_damage_reduction(
        self, spell: BaseSpell, damage: float, index: int
    ) -> float:
        """Apply AoE damage reduction if applicable."""

    @abstractmethod
    def handle_debug_output(
        self, spell: BaseSpell, damage: float, is_cast: bool
    ) -> None:
        """Output debug information if debugging is enabled."""

    @abstractmethod
    def update_time(self, delta_time: int) -> None:
        """Updates the time and cooldowns."""

    @abstractmethod
    def run(self) -> float:
        """Runs the simulation."""
