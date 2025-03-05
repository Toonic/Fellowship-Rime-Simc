"""Utility functions for the simfell_parser module."""

from typing import TypeVar, TYPE_CHECKING, Optional, Type, Dict

from characters.rime.rime import (
    WrathOfWinter,
    FrostBolt,
    ColdSnap,
    FreezingTorrent,
    BurstingIce,
    GlacialBlast,
    IceComet,
    DanceOfSwallows,
    IceBlitz,
    AnimaSpikes,
    Rime,
)

if TYPE_CHECKING:
    from base import BaseSpell, BaseCharacter

SpellType = TypeVar("SpellType", bound="BaseSpell")
CharacterType = TypeVar("CharacterType", bound="BaseCharacter")


def map_spell_name_to_class(spell_name: str) -> Type[SpellType]:
    """Map a spell name to a class."""

    class_name = spell_name.split("/")[1].split("_")
    class_name = "".join([word.capitalize() for word in class_name])

    # Dictionary to map class names to their corresponding classes
    spell_classes: Dict[str, Type["BaseSpell"]] = {
        "WrathOfWinter": WrathOfWinter,
        "FrostBolt": FrostBolt,
        "ColdSnap": ColdSnap,
        "FreezingTorrent": FreezingTorrent,
        "BurstingIce": BurstingIce,
        "GlacialBlast": GlacialBlast,
        "IceComet": IceComet,
        "DanceOfSwallows": DanceOfSwallows,
        "IceBlitz": IceBlitz,
        "AnimaSpikes": AnimaSpikes,
    }

    spell_class: Optional[SpellType] = spell_classes.get(class_name, None)
    if spell_class is None:
        raise ValueError(f"Spell class '{class_name}' not found.")

    return spell_class


def map_character_name_to_class(character_name: str) -> Type[CharacterType]:
    """Map a character name to a class."""

    class_name = character_name.capitalize()

    # Dictionary to map class names to their corresponding classes
    character_classes: Dict[str, Type["BaseCharacter"]] = {
        "Rime": Rime,
    }

    character_class: Optional[CharacterType] = character_classes.get(
        class_name, None
    )
    if character_class is None:
        raise ValueError(f"Character class '{class_name}' not found.")

    return character_class
