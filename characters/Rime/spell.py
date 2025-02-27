"""Module for the spells for Rime character."""

from enum import Enum

from base.spell import Spell


class RimeSpell(Enum):
    """
    Enum for all the spells in Rime.
    """

    WRATH_OF_WINTER = Spell(
        "Wrath of Winter",
        cast_time=0,
        cooldown=600,
        mana_generation=0,
        winter_orb_cost=0,
        damage_percent=0,
        is_buff=True,
        ticks=10,
        debuff_duration=20,
    )
    ICE_BLITZ = Spell(
        "Ice Blitz",
        cast_time=0,
        cooldown=120,
        mana_generation=0,
        winter_orb_cost=0,
        damage_percent=0,
        is_buff=True,
        ticks=0,
        debuff_duration=20,
    )
    DANCE_OF_SWALLOWS = Spell(
        "Dance of Swallows",
        cast_time=0,
        cooldown=60,
        mana_generation=0,
        winter_orb_cost=2,
        damage_percent=53,
        is_debuff=True,
        ticks=0,
        debuff_duration=20,
    )
    COLD_SNAP = Spell(
        "Cold Snap",
        cast_time=0,
        cooldown=8,
        mana_generation=0,
        winter_orb_cost=-1,
        damage_percent=204,
    )
    ICE_COMET = Spell(
        "Ice Comet",
        cast_time=0,
        cooldown=0,
        mana_generation=0,
        winter_orb_cost=3,
        damage_percent=300,
    )
    GLACIAL_BLAST = Spell(
        "Glacial Blast",
        cast_time=2.0,
        cooldown=0,
        mana_generation=0,
        winter_orb_cost=2,
        damage_percent=504,
    )
    BURSTING_ICE = Spell(
        "Bursting Ice",
        cast_time=2.0,
        cooldown=15,
        mana_generation=6,
        winter_orb_cost=0,
        damage_percent=366,
        is_debuff=True,
        ticks=6,
        debuff_duration=3,
        do_debuff_damage=True,
    )
    FREEZING_TORRENT = Spell(
        "Freezing Torrent",
        cast_time=2.0,
        cooldown=10,
        mana_generation=6,
        winter_orb_cost=0,
        damage_percent=390,
        channeled=True,
        ticks=6,
    )
    FROST_BOLT = Spell(
        "Frost Bolt",
        cast_time=1.5,
        cooldown=0,
        mana_generation=3,
        winter_orb_cost=0,
        damage_percent=73,
    )
    ANIMA_SPIKES = Spell(
        "Anima Spikes",
        cast_time=0,
        cooldown=0,
        mana_generation=0,
        winter_orb_cost=0,
        damage_percent=36,
        hits=3,
    )
    SOULFROST_TORRENT = Spell(
        "Soulfrost Torrent",
        cast_time=2.0,
        cooldown=10,
        mana_generation=12,
        winter_orb_cost=0,
        damage_percent=1560,  # Damage is set to 1560 because of ingame bug.
        channeled=True,
        ticks=12,
    )


class RimeBuff(Enum):
    """
    Enum for all the buffs in Rime.
    """

    SOULFROST_BUFF = Spell(
        "Soulfrost Buff", is_buff=True, debuff_duration=100000
    )
    GLACIAL_ASSAULT_BUFF = Spell(
        "Glacial Assault", is_buff=True, debuff_duration=100000
    )
    COMET_BONUS = Spell(
        "Ice Comet",
        cast_time=0,
        cooldown=0,
        mana_generation=0,
        winter_orb_cost=0,
        damage_percent=300,
    )
    BOOSTED_BLAST = Spell(
        "Glacial Blast",
        cast_time=0,
        cooldown=0,
        mana_generation=0,
        winter_orb_cost=2,
        damage_percent=604,
    )
