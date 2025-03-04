"""Module for the Spell class."""

import random
from abc import ABC
from typing import TYPE_CHECKING, final

if TYPE_CHECKING:
    from .character import BaseCharacter


class BaseSpell(ABC):
    """Abstract base class for all spells."""

    def __init__(
        self,
        name="",
        cast_time=0,  # The casttime of the spell.
        cooldown=0,  # The cooldown of the spell.
        # The Damage the spell does based on the players main stat.
        damage_percent=0,
        channeled=False,  # If the spell is channeled or not.
        ticks=1,  # How many ticks of damage over the duration.
        has_gcd=True,  # If the spell has a GCD or not.
        # If the spell can be cast while GCD  is happening or not.
        can_cast_on_gcd=False,
        # If the spell can be cast while casting or not.
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
        self.character = None

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
        # TODO: Add the Conditional check here from the SimFell file
        # as an additional check.
        return self.remaining_cooldown <= 0

    def effective_cast_time(self) -> float:
        """Returns the effective cast time of the spell.
        Including any modifiers."""
        return self.cast_time * (1 - self.character.get_haste() / 100)

    def cast(self, do_damage=True) -> None:
        """Casts the spell."""
        if self.channeled:
            self.character.simulation.gcd = self.get_gcd()
            tick_interval = self.effective_cast_time() / self.ticks
            self.set_cooldown()  # Channeled spells cooldown starts on cast.
            for _ in range(self.ticks):
                self.character.simulation.update_time(tick_interval)
                if do_damage:
                    self.damage()
                self.on_tick()
        else:
            self.character.simulation.update_time(self.effective_cast_time())
            if do_damage:
                self.damage()
            self.on_cast_complete()
            self.character.simulation.gcd = self.get_gcd()

    # NOTE: Public because Tariq has some spells with a static GCD
    # so this will future support that.
    def get_gcd(self) -> float:
        """Returns the GCD of the spell."""
        return (
            1.5 / (1 + self.character.get_haste() / 100) if self.has_gcd else 0
        )

    @final
    def damage(self) -> float:
        """Returns the damage of the spell. Including any modifiers."""
        # TODO: Handle AOE.
        damage = self.damage_percent  # The base damage of the spell.
        damage = self.damage_modifiers(
            damage  # Damage modifiers that modify the base %.
        )
        damage = self.damage_modified_player_stats(
            damage  # The damage after being modified by player stats.
        )
        damage *= 1 + self.character.damage_multiplier

        # Roll for Crit Damage.
        if random.uniform(0, 100) < self.get_crit_chance():
            damage *= 2  # TODO: Include Crit Power.

        if self.ticks > 1:
            damage /= self.ticks

        if damage > 0:
            if self.character.simulation.do_debug:
                print(
                    f"Time {self.character.simulation.time:.2f}: "
                    + f"{self.name} "
                    + f"deals {damage:.2f} damage"
                )

        self.character.simulation.damage += damage

    # Used as an override for damage modifiers from Talents and other sources.
    def damage_modifiers(self, damage) -> float:
        """Returns the damage of the spell. Including any modifiers."""
        return damage

    @final
    def damage_modified_player_stats(self, damage) -> float:
        """Returns the damage of the spell after being modified
        by player stats"""
        return (
            (damage / 100)
            * self.character.get_main_stat()
            * (1 + self.character.get_expertise() / 100)
        )

    @final
    def get_crit_chance(self) -> float:
        """Returns the crit chance of the spell."""
        return self.crit_chance_modifiers(self.character.get_crit())

    def crit_chance_modifiers(self, crit_chance) -> float:
        """Returns the crit chance of the spell. Including any modifiers."""

        # NOTE: This method will be used to override the crit chance
        # of the spell.

        return crit_chance

    def on_tick(self) -> None:
        """The effect of the spell on each tick."""

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

    def __init__(self, *args, duration=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.duration = duration
        self.base_tick_rate = duration / self.ticks
        self.tick_rate = 0
        self.time_to_next_tick = 0

    def cast(self, do_damage=False):
        super().cast(do_damage)

    def on_cast_complete(self):
        super().on_cast_complete()
        self.apply_debuff()

    def apply_debuff(self) -> None:
        """Applies the debuff to the target."""

        # Fellowship for some reason has an additional 0.15 Seconds
        # for debuffs. WHY?!
        self.remaining_time = self.duration + 0.15
        # self.tick_rate = self.base_tick_rate * (
        #     1 + (self.character.get_haste() / 100)
        # )
        self.tick_rate = self.base_tick_rate  # Temporary testing against old.
        self.time_to_next_tick = self.tick_rate
        self.character.simulation.debuffs[self.simfell_name] = self

        if self.character.simulation.do_debug:
            print(
                f"Time {self.character.simulation.time:.2f}: "
                + f"Applied {self.name} "
                + "debuff to enemy."
            )
        # TODO: Determine if there is a maximum buff/debuff count,
        # and if re-casting it refreshes the duration.

    def update_remaining_duration(self, delta_time: int) -> None:
        """Decreases the remaining buff/debuff duration by the delta time."""
        if self.character.simulation.do_debug:
            print(
                f"Time {self.character.simulation.time:.2f}: "
                + "Updating remaining duration"
            )

        while delta_time > 0 and self.remaining_time > 0:
            if delta_time >= self.time_to_next_tick:
                delta_time -= self.time_to_next_tick
                self.remaining_time -= self.time_to_next_tick
                self.time_to_next_tick = self.base_tick_rate
                self.on_tick()
            else:
                self.time_to_next_tick -= delta_time
                self.remaining_time -= delta_time
                delta_time = 0

        if self.remaining_time <= 0:
            if self.character.simulation.do_debug:
                print(
                    f"Time {self.character.simulation.time:.2f}: "
                    + f"Removing {self.name} debuff"
                )
            self.remove_debuff()

    def remove_debuff(self) -> None:
        """Removes the debuff from the target."""

        self.remaining_time = 0
        self.character.simulation.debuffs.pop(self.simfell_name, None)
        if self.character.simulation.do_debug:
            print(
                f"Time {self.character.simulation.time:.2f}: "
                + f"Removed {self.name} "
                + "debuff from enemy."
            )


class BaseBuff(BaseSpell):
    """Abstract base class for all buffs."""

    remaining_time = 0

    def __init__(self, *args, duration=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.duration = duration
        self.base_tick_rate = duration / self.ticks
        self.tick_rate = 0
        self.time_to_next_tick = 0

    def cast(self, do_damage=False):
        super().cast(do_damage)

    def on_cast_complete(self):
        super().on_cast_complete()
        self.apply_buff()

    def apply_buff(self) -> None:
        """Applies the debuff to the target."""
        # self.tick_rate = self.base_tick_rate * (
        #     1 + (self.character.get_haste() / 100)
        # )
        self.tick_rate = self.base_tick_rate  # Temporary testing against old.
        self.time_to_next_tick = self.tick_rate
        self.remaining_time = self.duration
        self.character.buffs[self.simfell_name] = self

        if self.character.simulation.do_debug:
            print(
                f"Time {self.character.simulation.time:.2f}: "
                + f"Applied {self.name} "
                + "buff to character."
            )
        # TODO: Determine if there is a maximum buff/debuff count,
        # and if re-casting it refreshes the duration.

    def update_remaining_duration(self, delta_time: float) -> None:
        """Decreases the remaining buff duration by the delta time."""
        while delta_time > 0 and self.remaining_time > 0:
            if delta_time >= self.time_to_next_tick:
                self.remaining_time -= self.time_to_next_tick
                self.time_to_next_tick = self.base_tick_rate
                self.on_tick()
            else:
                self.time_to_next_tick -= delta_time
                self.remaining_time -= delta_time
                delta_time = 0

        if self.remaining_time <= 0:
            self.remove_buff()

    def remove_buff(self) -> None:
        """Removes the buff from the character."""

        self.remaining_time = 0
        self.character.buffs.pop(self.simfell_name, None)

        if self.character.simulation.do_debug:
            print(
                f"Time {self.character.simulation.time:.2f}: "
                + f"Removed {self.name} "
                + "buff from character."
            )
