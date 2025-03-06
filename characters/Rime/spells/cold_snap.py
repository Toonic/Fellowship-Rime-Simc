"""Module for Cold Snap Spell"""

from characters.rime import RimeSpell
from characters.rime.talent import RimeTalents
from characters.rime.buffs import GlacialAssault
from .dance_of_swallows import DanceOfSwallows


class ColdSnap(RimeSpell):
    """Cold Snap Spell"""

    glacial_assault = GlacialAssault()

    def __init__(self):
        super().__init__(
            "Cold Snap", damage_percent=204, winter_orb_cost=-1, cooldown=8
        )
        self.glacial_assault.character = self.character

        self._dance_of_swallows_trigger_count = 10

    def on_cast_complete(self):
        super().on_cast_complete()

        if RimeTalents.GLACIAL_ASSAULT in self.character.talents:
            self.glacial_assault.apply_buff()

        # Trigger Dance of Swallows on cast if the buff is there.
        if (
            self.character.simulation.debuffs.get(
                DanceOfSwallows().simfell_name
            )
            is not None
        ):
            # Dance of Swallows is hard coded to trigger 10 times from ColdSnap

            # Mel's NOTE: The why dont you code it to the attribute?
            # E.g.: self.dance_of_swallows_trigger_count = 10
            # OR we would store trigger counts for each spell in the
            # Dance of Swallows class, since there may be more variance.
            # -> Decide!!
            for _ in range(self._dance_of_swallows_trigger_count):
                self.character.dance_of_swallows.damage()
