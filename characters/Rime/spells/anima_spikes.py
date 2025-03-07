"""Module for Anima Spikes Spell"""

from characters.rime import RimeSpell
from characters.rime.talent import RimeTalents
from utils.enums import SpellSimFellName


class AnimaSpikes(RimeSpell):
    """Anima Spikes Spell"""

    def __init__(self):
        super().__init__("Anima Spikes", damage_percent=36)

    def damage(self):
        super().damage()
        if self.character.has_talent(RimeTalents.ICY_FLOW):
            icy_flow = RimeTalents.ICY_FLOW.value
            self.character.spells[
                SpellSimFellName.FREEZING_TORRENT.value
            ].update_cooldown(icy_flow.torrent_cdr_from_anima_spikes)
