"""Module for Glacial Blast Spell"""

from characters.rime import RimeSpell
from characters.rime.talent import RimeTalents
from characters.rime.buffs import GlacialAssault


class GlacialBlast(RimeSpell):
    """Glacial Blast Spell"""

    glacial_assault = None

    def __init__(self):
        super().__init__(
            "Glacial Blast",
            cast_time=2.0,
            damage_percent=504,
            winter_orb_cost=2,
        )

    def effective_cast_time(self):
        """Overrides the effective cast time if you have maximum stacks of glacial assault."""
        if self.is_glacial_assault_ready():
            return 0
        return super().effective_cast_time()

    def damage_modifiers(self, damage) -> float:
        if self.is_glacial_assault_ready():
            return damage * 2
        else:
            return damage

    def on_cast_complete(self):
        super().on_cast_complete()
        if self.is_glacial_assault_ready():
            self.character.buffs[self.glacial_assault].remove_buff()

    def crit_chance_modifiers(self, crit_chance):
        if RimeTalents.GLACIAL_ASSAULT in self.character.talents:
            crit_chance += (
                20  # TODO: Move the 20 to a Glacial_Assault talent class.
            )
        return crit_chance

    def is_glacial_assault_ready(self) -> bool:
        if RimeTalents.GLACIAL_ASSAULT in self.character.talents:
            self.glacial_assault = GlacialAssault().simfell_name
            if self.glacial_assault in self.character.buffs:
                if (
                    self.character.buffs[self.glacial_assault].current_stacks
                    == self.character.buffs[
                        self.glacial_assault
                    ].maximum_stacks
                ):
                    return True
        return False
