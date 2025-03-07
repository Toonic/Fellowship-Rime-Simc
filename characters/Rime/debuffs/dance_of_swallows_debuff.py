"""Module for Dance of Swallows Debuff"""

from characters.rime import RimeDebuff
from characters.rime.talent import RimeTalents
from utils.enums import SpellSimFellName


class DanceOfSwallowsDebuff(RimeDebuff):
    """Dance of Swallos Debuff."""

    def __init__(self):
        super().__init__(
            "Dance of Swallows",
            duration=20,
            damage_percent=53,
        )

    def damage(self):
        super().damage()
        if self.character.has_talent(RimeTalents.ICY_FLOW):
            icy_flow = RimeTalents.ICY_FLOW.value
            self.character.spells[
                SpellSimFellName.FREEZING_TORRENT.value
            ].update_cooldown(icy_flow.torrent_cdr_from_anima_spikes)
