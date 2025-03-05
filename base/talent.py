"""Module for Talents"""

from typing import TypeVar
from dataclasses import dataclass
from enum import Enum

CharacterTypeT = TypeVar("CharacterTypeT", bound="CharacterTalent")


@dataclass
class Talent:
    """Talent class."""

    identifier: str
    name: str


class CharacterTalent(Enum):
    """Enum for Rime's talents."""

    @classmethod
    def get_by_identifier(cls, identifier: str):
        """Get a talent by its identifier."""

        for talent in cls:
            if talent.value.identifier == identifier:
                return talent
        return None
