"""Module for Glacial Blast Spell"""

from characters.rime import RimeSpell
from characters.rime.talent import RimeTalents
from characters.rime.buffs import GlacialAssault


class GlacialBlast(RimeSpell):
    """Glacial Blast Spell"""

    def __init__(self):
        super().__init__(
            "Glacial Blast",
            cast_time=2.0,
            damage_percent=504,
            winter_orb_cost=2,
        )

    def is_ready(self):
        glacial_assault = GlacialAssault()
        if (
            RimeTalents.GLACIAL_ASSAULT in self.character.talents
            and glacial_assault.simfell_name in self.character.buffs
        ):
            previous_cast_time = self.cast_time
            if (
                self.character.buffs[glacial_assault].current_stacks
                == self.character.buffs[glacial_assault].maximum_stacks
            ):
                self.cast_time = 0
            else:
                # self.cast_time = 2  # I don't like this.
                self.cast_time = previous_cast_time

    def crit_chance_modifiers(self, crit_chance):
        if RimeTalents.GLACIAL_ASSAULT in self.character.talents:
            # Mel's NOTE: Maybe you can create a class attribute that would
            # be used to determine additional modifiers.
            # E.g. self.additional_modifiers: Dict[str, float] = {}
            # crit_chance += self.additional_modifiers.get("crit_chance", 0)

            crit_chance += 20  # I also don't like this.
        return crit_chance
