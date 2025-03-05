from rime import RimeBuff


class WrathOfWinter(RimeBuff):
    """Wrath of Winter Spell"""

    haste_additional_bonus = 30
    damage_multiplier_bonus = 0.15

    def __init__(self):
        super().__init__(
            "Wrath of Winter",
            cast_time=0,
            duration=20,
            ticks=10,
            cooldown=1000,  # TODO: Spirit Gen instead.
        )

    def on_tick(self):
        self.character.gain_winter_orbs(1)

    def apply_buff(self):
        super().apply_buff()
        self.character.damage_multiplier += self.damage_multiplier_bonus
        self.character.haste_additional += self.haste_additional_bonus

    def remove_buff(self):
        super().remove_buff()
        self.character.damage_multiplier -= self.damage_multiplier_bonus
        self.character.haste_additional -= self.haste_additional_bonus
