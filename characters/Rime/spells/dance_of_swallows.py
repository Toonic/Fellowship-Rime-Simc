"""Module for Dance of Swallows Spell"""

from characters.rime import RimeDebuff
from characters.rime.debuffs import DanceOfSwallowsDebuff


class DanceOfSwallows(RimeDebuff):
    """Dance of Swallows Spell"""

    def __init__(self):
        super().__init__(
            "Dance of Swallows",
            cooldown=60,
            winter_orb_cost=2,
            debuff=DanceOfSwallowsDebuff(),
        )
