"""Module for Freezing Torrent Spell"""

from characters.rime import RimeSpell
from characters.rime.debuffs import DanceOfSwallowsDebuff


class FreezingTorrent(RimeSpell):
    """Freezing Torrent Spell"""

    # TODO: Future note to myself in the future:
    # I need to code PPM for Soulfrost which is at 1.5 PPM According to Devs.
    # Use WoW's RPPM calculations for this.

    def __init__(self):
        super().__init__(
            "Freezing Torrent",
            cast_time=2.0,
            cooldown=10,
            damage_percent=390,
            anima_per_tick=1,
            channeled=True,
            ticks=6,
        )

    def on_tick(self):
        self.character.gain_anima(self.anima_per_tick)

        dance_of_swallows = self.character.simulation.get_debuff(
            DanceOfSwallowsDebuff()
        )

        if dance_of_swallows is not None:
            dance_of_swallows.damage()
