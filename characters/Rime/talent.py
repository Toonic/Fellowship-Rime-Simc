"""Module for Rime's talents."""

from base import CharacterTalent, Talent


class RimeTalents(CharacterTalent):
    """Enum for Rime's talents."""

    CHILLBLAIN = Talent("1.1", "Chillblain")
    COALESCING_ICE = Talent("1.2", "Coalescing Ice")
    GLACIAL_ASSAULT = Talent("1.3", "Glacial Assault")
    UNRELENTING_ICE = Talent("2.1", "Unrelenting Ice")
    ICY_FLOW = Talent("2.2", "Icy Flow")
    TUNDRA_GUARD = Talent("2.3", "Tundra Guard")
    AVALANCHE = Talent("3.1", "Avalanche")
    WISDOM_OF_THE_NORTH = Talent("3.2", "Wisdom of the North")
    SOULFROST_TORRENT = Talent("3.3", "Soulfrost Torrent")
