from characters.rime import RimeSpell


class IceComet(RimeSpell):
    """Ice Comet Spell"""

    def __init__(self):
        super().__init__("Ice Comet", damage_percent=300, winter_orb_cost=3)
