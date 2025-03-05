from characters.rime import RimeSpell
from .dance_of_swallows import DanceOfSwallows


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
        if (
            self.character.simulation.debuffs.get(
                DanceOfSwallows().simfell_name
            )
            is not None
        ):
            self.character.dance_of_swallows.damage()
