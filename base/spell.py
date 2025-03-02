"""Module for the Spell class."""

import random
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from typing import final

if TYPE_CHECKING:
    from .character import BaseCharacter


class BaseSpell(ABC):
    """Abstract base class for all spells."""

    def __init__(
        self,
        name="",
        cast_time=0,  # The casttime of the spell.
        cooldown=0,  # The cooldown of the spell.
        damage_percent=0,  # The Damage the spell does based on the players main stat.
        channeled=False,  # If the spell is channeled or not.
        ticks=1,  # How many ticks of damage over the duration.
        has_gcd=True,  # If the spell has a GCD or not.
        can_cast_on_gcd=False,  # If the spell can be cast while GCD  is happening or not.
        can_cast_while_casting=False,  # If the spell can be cast while another spell is being cast.
    ):
        self.name = name
        self.cast_time = cast_time
        self.cooldown = cooldown
        self.damage_percent = damage_percent
        self.channeled = channeled
        self.ticks = ticks
        self.has_gcd = has_gcd
        self.can_cast_on_gcd = can_cast_on_gcd
        self.can_cast_while_casting = can_cast_while_casting

    @property
    def simfell_name(self) -> str:
        """Returns the name of the spell in the simfell file."""

        return self.name.lower().replace(" ", "_")

    def is_ready(self, character: "BaseCharacter", enemy_count: int) -> bool:
        """Returns True if the spell is ready to be cast."""

    def effective_cast_time(self, character: "BaseCharacter") -> float:
        """Returns the effective cast time of the spell. Including any modifiers."""

    def cast(self, character: "BaseCharacter", enemy_count: int) -> None:
        """Casts the spell."""
        # TODO: Pseudo Code. - I want to bring in the simulation.
        #       Possibly even the character tot he spell.
        #       I dislike passing in character for all of these functions.

        # if self.channeled:
        #     tick_interval = self.cast_time / self.ticks
        #     self.set_cooldown() #Channeled spells cooldown starts on cast.
        #     for tick in range(self.ticks):
        #         simulation.progress_time(tick_interval)
        #         simulation.apply_damage(self.damage(character) / self.ticks)
        #         self.on_tick_effect(character)
        # else:
        #     simulation.progress_time(self.cast_time)
        #     simulation.apply_damage(self.damage(character))
        #     self.set_cooldown()

    @final
    def damage(self, character: "BaseCharacter") -> float:
        """Returns the damage of the spell. Including any modifiers."""

        damage = self.damage_percent  # The base damage of the spell.
        damage = self.damage_modifiers(
            character, damage
        )  # Any additional modifiers being applied.
        damage = self.damage_modified_player_stats(
            character, damage
        )  # The damage after being modified by player stats.

        # Roll for Crit Damage.
        if random.uniform(0, 100) < self.get_crit_chance(character):
            damage = damage * 2  # TODO: Include Crit Power.

        return damage

    # Used as an override for damage modifiers from Talents and other sources.
    def damage_modifiers(self, character: "BaseCharacter", damage) -> float:
        """Returns the damage of the spell. Including any modifiers."""
        return damage

    @final
    def damage_modified_player_stats(
        self, character: "BaseCharacter", damage
    ) -> float:
        """Returns the damage of the spell after being modified by player stats"""
        modified_damage = damage * character.main_stat
        modified_damage = modified_damage * (1 + character.expertise / 100)
        return modified_damage

    @final
    def get_crit_chance(self, character: "BaseCharacter") -> float:
        """Returns the crit chance of the spell."""
        crit_chance = character.crit
        crit_chance = self.crit_chance_modifiers(character, crit_chance)
        return character.crit

    def crit_chance_modifiers(
        self, character: "BaseCharacter", crit_chance
    ) -> float:
        """Returns the crit chance of the spell. Including any modifiers."""
        return crit_chance

    def on_tick(self, character: "BaseCharacter") -> None:
        """The effect of the spell on each tick."""
        pass

    def on_cast_complete(self, character: "BaseCharacter") -> None:
        """The effect of the spell when the cast is complete."""
        pass

    def set_cooldown(self) -> None:
        """Sets the cooldown of the spell."""
        self.remaining_cooldown = self.cooldown

    def reset_cooldown(self) -> None:
        """Resets the cooldown of the spell."""
        self.remaining_cooldown = 0

    def update_cooldown(self, delta_time: int) -> None:
        """Decreases the remaining cooldown by the delta time."""
        self.remaining_cooldown -= delta_time


class BaseDebuff(BaseSpell):
    """Abstract base class for all debuffs."""

    remaining_time = 0

    def __init__(
        self, duration=0, *args, **kwargs
    ):  # The duration of the buff/debuff.
        super().__init__(*args, **kwargs)
        self.duration = duration

    def apply_debuff(self) -> None:
        """Applies the debuff to the target."""
        self.remaining_time = self.duration

    def update_remaining_duration(self, delta_time: int) -> None:
        """Decreases the remaining buff/debuff duration by the delta time."""
        self.remaining_time -= delta_time
