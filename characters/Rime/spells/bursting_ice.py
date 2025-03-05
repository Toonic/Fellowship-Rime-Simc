from characters.rime import RimeDebuff


class BurstingIce(RimeDebuff):
    """Bursting Ice Spell"""

    def __init__(self):
        super().__init__(
            "Bursting Ice",
            cast_time=2.0,
            cooldown=15,
            damage_percent=366,
            anima_per_tick=1,
            ticks=6,
            duration=3,
        )

    def on_tick(self):
        super().on_tick()
        self.damage()
        self.character.gain_anima(self.anima_per_tick)
