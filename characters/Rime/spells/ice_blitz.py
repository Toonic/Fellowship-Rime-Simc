"""Module for Ice Blitz Spell"""

from characters.rime import RimeBuff


class IceBlitz(RimeBuff):
    """Ice Blitz Spell"""

    ice_blitz_damage_multiplier = 0.15

    def __init__(self):
        super().__init__(
            "Ice Blitz",
            duration=20,
            cooldown=120,
            has_gcd=False,
            can_cast_on_gcd=True,
            can_cast_while_casting=True,
        )

    def apply_buff(self):
        super().apply_buff()
        self.character.damage_multiplier += self.ice_blitz_damage_multiplier

    def remove_buff(self):
        super().remove_buff()
        self.character.damage_multiplier -= self.ice_blitz_damage_multiplier
