from characters.rime import RimeDebuff
from characters.rime.talent import CoalescingIceTalent, RimeTalents


class BurstingIceDebuff(RimeDebuff):
    """Glacial Assault buff."""

    maximum_possible_anima = 3

    def __init__(self):
        super().__init__(
            "Bursting Ice",
            anima_per_tick=1,
            ticks=6,
            base_tick_duration=0.5,
            duration=3.15,
            damage_percent=366,
        )

    def damage_modifiers(self, damage):
        if self.character.has_talent(RimeTalents.COALESCING_ICE):
            return damage * (
                1 + (CoalescingIceTalent.bonus_bursting_damage / 100)
            )

        return damage

    def on_tick(self):
        super().on_tick()
        self.damage()
        anima_gain = self.anima_per_tick

        # TODO: Check to see if this is 1 target only.
        if self.character.has_talent(RimeTalents.COALESCING_ICE):
            anima_gain += CoalescingIceTalent.bonus_anima_single_target

        self.character.gain_anima(min(anima_gain, self.maximum_possible_anima))
