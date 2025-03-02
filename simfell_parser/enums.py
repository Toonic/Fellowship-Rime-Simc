"""Enum classes for the parser."""

from enum import Enum


class Gem(Enum):
    """Enum for gem types."""

    RUBY = "ruby"
    AMETHYST = "amethyst"
    TOPAZ = "topaz"
    EMERALD = "emerald"
    SAPPHIRE = "sapphire"
    DIAMOND = "diamond"


class Tier(Enum):
    """Enum for tier levels."""

    T1 = 1
    T2 = 2
    T3 = 3
    T4 = 4
    T5 = 5
    T6 = 6
    T7 = 7
    T8 = 8
    T9 = 9
    T10 = 10


class TierSet(Enum):
    """Enum for tier sets."""

    WYRMLING_VIGOR = "Wyrmling Vigor"
