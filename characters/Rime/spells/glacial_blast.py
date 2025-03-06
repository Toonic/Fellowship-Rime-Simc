"""Module for Glacial Blast Spell"""

from characters.rime import RimeSpell
from characters.rime.talent import RimeTalents
from characters.rime.buffs import GlacialAssaultBuff
from characters.rime.talent import GlacialAssaultTalent


class GlacialBlast(RimeSpell):
    """Glacial Blast Spell"""

    def __init__(self):
        super().__init__(
            "Glacial Blast",
            cast_time=2.0,
            damage_percent=504,
            winter_orb_cost=2,
        )

    def effective_cast_time(self):
        # Checks to see if the Glacial Assault buff is ready and overrides the cast time to  be instant.
        if self.is_glacial_assault_ready():
            return 0
        return super().effective_cast_time()

    def damage_modifiers(self, damage) -> float:
        if self.is_glacial_assault_ready():
            return damage * (1 + (GlacialAssaultTalent.bonus_damage) / 100)
        else:
            return damage

    def on_cast_complete(self):
        super().on_cast_complete()
        # On cast complete we want to consume the Glacial Assault buff.
        if self.is_glacial_assault_ready():
            self.character.get_buff(GlacialAssaultBuff()).remove(True)

    def crit_chance_modifiers(self, crit_chance):
        # Checks to see if Glacial Assault is talented, and if it is increases the Crit.
        if self.character.has_talent(RimeTalents.GLACIAL_ASSAULT):
            crit_chance += GlacialAssaultTalent.bonus_critical_strike
        return crit_chance

    def is_glacial_assault_ready(self) -> bool:
        """Checks to see if Glacial Assault is talented and at maximum stacks."""
        if self.character.has_talent(RimeTalents.GLACIAL_ASSAULT):
            if self.character.has_buff(GlacialAssaultBuff()):
                if (
                    self.character.get_buff(
                        GlacialAssaultBuff()
                    ).current_stacks
                    == self.character.get_buff(
                        GlacialAssaultBuff()
                    ).maximum_stacks
                ):
                    return True
        return False
