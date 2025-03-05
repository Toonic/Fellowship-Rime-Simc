"""Module for Dance of Swallows Spell"""

from characters.rime import RimeDebuff


class DanceOfSwallows(RimeDebuff):
    """Dance of Swallows Spell"""

    def __init__(self):
        super().__init__(
            "Dance of Swallows",
            cooldown=60,
            duration=20,
            damage_percent=53,
            winter_orb_cost=2,
        )
