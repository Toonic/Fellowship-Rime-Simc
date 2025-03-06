from base import BaseBuff


class IceBlitzBuff(BaseBuff):
    """Glacial Assault buff."""

    ice_blitz_damage_multiplier = 0.15

    def __init__(self):
        super().__init__("Ice Blitz", duration=20, maximum_stacks=1)

    def on_apply(self):
        self.character.damage_multiplier += self.ice_blitz_damage_multiplier

    def on_remove(self):
        self.character.damage_multiplier -= self.ice_blitz_damage_multiplier
