"""Module for the Character class."""

from typing import List, TYPE_CHECKING

from characters.Rime import RimeSpell, RimeBuff

if TYPE_CHECKING:
    from .spell import Spell


class Character:
    """Base class for all characters."""

    intellectPerPoint = 1
    critPerPoint = 0.21
    expertisePerPoint = 0.21
    hastePerPoint = 0.21
    spiritPerPoint = 0.21

    def __init__(self, intellect, crit, expertise, haste, spirit):
        self.intellect_points = intellect
        self.intellect = intellect * Character.intellectPerPoint
        self.crit_points = crit
        self.crit = (  # % chance (e.g., 5 for 5%)
            crit * Character.critPerPoint
        ) + 5
        self.expertise_points = expertise
        self.expertise = (  # % increase to damage
            expertise * Character.expertisePerPoint
        )
        self.haste_points = haste
        # % increase to cast speed
        self.haste = haste * Character.hastePerPoint
        self.spirit = spirit * Character.spiritPerPoint
        self.spirit_points = spirit
        self.mana = 0
        self.winter_orbs = 0
        # This will hold the character's available spells.
        self.spells: List[Spell] = [spell.value for spell in RimeSpell]
        # This will hold the character's rotation.
        self.rotation: List[Spell] = []
        # All the talents.
        self.talents: List[str] = []

        self.anima_spikes = RimeSpell.ANIMA_SPIKES.value
        self.soulfrost = RimeSpell.SOULFROST_TORRENT.value
        self.boosted_blast = RimeBuff.BOOSTED_BLAST.value

        self.soulfrost_buff = RimeBuff.SOULFROST_BUFF.value
        self.glacial_assault_buff = RimeBuff.GLACIAL_ASSAULT_BUFF.value
        self.comet_bonus = RimeBuff.COMET_BONUS.value

    def add_spell_to_rotation(self, spell: RimeSpell) -> None:
        """Adds a spell to the character's rotation."""

        if spell.value not in self.spells:
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

        self.intellect = intellect * Character.intellectPerPoint
        self.crit = crit * Character.critPerPoint
        self.expertise = expertise * Character.expertisePerPoint
        self.haste = haste * Character.hastePerPoint
        self.spirit = spirit * Character.spiritPerPoint
