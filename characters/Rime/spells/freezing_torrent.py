"""Module for Freezing Torrent Spell"""

from characters.rime import RimeSpell
from characters.rime.debuffs import DanceOfSwallowsDebuff
from characters.rime.buffs import SoulfrostBuff
from characters.rime.spells import BurstingIce
from characters.rime.talent import (
    RimeTalents,
    ChillblainTalent,
    UnrelentingIceTalent,
    SoulfrostTorrentTalent,
)


class FreezingTorrent(RimeSpell):
    """Freezing Torrent Spell"""

    # TODO: Future note to myself in the future:
    # I need to code PPM for Soulfrost which is at 1.5 PPM According to Devs.
    # Use WoW's RPPM calculations for this.

    in_soulfrost = False

    def __init__(self):
        super().__init__(
            "Freezing Torrent",
            cast_time=2.0,
            cooldown=10,
            damage_percent=65,  # Tick Based.
            anima_per_tick=1,
            channeled=True,
            base_tick_duration=0.4,
        )

    def cast(self, do_damage=True):
        if self.character.has_talent(
            RimeTalents.SOULFROST_TORRENT
        ) and self.character.has_buff(SoulfrostBuff()):
            if self.channeled:
                self.in_soulfrost = True
                self.character.simulation.gcd = self.get_gcd()
                self.set_cooldown()  # Channeled spells cooldown starts on cast.
                self.ticks = int(
                    (
                        self.cast_time
                        * SoulfrostTorrentTalent.torrent_bonus_duration
                    )
                    / self.base_tick_duration
                )
                self.character.get_buff(SoulfrostBuff()).remove()
                self.damage()
                for _ in range(self.ticks):
                    self.character.simulation.update_time(
                        self.base_tick_duration
                    )
                    if do_damage:
                        self.damage()
                    self.on_tick()
        else:
            self.in_soulfrost = False
            super().cast(do_damage)

    def effective_cast_time(self):
        if self.character.has_talent(RimeTalents.SOULFROST_TORRENT):
            if self.character.has_buff(SoulfrostBuff()):
                return (
                    super().effective_cast_time()
                    * SoulfrostTorrentTalent.torrent_bonus_duration
                )
        return super().effective_cast_time()

    def damage_modifiers(self, damage):
        if self.character.has_talent(RimeTalents.CHILLBLAIN):
            damage = damage * (
                1 + (ChillblainTalent.bonus_torrent_damage / 100)
            )

        if self.in_soulfrost:
            damage = damage * SoulfrostTorrentTalent.torrent_bonus_damage

        return damage

    def on_tick(self):
        self.character.gain_anima(self.anima_per_tick)

        if self.character.has_talent(RimeTalents.UNRELENTING_ICE):
            self.character.spells[BurstingIce().simfell_name].update_cooldown(
                UnrelentingIceTalent.bursting_ice_cdr_from_torrent
            )

        dance_of_swallows = self.character.simulation.get_debuff(
            DanceOfSwallowsDebuff()
        )

        if dance_of_swallows is not None:
            dance_of_swallows.damage()
