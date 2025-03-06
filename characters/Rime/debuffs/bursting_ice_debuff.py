from characters.rime import RimeDebuff


class BurstingIceDebuff(RimeDebuff):
    """Glacial Assault buff."""

    def __init__(self):
        super().__init__(
            "Bursting Ice",
            anima_per_tick=1,
            ticks=6,
            base_tick_duration=0.5,
            duration=3.15,
            damage_percent=366,
        )

    def on_tick(self):
        super().on_tick()
        self.damage()
        self.character.gain_anima(
            self.anima_per_tick
        )  # TODO: Maximum of 3 per Tick in AOE.
