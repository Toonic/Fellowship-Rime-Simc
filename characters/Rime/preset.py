"""Module for Rime's presets."""

from enum import Enum

from base import Character


class RimePreset(Enum):
    """Enum for Rime's presets."""

    DEFAULT = Character(
        intellect=300, crit=160, expertise=90, haste=120, spirit=50
    )
