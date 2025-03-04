"""Module for the Simulation class."""

from typing import Dict
from base.spell import BaseDebuff
from base.character import BaseCharacter

from rich import print  # pylint: disable=redefined-builtin


class Simulation:
    """Class for the Simulation."""

    def __init__(
        self,
        character: BaseCharacter,
        duration=180,
        enemy_count=1,
        do_debug=False,
        is_deterministic=False,
    ):
        """Initialize the Simulation."""

        self.character = character
        character.set_simulation(self)
        self.duration = duration
        self.enemy_count = enemy_count
        self.do_debug = do_debug
        self.time = 0
        self.gcd = 0
        self.ability_queue = []
        self.debuffs: Dict[str, BaseDebuff] = {}
        self.damage = 0
        self.damage_table = {}
        self.is_deterministic = is_deterministic

        if self.is_deterministic:
            self.character._crit = 0
            self.character._spirit = 0

    def update_time(self, delta_time: float):
        """Update the time of the simulation."""
        delta_time = round(delta_time, 2)
        self.time += delta_time
        self.gcd -= delta_time

        # Update spell cooldowns
        for spell in self.character.spells.values():
            spell.update_cooldown(delta_time)

        # Update Players Buffs
        for buff in list(self.character.buffs.values()):
            if self.do_debug:
                print(
                    f"Time {self.time:.2f}: Updating "
                    + f"[dark_green]{buff.name} (Buff)[/dark_green] "
                    + "remaining duration"
                )

            buff.update_remaining_duration(delta_time)

        # Update Debuffs on an Enemy.
        # TODO: In the future we will want to keep track of each enemy
        # and each debuff. This will be important for Multi-Dotting
        # in the future.

        for debuff in list(self.debuffs.values()):
            if self.do_debug:
                print(
                    f"Time {self.time:.2f}: Updating "
                    + f"[deep_pink4]{debuff.name} (Debuff)[/deep_pink4] "
                    + "remaining duration"
                )

            debuff.update_remaining_duration(delta_time)

    def run(self):
        """Run the simulation."""

        while self.time <= self.duration:
            if self.gcd > 0:
                if self.do_debug:
                    print(
                        f"Time {self.time:.2f}: GCD: {self.gcd:.2f}"
                        + " | [grey37]Updating time by GCD"
                    )
                self.update_time(self.gcd)

            for spell in self.character.rotation:
                if self.character.spells[spell].is_ready():
                    if self.do_debug:
                        spell_name = self.character.spells[spell].name
                        print(
                            f"Time {self.time:.2f}: "
                            + f"Casting [cornflower_blue]{spell_name}"
                            + "[/cornflower_blue]. "
                        )
                    self.character.spells[spell].cast()
                    break
            else:
                if self.do_debug:
                    print(
                        f"Time {self.time:.2f}: No Spell Ready"
                        + " | Updating time by 0.1"
                    )
                self.update_time(0.1)

        return self.damage / self.duration
