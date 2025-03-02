"""Module for the RimeCharacter class."""

from base import BaseCharacter
from characters.Rime.enum import RimeSpellEnum, RimeBuffEnum


class RimeCharacter(BaseCharacter):
    """Base class for all characters."""

    intellectPerPoint = 1
    critPerPoint = 0.21
    expertisePerPoint = 0.21
    hastePerPoint = 0.21
    spiritPerPoint = 0.21

    def __init__(self, intellect, crit, expertise, haste, spirit):
        super().__init__(intellect, crit, expertise, haste, spirit)

        self.mana = 0
        self.winter_orbs = 0

        self.spells = {
            spell.value.name.lower(): spell.value for spell in RimeSpellEnum
        }
        self.buffs = {
            spell.value.name.lower(): spell.value for spell in RimeBuffEnum
        }
        self.comet_bonus = RimeBuffEnum.COMET_BONUS.value

        # ------------
        # Test Values
        # ------------
        self.anima = 0

    def add_spell_to_rotation(self, spell: RimeSpellEnum) -> None:
        """Adds a spell to the character's rotation."""

        if spell.value.name.lower() not in self.spells:
            raise ValueError(f"Spell {spell} not found in available spells.")

        self.rotation.append(spell.value)

    def add_talent(self, talent: str) -> None:
        """Adds a talent to the character's available talents."""

        self.talents.append(talent)

    def update_stats(
        self,
        intellect: int,
        crit: int,
        expertise: int,
        haste: int,
        spirit: int,
    ) -> None:
        """Updates the character's stats."""

        self.intellect = intellect * self.intellectPerPoint
        self.crit = crit * self.critPerPoint
        self.expertise = expertise * self.expertisePerPoint
        self.haste = haste * self.hastePerPoint
        self.spirit = spirit * self.spiritPerPoint
