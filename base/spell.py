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
        can_cast_while_casting=False,
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
        self.remaining_cooldown = 0
        self.character = None  # Initialize character attribute

    @final
    def set_character(self, character: "BaseCharacter") -> None:
        """Sets the character for the spell."""
        self.character = character

    @property
    def simfell_name(self) -> str:
        """Returns the name of the spell in the simfell file."""

        return self.name.lower().replace(" ", "_")

    def is_ready(self) -> bool:
        """Returns True if the spell is ready to be cast."""
        # TODO: Add the Conditional check here from the SimFell file as an additional check.
        if self.remaining_cooldown <= 0:
            return True
        return False

    def effective_cast_time(self) -> float:
        """Returns the effective cast time of the spell. Including any modifiers."""
        return self.cast_time * (1 - self.character.get_haste() / 100)

    def cast(self) -> None:
        """Casts the spell."""
        # TODO: Pseudo Code. - I want to bring in the simulation.
        #       Possibly even the character tot he spell.
        #       I dislike passing in character for all of these functions.

        if self.channeled:
            self.character.simulation.gcd = self.get_gcd()
            tick_interval = self.effective_cast_time() / self.ticks
            self.set_cooldown()  # Channeled spells cooldown starts on cast.
            for _ in range(self.ticks):
                self.character.simulation.update_time(tick_interval)
                self.damage()
                # self.on_tick_effect(character)
        else:
            self.character.simulation.update_time(self.effective_cast_time())
            self.damage()
            self.on_cast_complete()
            self.character.simulation.gcd = self.get_gcd()
            # simulation.apply_damage(self.damage())

    # NOTE: Public because Tariq has some spells with a static GCD so this will future support that.
    def get_gcd(self) -> float:
        """Returns the GCD of the spell."""
        if self.has_gcd:
            return 1.5 / (1 + self.character.get_haste() / 100)
        return 0

    @final
    def damage(self) -> float:
        """Returns the damage of the spell. Including any modifiers."""
        # TODO: Handle AOE.

        damage = self.damage_percent  # The base damage of the spell.
        damage = self.damage_modifiers(
            damage
        )  # Any additional modifiers being applied.
        damage = self.damage_modified_player_stats(
            damage
        )  # The damage after being modified by player stats.

        damage = damage * (1 + self.character.damage_multiplier)

        # Roll for Crit Damage.
        if random.uniform(0, 100) < self.get_crit_chance():
            damage = damage * 2  # TODO: Include Crit Power.

        if damage > 0:
            print(
                f"Time {self.character.simulation.time:.2f}: "
                + f"Cast {self.name}, "
                + f"dealing {damage:.2f} damage"
            )

        # TODO: Apply damage to simulation here instead?
        # self.character.simulation.apply_damage(damage)

    # Used as an override for damage modifiers from Talents and other sources.
    def damage_modifiers(self, damage) -> float:
        """Returns the damage of the spell. Including any modifiers."""
        return damage

    @final
    def damage_modified_player_stats(self, damage) -> float:
        """Returns the damage of the spell after being modified by player stats"""
        modified_damage = (damage / 100) * self.character.get_main_stat()
        modified_damage = modified_damage * (
            1 + self.character.get_expertise() / 100
        )
        return modified_damage

    @final
    def get_crit_chance(
        self,
    ) -> float:
        """Returns the crit chance of the spell."""
        crit_chance = self.character.get_crit()
        crit_chance = self.crit_chance_modifiers(crit_chance)
        return crit_chance

    def crit_chance_modifiers(self, crit_chance) -> float:
        """Returns the crit chance of the spell. Including any modifiers."""
        return crit_chance

    def on_tick(
        self,
    ) -> None:
        """The effect of the spell on each tick."""
        pass

    def on_cast_complete(self) -> None:
        """The effect of the spell when the cast is complete."""
        self.set_cooldown()

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
        self, *args, duration=0, **kwargs
    ):  # The duration of the debuff.
        super().__init__(*args, **kwargs)
        self.duration = duration
        self.base_tick_rate = duration / self.ticks

    def on_cast_complete(self):
        super().on_cast_complete()
        self.apply_debuff()

    def apply_debuff(self) -> None:
        """Applies the debuff to the target."""
        self.remaining_time = (
            self.duration + 0.15
        )  # Fellowship for some reason has an additional 0.15 Seconds for debuffs. WHY?!
        self.character.simulation.debuffs[self.simfell_name] = self
        print(
            f"Time {self.character.simulation.time:.2f}: "
            + f"Applied {self.name} "
            + "debuff to enemy."
        )
        # TODO: Determine if there is a maximum buff/debuff count, and if re-casting it refreshes the duration.

    def update_remaining_duration(self, delta_time: int) -> None:
        """Decreases the remaining buff/debuff duration by the delta time."""
        self.remaining_time -= delta_time
        if self.remaining_time <= 0:
            self.remove_debuff()

    def remove_debuff(self) -> None:
        """Removes the debuff from the target."""
        self.remaining_time = 0
        del self.character.simulation.debuffs[self.simfell_name]
        print(
            f"Time {self.character.simulation.time:.2f}: "
            + f"Removed {self.name} "
            + "debuff from enemy."
        )


class BaseBuff(BaseSpell):
    """Abstract base class for all buffs."""

    remaining_time = 0

    def __init__(
        self, *args, duration=0, **kwargs
    ):  # The duration of the buff
        super().__init__(*args, **kwargs)
        self.duration = duration
        self.base_tick_rate = duration / self.ticks

    def on_cast_complete(self):
        super().on_cast_complete()
        self.apply_buff()

    def apply_buff(self) -> None:
        """Applies the debuff to the target."""
        self.remaining_time = self.duration
        self.character.buffs[self.simfell_name] = self
        print(
            f"Time {self.character.simulation.time:.2f}: "
            + f"Applied {self.name} "
            + "buff to character."
        )
        # TODO: Determine if there is a maximum buff/debuff count, and if re-casting it refreshes the duration.

    def update_remaining_duration(self, delta_time: float) -> None:
        """Decreases the remaining buff duration by the delta time."""
        self.remaining_time -= delta_time
        if self.remaining_time <= 0:
            self.remove_buff()

    def remove_buff(self) -> None:
        """Removes the buff from the character."""
        self.remaining_time = 0
        del self.character.buffs[self.simfell_name]
        print(
            f"Time {self.character.simulation.time:.2f}: "
            + f"Removed {self.name} "
            + "buff to character."
        )
