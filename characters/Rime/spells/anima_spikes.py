"""Module for Anima Spikes Spell"""

from characters.rime import RimeSpell


class AnimaSpikes(RimeSpell):
    """Anima Spikes Spell"""

    def __init__(self):
        super().__init__("Anima Spikes", damage_percent=36)
