from characters.rime import RimeDebuff
from characters.rime.talent import IcyFlowTalent, RimeTalents


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
            from characters.rime.spells import FreezingTorrent

            self.character.spells[
                FreezingTorrent().simfell_name
            ].update_cooldown(IcyFlowTalent.torrent_cdr_from_anima_spikes)
