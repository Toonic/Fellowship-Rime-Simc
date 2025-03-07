"""Module for the Rime Character."""

import random
from characters.rime.spells import (
    AnimaSpikes,
    BurstingIce,
    ColdSnap,
    DanceOfSwallows,
    FreezingTorrent,
    FrostBolt,
    GlacialBlast,
    IceBlitz,
    IceComet,
    WrathOfWinter,
)

from characters.rime.talent import RimeTalents, AvalancheTalent

from characters.rime.buffs import IceBlitzBuff
from base import BaseCharacter


# Defines the Rime Character class.
class Rime(BaseCharacter):
    """Stat Point DR"""

    anima_spikes = None
    anima = 0
    winter_orbs = 0

    def __init__(self, intellect, crit, expertise, haste, spirit):
        super().__init__(intellect, crit, expertise, haste, spirit)
        self.anima = 0
        self.winter_orbs = 0

    def configure_spell_book(self):
        self.spells = {
            WrathOfWinter().simfell_name: WrathOfWinter(),
            FrostBolt().simfell_name: FrostBolt(),
            ColdSnap().simfell_name: ColdSnap(),
            FreezingTorrent().simfell_name: FreezingTorrent(),
            BurstingIce().simfell_name: BurstingIce(),
            GlacialBlast().simfell_name: GlacialBlast(),
            IceComet().simfell_name: IceComet(),
            DanceOfSwallows().simfell_name: DanceOfSwallows(),
            IceBlitz().simfell_name: IceBlitz(),
        }

        self.anima_spikes = AnimaSpikes()
        self.anima_spikes.character = self

        self.dance_of_swallows = DanceOfSwallows()
        self.dance_of_swallows.character = self

        # I couldn't find a clean way to handle this. Up for solutions.
        for spell in self.spells.values():
            spell.character = self

    def gain_anima(self, amount):
        """Gain Anima"""
        self.anima += amount
        if self.anima >= 10:
            self.anima = 0
            self.gain_winter_orbs(1)

        if IceBlitzBuff().simfell_name in self.buffs:
            for _ in range(amount):
                self.anima_spikes.cast()

    def gain_winter_orbs(self, amount):
        """Gain Winter Orbs"""
        self.winter_orbs += amount
        for _ in range(3):
            self.anima_spikes.cast()
        if self.winter_orbs > 5:
            self.winter_orbs = 5

    def lose_winter_orbs(self, amount):
        """Lose Winter Orbs"""
        self.winter_orbs -= amount
        self.winter_orbs = max(self.winter_orbs, 0)
        if random.uniform(0, 100) < self.get_spirit():
            self.winter_orbs += amount
            self.winter_orbs = min(self.winter_orbs, 5)

    def add_talent(self, talent):
        super().add_talent(talent)
        if talent == RimeTalents.AVALANCHE:
            self.crit_power_multiplier += AvalancheTalent.bonus_crit_power
