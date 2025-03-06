"""Module for Cold Snap Spell"""

from characters.rime import RimeSpell
from characters.rime.talent import RimeTalents
from characters.rime.buffs import GlacialAssaultBuff
from .dance_of_swallows import DanceOfSwallows


class ColdSnap(RimeSpell):
    """Cold Snap Spell"""

    def __init__(self):
        super().__init__(
            "Cold Snap", damage_percent=204, winter_orb_cost=-1, cooldown=8
        )

        self._dance_of_swallows_trigger_count = 10

    def apply_buff(self):
        if self.character.has_talent(RimeTalents.GLACIAL_ASSAULT):
            GlacialAssaultBuff().apply(self.character)

    def on_cast_complete(self):
        super().on_cast_complete()

        # Trigger Dance of Swallows on cast if the buff is there.
        if (
            self.character.simulation.debuffs.get(
                DanceOfSwallows().simfell_name
            )
            is not None
        ):
            # Dance of Swallows is hard coded to trigger 10 times from ColdSnap
            for _ in range(self._dance_of_swallows_trigger_count):
                self.character.dance_of_swallows.damage()
