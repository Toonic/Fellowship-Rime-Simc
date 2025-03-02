"""Module for the spells for Rime character."""

from enum import Enum

from .spell import RimeSpell


class RimeSpellEnum(Enum):
    """
    Enum for all the spells in Rime.
    """

    WRATH_OF_WINTER = RimeSpell(
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
    ICE_BLITZ = RimeSpell(
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
    DANCE_OF_SWALLOWS = RimeSpell(
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
    COLD_SNAP = RimeSpell(
        "Cold Snap",
        cast_time=0,
        cooldown=8,
        mana_generation=0,
        winter_orb_cost=-1,
        damage_percent=204,
    )
    ICE_COMET = RimeSpell(
        "Ice Comet",
        cast_time=0,
        cooldown=0,
        mana_generation=0,
        winter_orb_cost=3,
        damage_percent=300,
        min_target_count=3,
        max_target_count=1000,
    )
    GLACIAL_BLAST = RimeSpell(
        "Glacial Blast",
        cast_time=2.0,
        cooldown=0,
        mana_generation=0,
        winter_orb_cost=2,
        damage_percent=504,
        min_target_count=1,
        max_target_count=2,
    )
    BURSTING_ICE = RimeSpell(
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
    FREEZING_TORRENT = RimeSpell(
        "Freezing Torrent",
        cast_time=2.0,
        cooldown=10,
        mana_generation=6,
        winter_orb_cost=0,
        damage_percent=390,
        channeled=True,
        ticks=6,
    )
    FROST_BOLT = RimeSpell(
        "Frost Bolt",
        cast_time=1.5,
        cooldown=0,
        mana_generation=3,
        winter_orb_cost=0,
        damage_percent=73,
    )
    ANIMA_SPIKES = RimeSpell(
        "Anima Spikes",
        cast_time=0,
        cooldown=0,
        mana_generation=0,
        winter_orb_cost=0,
        damage_percent=36,
        hits=3,
    )
    SOULFROST_TORRENT = RimeSpell(
        "Soulfrost Torrent",
        cast_time=4.0,
        cooldown=10,
        mana_generation=11,
        winter_orb_cost=0,
        damage_percent=1430,  # Damage is set to 1560 because of ingame bug.
        channeled=True,
        ticks=11,
    )


class RimeBuffEnum(Enum):
    """
    Enum for all the buffs in Rime.
    """

    SOULFROST_BUFF = RimeSpell(
        "Soulfrost Buff", is_buff=True, debuff_duration=100000
    )
    GLACIAL_ASSAULT_BUFF = RimeSpell(
        "Glacial Assault", is_buff=True, debuff_duration=100000
    )
    COMET_BONUS = RimeSpell(
        "Ice Comet",
        cast_time=0,
        cooldown=0,
        mana_generation=0,
        winter_orb_cost=0,
        damage_percent=300,
    )
    BOOSTED_BLAST = RimeSpell(
        "Boosted Glacial Blast",
        cast_time=0,
        cooldown=0,
        mana_generation=0,
        winter_orb_cost=2,
        damage_percent=1008,
    )
