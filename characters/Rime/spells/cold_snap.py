from characters.rime import RimeSpell
from .dance_of_swallows import DanceOfSwallows


class ColdSnap(RimeSpell):
    """Cold Snap Spell"""

    def __init__(self):
        super().__init__(
            "Cold Snap", damage_percent=204, winter_orb_cost=-1, cooldown=8
        )

    def on_cast_complete(self):
        super().on_cast_complete()
        if (
            self.character.simulation.debuffs.get(
                DanceOfSwallows().simfell_name
            )
            is not None
        ):
            # Dance of Swallows is hard coded to trigger 10 times from ColdSnap
            for _ in range(10):
                self.character.dance_of_swallows.damage()
