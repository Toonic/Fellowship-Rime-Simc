"""Module for Anima Spikes Spell"""

from typing import TYPE_CHECKING
from characters.rime import RimeSpell
from characters.rime.talent import RimeTalents, IcyFlowTalent

if TYPE_CHECKING:
    from characters.rime.spells import FreezingTorrent


class AnimaSpikes(RimeSpell):
    """Anima Spikes Spell"""

    def __init__(self):
        super().__init__("Anima Spikes", damage_percent=36)

    def damage(self):
        super().damage()
        if self.character.has_talent(RimeTalents.ICY_FLOW):
            from characters.rime.spells import FreezingTorrent

            self.character.spells[
                FreezingTorrent().simfell_name
            ].update_cooldown(IcyFlowTalent.torrent_cdr_from_anima_spikes)
