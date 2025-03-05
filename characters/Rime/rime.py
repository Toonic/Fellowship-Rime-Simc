"""Module for the Rime Character."""

from characters.rime import RimeSpell, RimeBuff, RimeDebuff
from base import BaseCharacter


# Defines the Rime Character class.
class Rime(BaseCharacter):
    """Stat Point DR"""

    main_stat_per_point = 1
    critPerPoint = 0.21
    expertisePerPoint = 0.21
    hastePerPoint = 0.21
    spiritPerPoint = 0.21

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
        if self.winter_orbs < 0:
            self.winter_orbs = 0


class WrathOfWinter(RimeBuff):
    """Wrath of Winter Spell"""

    haste_additional_bonus = 30
    damage_multiplier_bonus = 0.15

    def __init__(self):
        super().__init__(
            "Wrath of Winter",
            cast_time=0,
            duration=20,
            ticks=10,
            cooldown=1000,  # TODO: Spirit Gen instead.
        )

    def on_tick(self):
        self.character.gain_winter_orbs(1)

    def apply_buff(self):
        super().apply_buff()
        self.character.damage_multiplier += self.damage_multiplier_bonus
        self.character.haste_additional += self.haste_additional_bonus

    def remove_buff(self):
        super().remove_buff()
        self.character.damage_multiplier -= self.damage_multiplier_bonus
        self.character.haste_additional -= self.haste_additional_bonus


class FrostBolt(RimeSpell):
    """Frost Bolt Spell"""

    def __init__(self):
        super().__init__(
            "Frost Bolt", cast_time=1.5, damage_percent=73, anima_gain=3
        )


class ColdSnap(RimeSpell):
    """Cold Snap Spell"""

    def __init__(self):
        super().__init__(
            "Cold Snap", damage_percent=204, winter_orb_cost=-1, cooldown=8
        )

    def on_cast_complete(self):
        super().on_cast_complete()
        if (
            self.character.simulation.debuffs.get(
                DanceOfSwallows().simfell_name
            )
            is not None
        ):
            # Dance of Swallows is hard coded to trigger 10 times from ColdSnap
            for _ in range(10):
                self.character.dance_of_swallows.damage()


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


class BurstingIce(RimeDebuff):
    """Bursting Ice Spell"""

    def __init__(self):
        super().__init__(
            "Bursting Ice",
            cast_time=2.0,
            cooldown=15,
            damage_percent=366,
            anima_per_tick=1,
            ticks=6,
            duration=3,
        )

    def on_tick(self):
        super().on_tick()
        self.damage()
        self.character.gain_anima(self.anima_per_tick)


class GlacialBlast(RimeSpell):
    """Glacial Blast Spell"""

    def __init__(self):
        super().__init__(
            "Glacial Blast",
            cast_time=2.0,
            damage_percent=504,
            winter_orb_cost=2,
        )

    def crit_chance_modifiers(self, crit_chance):
        # TODO: Better handling of talents instead of string matching.
        if "Glacial Assault" in self.character.talents:
            crit_chance += 20
        return crit_chance


class IceComet(RimeSpell):
    """Ice Comet Spell"""

    def __init__(self):
        super().__init__("Ice Comet", damage_percent=300, winter_orb_cost=3)


class DanceOfSwallows(RimeDebuff):
    """Dance of Swallows Spell"""

    def __init__(self):
        super().__init__(
            "Dance of Swallows",
            cooldown=60,
            duration=20,
            damage_percent=53,
            winter_orb_cost=2,
        )


class IceBlitz(RimeBuff):
    """Ice Blitz Spell"""

    ice_blitz_damage_multiplier = 0.15

    def __init__(self):
        super().__init__(
            "Ice Blitz",
            duration=20,
            cooldown=120,
            has_gcd=False,
            can_cast_on_gcd=True,
            can_cast_while_casting=True,
        )

    def apply_buff(self):
        super().apply_buff()
        self.character.damage_multiplier += self.ice_blitz_damage_multiplier

    def remove_buff(self):
        super().remove_buff()
        self.character.damage_multiplier -= self.ice_blitz_damage_multiplier


class AnimaSpikes(RimeSpell):
    """Anima Spikes Spell"""

    def __init__(self):
        super().__init__("Anima Spikes", damage_percent=36)
