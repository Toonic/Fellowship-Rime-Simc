from rime import RimeSpell


class GlacialBlast(RimeSpell):
    """Glacial Blast Spell"""

    def __init__(self):
        super().__init__(
            "Glacial Blast",
            cast_time=2.0,
            damage_percent=504,
            winter_orb_cost=2,
        )

    def crit_chance_modifiers(self, crit_chance):
        # TODO: Better handling of talents instead of string matching.
        if "Glacial Assault" in self.character.talents:
            crit_chance += 20
        return crit_chance
