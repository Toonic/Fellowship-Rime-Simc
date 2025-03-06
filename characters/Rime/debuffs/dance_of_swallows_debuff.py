from characters.rime import RimeDebuff


class DanceOfSwallowsDebuff(RimeDebuff):
    """Glacial Assault buff."""

    def __init__(self):
        super().__init__(
            "Dance of Swallows",
            duration=20,
            damage_percent=53,
        )
