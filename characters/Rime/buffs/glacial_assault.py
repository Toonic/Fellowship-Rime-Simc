from base import BaseBuff


class GlacialAssault(BaseBuff):
    """Glacial Assault buff."""

    def __init__(self):
        super().__init__(
            "Glacial Assault", duration=float("inf"), maximum_stacks=4
        )
