"""Module for Glacial Blast Spell"""

from characters.rime import RimeSpell
from characters.rime.talent import RimeTalents


class GlacialBlast(RimeSpell):
    """Glacial Blast Spell"""

    def __init__(self):
        super().__init__(
            "Glacial Blast",
            cast_time=2.0,
            damage_percent=504,
            winter_orb_cost=2,
        )

    def crit_chance_modifiers(self, crit_chance):
        if RimeTalents.GLACIAL_ASSAULT in self.character.talents:
            crit_chance += 20
        return crit_chance
