"""Module for Talents"""

from typing import TypeVar, Optional, Type
from dataclasses import dataclass
from enum import Enum

CharacterTalentT = TypeVar("CharacterTalentT", bound="CharacterTalent")


@dataclass
class Talent:
    """Talent class."""

    identifier: str
    name: str


class CharacterTalent(Enum):
    """Enum for Rime's talents."""

    # value: Talent

    @classmethod
    def get_by_identifier(
        cls: Type["CharacterTalent"], identifier: str
    ) -> Optional["CharacterTalent"]:
        """Get a talent by its identifier."""

        for talent in cls:
            if talent.value.identifier == identifier:
                return talent
        return None
