from characters.rime import RimeDebuff


class BurstingIceDebuff(RimeDebuff):
    """Glacial Assault buff."""

    haste_additional_bonus = 30
    damage_multiplier_bonus = 0.15

    def __init__(self):
        super().__init__(
            "Bursting Ice",
            anima_per_tick=1,
            ticks=6,
            duration=3,
            damage_percent=366,
        )

    def on_tick(self):
        super().on_tick()
        self.damage()
        self.character.gain_anima(
            self.anima_per_tick
        )  # TODO: Maximum of 3 per Tick in AOE.
